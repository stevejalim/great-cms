from django.db import models

from modelcluster.fields import ParentalManyToManyField

from core.constants import ARTICLE_TYPES

from export_readiness import snippets
from export_readiness.models import BasePage, MarkdownField
from . import panels


class BaseInternationalPage(BasePage):
    # service_name_value = 'GREAT_INTERNATIONAL'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # self.uses_tree_based_routing = True
        return super().save(*args, **kwargs)


class BaseInternationalSectorPage(panels.BaseInternationalSectorPagePanels, BaseInternationalPage):
    class Meta:
        abstract = True

    parent_page_types = [
        'core.LandingPage',
        'domestic.DomesticHomePage',
        # 'great_international.InternationalTopicLandingPage'
    ]
    subpage_types = []

    tags = ParentalManyToManyField(snippets.Tag, blank=True)

    heading = models.CharField(max_length=255, verbose_name='Sector name')
    sub_heading = models.TextField(blank=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    heading_teaser = models.TextField(blank=True, verbose_name='Introduction')
    featured_description = models.TextField(
        blank=True,
        help_text="This is the description shown when the sector "
        "is featured on another page i.e. the Invest Home Page",
    )

    section_one_body = MarkdownField(null=True, verbose_name='3 unique selling points markdown', blank=True)
    section_one_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Image for unique selling points',
        blank=True,
    )
    section_one_image_caption = models.CharField(max_length=255, blank=True, verbose_name='Image caption')
    section_one_image_caption_company = models.CharField(
        max_length=255, blank=True, verbose_name='Image caption attribution'
    )

    statistic_1_number = models.CharField(max_length=255, blank=True)
    statistic_1_heading = models.CharField(max_length=255, blank=True)
    statistic_1_smallprint = models.CharField(max_length=255, blank=True)

    statistic_2_number = models.CharField(max_length=255, blank=True)
    statistic_2_heading = models.CharField(max_length=255, blank=True)
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

    section_two_heading = models.CharField(max_length=255, verbose_name='Spotlight', blank=True)
    section_two_teaser = models.TextField(verbose_name='Spotlight summary', blank=True)

    section_two_subsection_one_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Spotlight 1 icon',
    )
    section_two_subsection_one_heading = models.CharField(
        max_length=255, verbose_name='Spotlight 1 heading', blank=True
    )
    section_two_subsection_one_body = models.TextField(verbose_name='Spotlight 1 body', blank=True)

    section_two_subsection_two_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Spotlight 2 icon',
    )
    section_two_subsection_two_heading = models.CharField(
        max_length=255, verbose_name='Spotlight 2 heading', blank=True
    )
    section_two_subsection_two_body = models.TextField(verbose_name='Spotlight 2 body', blank=True)

    section_two_subsection_three_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Spotlight 3 icon',
    )
    section_two_subsection_three_heading = models.CharField(
        max_length=255, verbose_name='Spotlight 3 heading', blank=True
    )
    section_two_subsection_three_body = models.TextField(verbose_name='Spotlight 3 body', blank=True)

    case_study_title = models.CharField(max_length=255, blank=True)
    case_study_description = models.TextField(blank=True)
    case_study_cta_text = models.TextField(blank=True, verbose_name='Case study link text')
    case_study_cta_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Case study link URL',
    )
    case_study_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    section_three_heading = models.CharField(max_length=255, blank=True, verbose_name='Fact sheets heading')
    section_three_teaser = models.TextField(blank=True, verbose_name='Fact sheets teaser')

    section_three_subsection_one_heading = models.CharField(
        max_length=255, blank=True, verbose_name='Fact sheet 1 heading'
    )
    section_three_subsection_one_teaser = models.TextField(blank=True, verbose_name='Fact sheet 1 teaser')
    section_three_subsection_one_body = MarkdownField(blank=True, null=True, verbose_name='Fact sheet 1 body')

    section_three_subsection_two_heading = models.CharField(
        max_length=255, blank=True, verbose_name='Fact sheet 2 heading'
    )
    section_three_subsection_two_teaser = models.TextField(blank=True, verbose_name='Fact sheet 2 teaser')
    section_three_subsection_two_body = MarkdownField(blank=True, null=True, verbose_name='Fact sheet 2 body')

    related_page_one = models.ForeignKey(
        'wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    related_page_two = models.ForeignKey(
        'wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    related_page_three = models.ForeignKey(
        'wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    project_opportunities_title = models.CharField(max_length=255, blank=True)
    related_opportunities_cta_text = models.CharField(max_length=255, blank=True)
    related_opportunities_cta_link = models.CharField(max_length=255, blank=True)


class InternationalSectorPage(BaseInternationalSectorPage):
    class Meta:
        ordering = ['-heading']

    template = "international_sector_page.html"

    parent_page_types = [
        'core.LandingPage',
        'domestic.DomesticHomePage',
        # 'great_international.InternationalTopicLandingPage'
    ]

    @classmethod
    def allowed_subpage_models(cls):
        return [InternationalSubSectorPage, InternationalArticlePage]


class InternationalSubSectorPage(BaseInternationalSectorPage):

    parent_page_types = ['great_international.InternationalSectorPage']


class InternationalArticlePage(panels.InternationalArticlePagePanels, BaseInternationalPage):
    parent_page_types = [
        'core.LandingPage',
        'domestic.DomesticHomePage',
    ]
    subpage_types = []

    type_of_article = models.TextField(choices=ARTICLE_TYPES, null=True)

    article_title = models.TextField()
    article_subheading = models.TextField(
        blank=True, help_text="This is a subheading that displays " "below the main title on the article page"
    )
    article_teaser = models.TextField(
        blank=True, help_text="This is a subheading that displays when the article " "is featured on another page"
    )
    article_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    article_video = models.ForeignKey(
        'wagtailmedia.Media', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    article_body_text = MarkdownField()

    cta_title = models.CharField(max_length=255, blank=True, verbose_name='CTA title')
    cta_teaser = models.TextField(blank=True, verbose_name='CTA teaser')

    cta_link_label = models.CharField(max_length=255, blank=True, verbose_name='CTA link label')
    cta_link = models.CharField(max_length=255, blank=True, verbose_name='CTA link')

    related_page_one = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_two = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_three = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    tags = ParentalManyToManyField(snippets.Tag, blank=True)


class InternationalCampaignPage(panels.InternationalCampaignPagePanels, BaseInternationalPage):
    parent_page_types = [
        'core.LandingPage',
        'domestic.DomesticHomePage',
        # 'great_international.InternationalArticleListingPage',
        # 'great_international.InternationalTopicLandingPage',
    ]
    subpage_types = ['great_international.InternationalArticlePage']
    view_path = 'campaigns/'

    campaign_subheading = models.CharField(
        max_length=255,
        blank=True,
        help_text="This is a subheading that displays " "when the article is featured on another page",
    )
    campaign_teaser = models.CharField(max_length=255, null=True, blank=True)
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
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_two = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_three = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    cta_box_message = models.CharField(max_length=255)
    cta_box_button_url = models.CharField(max_length=255)
    cta_box_button_text = models.CharField(max_length=255)

    tags = ParentalManyToManyField(snippets.Tag, blank=True)
