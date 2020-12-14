from functools import partial
from urllib.parse import urlencode, urljoin

from modeltranslation.utils import build_localized_fieldname
from modeltranslation.translator import translator
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.shortcuts import redirect
from django.utils import translation

from django.db import models, transaction
from django.core.exceptions import ValidationError
from directory_constants import cms
from modelcluster.fields import ParentalManyToManyField
from . import forms, panels, snippets, widgets, helpers
from django.db.models import TextField
from core import constants

from directory_constants import choices

from wagtail.core.models import Page, Site

from django.core import signing
from django.conf import settings


ARTICLE_TYPES = [
    ('Blog', 'Blog'),
    ('Advice', 'Advice'),
    ('Case study', 'Case study'),
    ('Campaign', 'Campaign'),
]

VIDEO_TRANSCRIPT_HELP_TEXT = "If the video is present, a transcript must be provided."


@register_setting
class RoutingSettings(BaseSetting):
    root_path_prefix = models.CharField(
        blank=True,
        max_length=100,
        help_text=(
            "When determining URLs for a page in this site, the page's "
            "'url_path' is prepended with this value to create a URL that "
            "will be recognised by the relevant front-end app."
        ),
    )
    include_port_in_urls = models.BooleanField(
        default=True,
        verbose_name="include port in page URLs",
        help_text=(
            "This allows us to add dummy port values to Wagtail Site "
            "objects, to get around the unique hostname/port "
            "restrictions. If unchecked, the port won't be included "
            "in page URLs, and so becomes inconsequential."
        ),
    )

    panels = [
        MultiFieldPanel(
            heading="Routing configuration",
            children=[
                FieldPanel('root_path_prefix'),
                FieldPanel('include_port_in_urls'),
            ],
        )
    ]


class BasePage(Page):
    service_name = models.CharField(
        max_length=100,
        choices=choices.CMS_APP_CHOICES,
        db_index=True,
        null=True,
    )
    uses_tree_based_routing = models.BooleanField(
        default=False,
        verbose_name="tree-based routing enabled",
        help_text=(
            "Allow this page's URL to be determined by its slug, and " "the slugs of its ancestors in the page tree."
        ),
    )

    class Meta:
        abstract = True

    # URL fixes for legacy pages:
    # overrides the url path before the page slug is appended
    view_path = ''
    # overrides the entire url path including any custom slug the page has
    full_path_override = ''
    # if True when generating the url this page's slug will be ignored
    folder_page = False
    # overrides page.slug when generating the url
    slug_override = None

    subpage_types = []
    content_panels = []
    promote_panels = []
    read_only_fields = []

    _base_form_class = forms.WagtailAdminPageForm

    def __init__(self, *args, **kwargs):
        self.signer = signing.Signer()
        #  workaround modeltranslation patching Page.clean in an unpythonic way
        #  goo.gl/yYD4pw
        self.clean = lambda: None
        super().__init__(*args, **kwargs)

    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass

    @classmethod
    def fix_base_form_class_monkeypatch(cls):
        # workaround modeltranslation patching Page.base_form_class in an unpythonic way
        for model in cls.get_subclasses():
            base_form_class = getattr(model, '_base_form_class')
            setattr(model, 'base_form_class', base_form_class)

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.service_name = self.service_name_value
        return super().save(*args, **kwargs)

    def get_draft_token(self):
        return self.signer.sign(self.pk)

    def is_draft_token_valid(self, draft_token):
        try:
            value = self.signer.unsign(draft_token)
        except signing.BadSignature:
            return False
        else:
            return str(self.pk) == str(value)

    def get_non_prefixed_url(self, site=None):
        """
        Returns the page's url_path value with the url_path of the
        site's root page removed from the start, and starting with
        a forward slash. e.g. "/international/some-some-page".
        Used by get_tree_based_url() and for generating `old_path`
        values when creating redirects for this page
        """
        site = site or self.get_site()
        return self.url_path[len(site.root_page.url_path) :]  # noqa: E203

    def get_site(self):
        """
        Overrides Page.get_site() in order to fetch ``RoutingSettings``
        in the same query (for tree-based-routing). Will also create a
        ``RoutingSettings`` for the site if they haven't been created yet.
        """
        url_parts = self.get_url_parts()

        if url_parts is None:
            # page is not routable
            return

        site_id, root_url, page_path = url_parts

        site = Site.objects.select_related('routingsettings').get(id=site_id)

        # Ensure the site has routingsettings before returning
        try:
            # if select_related() above was successful, great!
            site.routingsettings
        except RoutingSettings.DoesNotExist:
            # RoutingSettings need creating
            site.routingsettings = RoutingSettings.objects.create(site=site)
        return site

    def get_tree_based_url(self, include_site_url=False):
        """
        Returns the URL for this page based on it's position in the tree,
        and the RoutingSettings options for the `Site` the page belongs to.
        Wagtail multisite must be set up in order for this to work.
        """
        site = self.get_site()
        routing_settings = site.routingsettings
        page_path = self.get_non_prefixed_url(site)

        # prefix path with prefix from routing settings
        prefix = routing_settings.root_path_prefix.rstrip('/')
        if prefix:
            page_path = prefix + '/' + page_path

        if include_site_url:
            if not routing_settings.include_port_in_urls:
                # prevent the port being included in site.root_url
                site.port = 80
            return urljoin(site.root_url, page_path)

        return page_path

    def get_url_path_parts(self):
        return [self.view_path, self.slug + '/']

    def get_url(self, is_draft=False, language_code=settings.LANGUAGE_CODE):
        url = self.full_url
        querystring = {}
        if is_draft:
            querystring['draft_token'] = self.get_draft_token()
        if language_code != settings.LANGUAGE_CODE:
            querystring['lang'] = language_code
        if querystring:
            url += '?' + urlencode(querystring)
        return url

    @property
    def ancestors_in_app(self):
        """
        Used by `full_path` and `get_tree_based_breadcrumbs`
        in BasePageSerializer.
        Starts at 2 to exclude the root page and the app page.
        Ignores 'folder' pages.
        """
        ancestors = self.get_ancestors()[2:]

        return [page for page in ancestors if not page.specific_class.folder_page]

    @property
    def full_path(self):
        """Return the full path of a page, ignoring the root_page and
        the app page.
        """
        if self.uses_tree_based_routing:
            return self.get_tree_based_url(include_site_url=False)

        # continue with existing behaviour
        if self.full_path_override:
            return self.full_path_override

        path_components = []

        if not self.view_path:
            path_components = [page.specific_class.slug_override or page.slug for page in self.ancestors_in_app]

        # need to also take into account the view_path if it's set
        else:
            path_components.insert(0, self.view_path.strip('/'))

        path_components.append(self.slug_override if self.slug_override is not None else self.slug)

        return '/{path}/'.format(path='/'.join(path_components))

    @property
    def full_url(self):
        if self.uses_tree_based_routing:
            return self.get_tree_based_url(include_site_url=True)

        # continue with existing behaviour
        domain = dict(constants.APP_URLS)[self.service_name_value]
        return helpers.get_page_full_url(domain, self.full_path)

    @property
    def url(self):
        return self.get_url()

    def get_localized_urls(self):
        # localized urls are used to tell google of alternative urls for
        # available languages, so there should be no need to expose the draft
        # url
        return [
            (language_code, self.get_url(language_code=language_code)) for language_code in self.translated_languages
        ]

    def serve(self, request, *args, **kwargs):
        return redirect(self.get_url())

    def get_latest_nested_revision_as_page(self):
        revision = self.get_latest_revision_as_page()
        foreign_key_names = [
            field.name for field in revision._meta.get_fields() if isinstance(field, models.ForeignKey)
        ]
        for name in foreign_key_names:
            field = getattr(revision, name)
            if hasattr(field, 'get_latest_revision_as_page'):
                setattr(revision, name, field.get_latest_revision_as_page())
        return revision

    @classmethod
    def get_translatable_fields(cls):
        return list(translator.get_options_for_model(cls).fields.keys())

    @classmethod
    def get_translatable_string_fields(cls):
        text_fields = ['TextField', 'CharField']
        return [
            name
            for name in cls.get_translatable_fields()
            if cls._meta.get_field(name).get_internal_type() in text_fields
        ]

    @classmethod
    def get_required_translatable_fields(cls):
        fields = [cls._meta.get_field(name) for name in cls.get_translatable_fields()]
        return [field.name for field in fields if not field.blank and field.model is cls]

    @property
    def translated_languages(self):
        fields = self.get_required_translatable_fields()
        if not fields:
            return [settings.LANGUAGE_CODE]
        language_codes = translation.trans_real.get_languages()
        # If new mandatory fields are added to a page model which has existing
        # instances on wagtail admin, the code below returns an empty list
        # because not all the mandatory fields are populated with English
        # content. An empty list means that the UI client will return a 404
        # because it can't find English, although the page is valid and still
        # published in CMS. I'm forcing en-gb in the list to avoid this issue.
        # This is diffucult to test both programmatically and manually and it's
        # a corner case so I'm leaving the next line effectively untested.
        # A manual test would have the following steps:
        # 1) Add a page model
        # 2) Create an instance of the above page model in wagtail
        # 3) Add at least one new mandatory field to the model
        # 4) Migrate CMS
        # 5) Open the page on the UI client without adding the new content
        translated_languages = ['en-gb']
        for language_code in language_codes:
            builder = partial(build_localized_fieldname, lang=language_code)
            if all(getattr(self, builder(field_name=name)) for name in fields):
                translated_languages.append(language_code)
                # cast to a set to remove double en-gb if any
        return list(set(translated_languages))

    @property
    def language_names(self):
        if len(self.translated_languages) > 1:
            names = [
                label
                for code, label, _ in settings.LANGUAGES_DETAILS
                if code in self.translated_languages and code != settings.LANGUAGE_CODE
            ]
            return 'Translated to {}'.format(', '.join(names))
        return ''

    @classmethod
    def can_exist_under(cls, parent):
        """
        Overrides Page.can_exist_under() so that pages cannot be created or
        moved below a parent page whos specific page class has been removed.
        """
        if not parent.specific_class:
            return False
        return super().can_exist_under(parent)


class MarkdownField(TextField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.MarkdownTextarea}
        defaults.update(kwargs)
        return super(MarkdownField, self).formfield(**defaults)


class ServiceNameUniqueSlugMixin:
    @staticmethod
    def _slug_is_available(slug, parent, page=None):
        from export_readiness import filters  # circular dependencies

        queryset = filters.ServiceNameFilter().filter_service_name(
            queryset=Page.objects.filter(slug=slug).exclude(pk=page.pk),
            name=None,
            value=page.service_name,
        )
        return not queryset.exists()

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.service_name = self.service_name_value
        if not self._slug_is_available(slug=self.slug, parent=self.get_parent(), page=self):
            raise ValidationError({'slug': 'This slug is already in use'})
        return super().save(*args, **kwargs)


class BaseDomesticPage(ServiceNameUniqueSlugMixin, BasePage):
    service_name_value = cms.EXPORT_READINESS

    class Meta:
        abstract = True


class CountryGuidePage(panels.CountryGuidePagePanels, BaseDomesticPage):
    """Make a cup of tea, this model is BIG! ☕"""

    class Meta:
        ordering = ['-heading']

    parent_page_types = [
        'core.LandingPage',
        'domestic.DomesticHomePage',
    ]
    subpage_types = [
        'export_readiness.ArticleListingPage',
        'export_readiness.ArticlePage',
        'export_readiness.CampaignPage',
    ]

    heading = models.CharField(max_length=255, verbose_name='Country name', help_text='Only enter the country name')
    sub_heading = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    heading_teaser = models.TextField(blank=True, verbose_name='Introduction')
    intro_cta_one_title = models.CharField(max_length=500, blank=True, verbose_name='CTA 1 title')
    intro_cta_one_link = models.CharField(max_length=500, blank=True, verbose_name='CTA 1 link')
    intro_cta_two_title = models.CharField(max_length=500, blank=True, verbose_name='CTA 2 title')
    intro_cta_two_link = models.CharField(max_length=500, blank=True, verbose_name='CTA 2 link')
    intro_cta_three_title = models.CharField(max_length=500, blank=True, verbose_name='CTA 3 title')
    intro_cta_three_link = models.CharField(max_length=500, blank=True, verbose_name='CTA 3 link')

    section_one_body = MarkdownField(
        null=True,
        verbose_name='3 unique selling points markdown',
        help_text='Use H3 (###) markdown for the 3 subheadings',
    )
    section_one_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Image for unique selling points',
    )
    section_one_image_caption = models.CharField(max_length=255, blank=True, verbose_name='Bullets image caption')
    section_one_image_caption_company = models.CharField(
        max_length=255, blank=True, verbose_name='Bullets image caption — company name'
    )

    statistic_1_number = models.CharField(max_length=255)
    statistic_1_heading = models.CharField(max_length=255)
    statistic_1_smallprint = models.CharField(max_length=255, blank=True)

    statistic_2_number = models.CharField(max_length=255)
    statistic_2_heading = models.CharField(max_length=255)
    statistic_2_smallprint = models.CharField(max_length=255, blank=True)

    statistic_3_number = models.CharField(max_length=255, blank=True)
    statistic_3_heading = models.CharField(max_length=255, blank=True)
    statistic_3_smallprint = models.CharField(max_length=255, blank=True)

    statistic_4_number = models.CharField(max_length=255, blank=True)
    statistic_4_heading = models.CharField(max_length=255, blank=True)
    statistic_4_smallprint = models.CharField(max_length=255, blank=True)

    statistic_5_number = models.CharField(max_length=255, blank=True)
    statistic_5_heading = models.CharField(max_length=255, blank=True)
    statistic_5_smallprint = models.CharField(max_length=255, blank=True)

    statistic_6_number = models.CharField(max_length=255, blank=True)
    statistic_6_heading = models.CharField(max_length=255, blank=True)
    statistic_6_smallprint = models.CharField(max_length=255, blank=True)

    section_two_heading = models.CharField(
        max_length=255, verbose_name='High potential industries for UK businesses', blank=True
    )
    section_two_teaser = models.TextField(verbose_name='Summary of the industry opportunities', blank=True)

    # accordion 1
    accordion_1_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Industry Icon',
    )
    accordion_1_title = models.CharField(max_length=255, blank=True, verbose_name='Industry title')
    accordion_1_teaser = models.TextField(blank=True, verbose_name='Industry teaser')
    accordion_1_subsection_1_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 1 icon',
    )
    accordion_1_subsection_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 1 heading')
    accordion_1_subsection_1_body = models.TextField(blank=True, verbose_name='Subsection 1 body')

    accordion_1_subsection_2_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_1_subsection_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_1_subsection_2_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_1_subsection_3_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_1_subsection_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_1_subsection_3_body = models.TextField(blank=True, verbose_name='Subsection 2 body')
    accordion_1_case_study_hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Case study hero',
    )
    accordion_1_case_study_button_text = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button text'
    )
    accordion_1_case_study_button_link = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button link'
    )
    accordion_1_case_study_title = models.CharField(max_length=255, blank=True, verbose_name='Case study title')
    accordion_1_case_study_description = models.CharField(
        max_length=255, blank=True, verbose_name='Case study description'
    )

    accordion_1_statistic_1_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 number')
    accordion_1_statistic_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 heading')
    accordion_1_statistic_1_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 smallprint')

    accordion_1_statistic_2_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 number')
    accordion_1_statistic_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 heading')
    accordion_1_statistic_2_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 smallprint')

    accordion_1_statistic_3_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 number')
    accordion_1_statistic_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 heading')
    accordion_1_statistic_3_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 smallprint')

    accordion_1_statistic_4_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 number')
    accordion_1_statistic_4_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 heading')
    accordion_1_statistic_4_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 smallprint')

    accordion_1_statistic_5_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 number')
    accordion_1_statistic_5_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 heading')
    accordion_1_statistic_5_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 smallprint')

    accordion_1_statistic_6_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 number')
    accordion_1_statistic_6_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 heading')
    accordion_1_statistic_6_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 smallprint')

    # accordion 2
    accordion_2_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Industry Icon',
    )
    accordion_2_title = models.CharField(max_length=255, blank=True, verbose_name='Industry title')
    accordion_2_teaser = models.TextField(blank=True, verbose_name='Industry teaser')
    accordion_2_subsection_1_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 1 icon',
    )
    accordion_2_subsection_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 1 heading')
    accordion_2_subsection_1_body = models.TextField(blank=True, verbose_name='Subsection 1 body')
    accordion_2_subsection_2_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_2_subsection_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_2_subsection_2_body = models.TextField(blank=True, verbose_name='Subsection 2 body')
    accordion_2_subsection_3_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_2_subsection_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_2_subsection_3_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_2_case_study_hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Case study hero',
    )
    accordion_2_case_study_button_text = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button text'
    )
    accordion_2_case_study_button_link = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button link'
    )
    accordion_2_case_study_title = models.CharField(max_length=255, blank=True, verbose_name='Case study title')
    accordion_2_case_study_description = models.CharField(
        max_length=255, blank=True, verbose_name='Case study description'
    )

    accordion_2_statistic_1_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 number')
    accordion_2_statistic_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 heading')
    accordion_2_statistic_1_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 smallprint')

    accordion_2_statistic_2_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 number')
    accordion_2_statistic_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 heading')
    accordion_2_statistic_2_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 smallprint')

    accordion_2_statistic_3_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 number')
    accordion_2_statistic_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 heading')
    accordion_2_statistic_3_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 smallprint')

    accordion_2_statistic_4_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 number')
    accordion_2_statistic_4_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 heading')
    accordion_2_statistic_4_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 smallprint')

    accordion_2_statistic_5_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 number')
    accordion_2_statistic_5_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 heading')
    accordion_2_statistic_5_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 smallprint')

    accordion_2_statistic_6_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 number')
    accordion_2_statistic_6_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 heading')
    accordion_2_statistic_6_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 smallprint')

    # accordion 3
    accordion_3_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Industry Icon',
    )
    accordion_3_title = models.CharField(max_length=255, blank=True, verbose_name='Industry title')
    accordion_3_teaser = models.TextField(blank=True, verbose_name='Industry teaser')
    accordion_3_subsection_1_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 1 icon',
    )
    accordion_3_subsection_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 1 heading')
    accordion_3_subsection_1_body = models.TextField(blank=True, verbose_name='Subsection 1 body')

    accordion_3_subsection_2_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_3_subsection_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_3_subsection_2_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_3_subsection_3_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_3_subsection_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_3_subsection_3_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_3_case_study_hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Case study hero',
    )
    accordion_3_case_study_button_text = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button text'
    )
    accordion_3_case_study_button_link = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button link'
    )
    accordion_3_case_study_title = models.CharField(max_length=255, blank=True, verbose_name='Case study title')
    accordion_3_case_study_description = models.CharField(
        max_length=255, blank=True, verbose_name='Case study description'
    )

    accordion_3_statistic_1_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 number')
    accordion_3_statistic_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 heading')
    accordion_3_statistic_1_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 smallprint')

    accordion_3_statistic_2_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 number')
    accordion_3_statistic_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 heading')
    accordion_3_statistic_2_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 smallprint')

    accordion_3_statistic_3_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 number')
    accordion_3_statistic_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 heading')
    accordion_3_statistic_3_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 smallprint')

    accordion_3_statistic_4_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 number')
    accordion_3_statistic_4_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 heading')
    accordion_3_statistic_4_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 smallprint')

    accordion_3_statistic_5_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 number')
    accordion_3_statistic_5_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 heading')
    accordion_3_statistic_5_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 smallprint')

    accordion_3_statistic_6_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 number')
    accordion_3_statistic_6_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 heading')
    accordion_3_statistic_6_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 smallprint')

    # accordion 4
    accordion_4_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Industry Icon',
    )
    accordion_4_title = models.CharField(max_length=255, blank=True, verbose_name='Industry title')
    accordion_4_teaser = models.TextField(blank=True, verbose_name='Industry teaser')
    accordion_4_subsection_1_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 1 icon',
    )
    accordion_4_subsection_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 1 heading')
    accordion_4_subsection_1_body = models.TextField(blank=True, verbose_name='Subsection 1 body')

    accordion_4_subsection_2_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_4_subsection_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_4_subsection_2_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_4_subsection_3_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_4_subsection_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_4_subsection_3_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_4_case_study_hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Case study hero',
    )
    accordion_4_case_study_button_text = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button text'
    )
    accordion_4_case_study_button_link = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button link'
    )
    accordion_4_case_study_title = models.CharField(max_length=255, blank=True, verbose_name='Case study title')
    accordion_4_case_study_description = models.CharField(
        max_length=255, blank=True, verbose_name='Case study description'
    )

    accordion_4_statistic_1_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 number')
    accordion_4_statistic_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 heading')
    accordion_4_statistic_1_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 smallprint')

    accordion_4_statistic_2_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 number')
    accordion_4_statistic_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 heading')
    accordion_4_statistic_2_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 smallprint')

    accordion_4_statistic_3_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 number')
    accordion_4_statistic_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 heading')
    accordion_4_statistic_3_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 smallprint')

    accordion_4_statistic_4_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 number')
    accordion_4_statistic_4_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 heading')
    accordion_4_statistic_4_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 smallprint')

    accordion_4_statistic_5_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 number')
    accordion_4_statistic_5_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 heading')
    accordion_4_statistic_5_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 smallprint')

    accordion_4_statistic_6_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 number')
    accordion_4_statistic_6_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 heading')
    accordion_4_statistic_6_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 smallprint')

    # accordion 5
    accordion_5_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Industry Icon',
    )
    accordion_5_title = models.CharField(max_length=255, blank=True, verbose_name='Industry title')
    accordion_5_teaser = models.TextField(blank=True, verbose_name='Industry teaser')
    accordion_5_subsection_1_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 1 icon',
    )
    accordion_5_subsection_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 1 heading')
    accordion_5_subsection_1_body = models.TextField(blank=True, verbose_name='Subsection 1 body')

    accordion_5_subsection_2_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_5_subsection_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_5_subsection_2_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_5_subsection_3_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_5_subsection_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_5_subsection_3_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_5_case_study_hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Case study hero',
    )
    accordion_5_case_study_button_text = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button text'
    )
    accordion_5_case_study_button_link = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button link'
    )
    accordion_5_case_study_title = models.CharField(max_length=255, blank=True, verbose_name='Case study title')
    accordion_5_case_study_description = models.CharField(
        max_length=255, blank=True, verbose_name='Case study description'
    )

    accordion_5_statistic_1_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 number')
    accordion_5_statistic_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 heading')
    accordion_5_statistic_1_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 smallprint')

    accordion_5_statistic_2_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 number')
    accordion_5_statistic_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 heading')
    accordion_5_statistic_2_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 smallprint')

    accordion_5_statistic_3_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 number')
    accordion_5_statistic_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 heading')
    accordion_5_statistic_3_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 smallprint')

    accordion_5_statistic_4_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 number')
    accordion_5_statistic_4_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 heading')
    accordion_5_statistic_4_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 smallprint')

    accordion_5_statistic_5_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 number')
    accordion_5_statistic_5_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 heading')
    accordion_5_statistic_5_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 smallprint')

    accordion_5_statistic_6_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 number')
    accordion_5_statistic_6_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 heading')
    accordion_5_statistic_6_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 smallprint')

    # accordion 6
    accordion_6_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Industry Icon',
    )
    accordion_6_title = models.CharField(max_length=255, blank=True, verbose_name='Industry title')
    accordion_6_teaser = models.TextField(blank=True, verbose_name='Industry teaser')
    accordion_6_subsection_1_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 1 icon',
    )
    accordion_6_subsection_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 1 heading')
    accordion_6_subsection_1_body = models.TextField(blank=True, verbose_name='Subsection 1 body')

    accordion_6_subsection_2_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_6_subsection_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_6_subsection_2_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_6_subsection_3_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Subsection 2 icon',
    )
    accordion_6_subsection_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Subsection 2 heading')
    accordion_6_subsection_3_body = models.TextField(blank=True, verbose_name='Subsection 2 body')

    accordion_6_case_study_hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Case study hero',
    )
    accordion_6_case_study_button_text = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button text'
    )
    accordion_6_case_study_button_link = models.CharField(
        max_length=255, blank=True, verbose_name='Case study button link'
    )
    accordion_6_case_study_title = models.CharField(max_length=255, blank=True, verbose_name='Case study title')
    accordion_6_case_study_description = models.CharField(
        max_length=255, blank=True, verbose_name='Case study description'
    )

    accordion_6_statistic_1_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 number')
    accordion_6_statistic_1_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 heading')
    accordion_6_statistic_1_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 1 smallprint')

    accordion_6_statistic_2_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 number')
    accordion_6_statistic_2_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 heading')
    accordion_6_statistic_2_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 2 smallprint')

    accordion_6_statistic_3_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 number')
    accordion_6_statistic_3_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 heading')
    accordion_6_statistic_3_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 3 smallprint')

    accordion_6_statistic_4_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 number')
    accordion_6_statistic_4_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 heading')
    accordion_6_statistic_4_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 4 smallprint')

    accordion_6_statistic_5_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 number')
    accordion_6_statistic_5_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 heading')
    accordion_6_statistic_5_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 5 smallprint')

    accordion_6_statistic_6_number = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 number')
    accordion_6_statistic_6_heading = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 heading')
    accordion_6_statistic_6_smallprint = models.CharField(max_length=255, blank=True, verbose_name='Stat 6 smallprint')

    # fact sheet
    fact_sheet_title = models.CharField(
        max_length=255, blank=True, verbose_name="Title for 'Doing business in' section"
    )
    fact_sheet_teaser = models.CharField(
        max_length=255, blank=True, verbose_name="Summary for 'Doing business in' section"
    )
    fact_sheet_column_1_title = models.CharField(max_length=255, blank=True, verbose_name="Title for 'Tax and customs'")
    fact_sheet_column_1_teaser = models.CharField(
        max_length=255, blank=True, verbose_name="Summary for 'Tax and customs'"
    )
    fact_sheet_column_1_body = MarkdownField(
        blank=True,
        verbose_name="Detailed text for 'Tax and customs'",
        help_text='Use H4 (####) for each sub category heading. ' 'Maximum five sub categories. Aim for 50 words each.',
    )
    fact_sheet_column_2_title = models.CharField(
        max_length=255, blank=True, verbose_name="Title for 'Protecting your business'"
    )
    fact_sheet_column_2_teaser = models.CharField(
        max_length=255, blank=True, verbose_name="Summary for 'Protecting your business'"
    )
    fact_sheet_column_2_body = MarkdownField(
        blank=True,
        verbose_name="Detailed text for 'Protecting your business'",
        help_text='Use H4 (####) for each sub category heading. ' 'Maximum five sub categories. Aim for 50 words each.',
    )

    # need help
    duties_and_custom_procedures_cta_link = models.URLField(
        blank=True, null=True, verbose_name='Check duties and customs procedures for exporting goods'
    )

    # related pages
    related_page_one = models.ForeignKey(
        'wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    related_page_two = models.ForeignKey(
        'wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    related_page_three = models.ForeignKey(
        'wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    tags = ParentalManyToManyField(snippets.IndustryTag, blank=True)
    country = models.ForeignKey(snippets.Country, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')


class ArticlePage(panels.ArticlePagePanels, BaseDomesticPage):

    subpage_types = []

    type_of_article = models.TextField(choices=ARTICLE_TYPES, null=True)

    article_title = models.TextField()
    article_subheading = models.TextField(
        blank=True, help_text="This is a subheading that displays " "below the main title on the article page"
    )
    article_teaser = models.TextField(
        blank=True,
        null=True,
        help_text="This is a subheading that displays when the article " "is featured on another page",
    )
    article_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    article_video = models.ForeignKey(
        'wagtailmedia.Media', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    article_video_transcript = MarkdownField(null=True, blank=True, help_text=VIDEO_TRANSCRIPT_HELP_TEXT)
    article_body_text = MarkdownField()

    cta_title = models.CharField(max_length=255, blank=True, verbose_name='CTA title')
    cta_teaser = models.TextField(blank=True, verbose_name='CTA teaser')

    cta_link_label = models.CharField(max_length=255, blank=True, verbose_name='CTA link label')
    cta_link = models.CharField(max_length=255, blank=True, verbose_name='CTA link')

    related_page_one = models.ForeignKey(
        'export_readiness.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_two = models.ForeignKey(
        'export_readiness.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_three = models.ForeignKey(
        'export_readiness.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    tags = ParentalManyToManyField(snippets.Tag, blank=True)


class ArticleListingPage(panels.ArticleListingPagePanels, BaseDomesticPage):

    subpage_types = [
        'export_readiness.ArticlePage',
    ]

    landing_page_title = models.CharField(max_length=255)

    hero_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    hero_teaser = models.CharField(max_length=255, null=True, blank=True)

    list_teaser = MarkdownField(null=True, blank=True)

    @property
    def articles_count(self):
        return self.get_descendants().type(ArticlePage).live().count()


class CampaignPage(panels.CampaignPagePanels, BaseDomesticPage):

    subpage_types = []

    campaign_heading = models.CharField(max_length=255)
    campaign_hero_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    section_one_heading = models.CharField(max_length=255)
    section_one_intro = MarkdownField()
    section_one_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    selling_point_one_icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    selling_point_one_heading = models.CharField(max_length=255)
    selling_point_one_content = MarkdownField()

    selling_point_two_icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    selling_point_two_heading = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    selling_point_two_content = MarkdownField(null=True, blank=True)

    selling_point_three_icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    selling_point_three_heading = models.CharField(max_length=255, null=True, blank=True)
    selling_point_three_content = MarkdownField(null=True, blank=True)

    section_one_contact_button_url = models.CharField(max_length=255, null=True, blank=True)
    section_one_contact_button_text = models.CharField(max_length=255, null=True, blank=True)

    section_two_heading = models.CharField(max_length=255)
    section_two_intro = MarkdownField()

    section_two_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    section_two_contact_button_url = models.CharField(max_length=255, null=True, blank=True)
    section_two_contact_button_text = models.CharField(max_length=255, null=True, blank=True)

    related_content_heading = models.CharField(max_length=255)
    related_content_intro = MarkdownField()

    related_page_one = models.ForeignKey(
        'export_readiness.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_two = models.ForeignKey(
        'export_readiness.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_three = models.ForeignKey(
        'export_readiness.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    cta_box_message = models.CharField(max_length=255)
    cta_box_button_url = models.CharField(max_length=255)
    cta_box_button_text = models.CharField(max_length=255)
