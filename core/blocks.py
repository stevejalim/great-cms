from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import AbstractMediaChooserBlock

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from core import models
from core.constants import (
    COUNTRY_TAG_PARAM_NAME,
    HS_TAG_PARAM_NAME,
    RICHTEXT_FEATURES__MINIMAL,
)


class MediaChooserBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        """Render implemented in the VideoBlock, this block shouldn't be used in its own."""
        raise NotImplementedError("MediaChooserBlock Shouldn't be used it's own")


class VideoBlock(blocks.StructBlock):
    width = blocks.IntegerBlock()
    height = blocks.IntegerBlock()
    video = MediaChooserBlock()

    class Meta:
        icon = 'fa-play'


class Item(blocks.StructBlock):
    item = blocks.CharBlock(max_length=255)


class CuratedTopicBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    pages = blocks.ListBlock(blocks.PageChooserBlock(label='Detail page'))

    class Meta:
        template = 'core/curated_topic.html'


class LinkStructValue(blocks.StructValue):
    """
    Generates a URL for blocks with multiple link choices.
    """
    @property
    def url(self):
        page = self.get('internal_link')
        ext = self.get('external_link')
        if page:
            return page.url_path
        else:
            return ext


class LinkBlock(blocks.StructBlock):
    internal_link = blocks.PageChooserBlock(
        required=False,
        label='Internal link',
    )
    external_link = blocks.CharBlock(
        required=False,
        max_length=255,
        label='External link',
    )

    class Meta:
        value_class = LinkStructValue
        icon = 'redirect'


class TitleBlock(blocks.CharBlock):
    class Meta:
        max_length = 255
        help_text = 'Enter a title'
        template = 'core/includes/_title.html'
        icon = 'bold'


class HrBlock(blocks.StaticBlock):
    # A horizontal full-width line
    class Meta:
        help_text = 'Horizontal rule'
        template = 'core/includes/_hr.html'
        icon = 'horizontalrule'


class ImageBlock(ImageChooserBlock):
    class Meta:
        help_text = 'Include an image'
        template = 'core/includes/_image.html'
        icon = 'image'


class SimpleVideoBlock(blocks.StructBlock):
    video = MediaChooserBlock()

    class Meta:
        help_text = 'Include a video'
        template = 'core/includes/_hero_video.html'
        icon = 'fa-play'


class ButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=255)
    link = LinkBlock(required=False)

    class Meta:
        template = 'core/button.html'
        icon = 'radio-full'


class RouteSectionBlock(blocks.StructBlock):
    # One of the three intro blocks at the top of the domestic dashboard
    route_type = blocks.ChoiceBlock(choices=[
        ('learn', 'Learning'),
        ('plan', 'Export plan'),
        ('target', 'Target market'),
    ], icon='redirect')
    title = blocks.CharBlock(max_length=255)
    body = blocks.TextBlock(max_length=4096)
    image = ImageChooserBlock()
    button = ButtonBlock(icon='cog', required=False)

    class Meta:
        help_text = 'The routing block at the top of the dashboard. There should be three - learn, target, plan'
        template = 'core/includes/_route-section.html'
        icon = 'redirect'


class SidebarLinkBlock(blocks.StructBlock):
    # a link to a learning page in the RH column
    link = LinkBlock(required=True)
    title_override = blocks.CharBlock(max_length=255, required=False)
    lede_override = blocks.CharBlock(max_length=255, required=False)

    def render(self, value, context={}):
        try:
            internal_link = value['link']['internal_link']
            value['target_lede'] = internal_link.get_parent() and internal_link.get_parent().title
            value['target_title'] = internal_link.title
            # If it's a detail page, get the read duration
            if isinstance(internal_link.specific, models.DetailPage):
                detail_page = (internal_link.specific.__class__.objects.get(id=internal_link.id))
                value['read_time'] = getattr(detail_page, 'estimated_read_duration')
        except (ObjectDoesNotExist, KeyError, TypeError, AttributeError):
            pass

        return super().render(value, context=context)

    class Meta:
        help_text = 'A floating link in a section to the right of the content. Labels can be overridden.'
        template = 'core/includes/_sidebar-link.html'
        icon = 'tag'


class ComponentTargetTable(blocks.StaticBlock):
    # This is a dummy block to show the principal of components
    class Meta:
        help_text = 'Target section table for marketing approach page'
        template = 'core/includes/_target_table.html'
        icon = 'grip'


class SectionBlock(blocks.StreamBlock):
    # a section in generic layout 1:2 columns
    title = TitleBlock()
    text_block = blocks.RichTextBlock(icon='openquote', helptext='Add a textblock')
    image = ImageBlock()
    hr = HrBlock()
    #  Components
    side_link = SidebarLinkBlock()
    target_table = ComponentTargetTable()

    class Meta:
        help_text = 'A 1:2 column section'
        template = 'core/includes/_section.html'
        icon = 'placeholder'


class ModularContentStaticBlock(blocks.StaticBlock):

    class Meta:
        admin_text = 'Content modules will be automatically displayed, no configuration needed.'
        icon = 'fa-archive'
        template = 'core/cs_block.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        if 'tags' in context['request'].GET:
            from core.models import ContentModule

            tags = context['request'].GET['tags'].split(',')
            context['modules'] = ContentModule.objects.filter(tags__name__in=tags).distinct()
        return context


class StepByStepBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    body = blocks.RichTextBlock()
    image = ImageChooserBlock(required=False)

    class Meta:
        template = 'learn/step_by_step.html'


class ITAQuoteBlock(blocks.StructBlock):
    quote = blocks.RichTextBlock()
    author = blocks.CharBlock(max_length=255)

    class Meta:
        template = 'learn/ita_quote.html'


class ChooseDoNotChooseBlock(blocks.StructBlock):
    choose_title = blocks.CharBlock(max_length=255)
    choose_body = blocks.RichTextBlock(features=RICHTEXT_FEATURES__MINIMAL)

    do_not_choose_title = blocks.CharBlock(max_length=255)
    do_not_choose_body = blocks.RichTextBlock(features=RICHTEXT_FEATURES__MINIMAL)

    class Meta:
        help_text = (
            'A pair of custom rich-text areas with titles, '
            'one for Choose and the other for Do Not Choose'
        )
        icon = 'fa-question-circle'
        template = 'learn/choose_do_not_choose.html'


class CaseStudyStaticBlock(blocks.StaticBlock):

    class Meta:
        admin_text = (
            'Case Studies are automatically displayed based on '
            'personalisation rules; no configuration needed beyond '
            'adding this block to the page.'
        )
        icon = 'fa-book'
        template = 'core/blocks/case_study.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(
            value,
            parent_context=parent_context
        )

        # CURRENTLY we get tag values from the querystring, but this will
        # change when we hook into personalisation. For now, testers will
        # need to provide `?hs-tag=Y&country-tag=X` or `?hs-tag=Y` or
        # `?country-tag=X` to get the case study logic to work.

        hs_tags = context['request'].GET.get(
            HS_TAG_PARAM_NAME, ''
        ).split(',')

        country_tags = context['request'].GET.get(
            COUNTRY_TAG_PARAM_NAME, ''
        ).split(',')

        if hs_tags or country_tags:

            hs_tags_q = Q(hs_code_tags__name__in=hs_tags)
            country_tags_q = Q(country_code_tags__name__in=country_tags)

            case_study = models.CaseStudy.objects.filter(
                hs_tags_q | country_tags_q
            ).distinct().first()

            context['case_study'] = case_study
        return context
