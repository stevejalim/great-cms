from django.forms import CheckboxSelectMultiple, Textarea, Select

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    PageChooserPanel,
    HelpPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmedia.widgets import AdminMediaChooser


class SearchEngineOptimisationPanel(MultiFieldPanel):
    default_heading = 'Search Engine Optimisation'
    default_children = [
        FieldPanel('seo_title'),
        FieldPanel('search_description'),
    ]

    def __init__(self, children=default_children, heading=default_heading, *args, **kwargs):
        super().__init__(*args, children=children, heading=heading, **kwargs)


ACCORDION_FIELDS_HELP_TEXT = (
    'To be displayed, this industry needs at least: a title, a teaser, '
    '2 bullet points, and 2 calls to action (CTAs).'
)


class CountryGuidePagePanels:

    content_panels = [
        MultiFieldPanel(
            heading='Heading and introduction',
            children=[
                FieldPanel('heading'),
                FieldPanel('sub_heading'),
                ImageChooserPanel('hero_image'),
                FieldPanel('heading_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('intro_cta_one_link'),
                                FieldPanel('intro_cta_one_title'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('intro_cta_two_link'),
                                FieldPanel('intro_cta_two_title'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('intro_cta_three_link'),
                                FieldPanel('intro_cta_three_title'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Unique selling points of the market for UK exporters',
            children=[
                FieldRowPanel(
                    [
                        FieldPanel('section_one_body'),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('section_one_image'),
                                FieldPanel('section_one_image_caption'),
                                FieldPanel('section_one_image_caption_company'),
                            ]
                        ),
                    ]
                )
            ],
        ),
        MultiFieldPanel(
            heading='Statistics',
            classname='collapsible',
            children=[
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_1_number'),
                                FieldPanel('statistic_1_heading'),
                                FieldPanel('statistic_1_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_2_number'),
                                FieldPanel('statistic_2_heading'),
                                FieldPanel('statistic_2_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_3_number'),
                                FieldPanel('statistic_3_heading'),
                                FieldPanel('statistic_3_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_4_number'),
                                FieldPanel('statistic_4_heading'),
                                FieldPanel('statistic_4_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_5_number'),
                                FieldPanel('statistic_5_heading'),
                                FieldPanel('statistic_5_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_6_number'),
                                FieldPanel('statistic_6_heading'),
                                FieldPanel('statistic_6_smallprint'),
                            ]
                        ),
                    ]
                )
            ],
        ),
        MultiFieldPanel(
            heading='Highlights', children=[FieldPanel('section_two_heading'), FieldPanel('section_two_teaser')]
        ),
        MultiFieldPanel(
            heading='Industry one',
            classname='collapsible collapsed',
            children=[
                HelpPanel(content=ACCORDION_FIELDS_HELP_TEXT, classname='help-panel-font-large'),
                ImageChooserPanel('accordion_1_icon'),
                FieldPanel('accordion_1_title'),
                FieldPanel('accordion_1_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_1_subsection_1_icon'),
                                FieldPanel('accordion_1_subsection_1_heading'),
                                FieldPanel('accordion_1_subsection_1_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_1_subsection_2_icon'),
                                FieldPanel('accordion_1_subsection_2_heading'),
                                FieldPanel('accordion_1_subsection_2_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_1_subsection_3_icon'),
                                FieldPanel('accordion_1_subsection_3_heading'),
                                FieldPanel('accordion_1_subsection_3_body'),
                            ]
                        ),
                    ]
                ),
                MultiFieldPanel(
                    [
                        ImageChooserPanel('accordion_1_case_study_hero_image'),
                        FieldPanel('accordion_1_case_study_button_text'),
                        FieldPanel('accordion_1_case_study_button_link'),
                        FieldPanel('accordion_1_case_study_title'),
                        FieldPanel('accordion_1_case_study_description'),
                    ]
                ),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_1_statistic_1_number'),
                                FieldPanel('accordion_1_statistic_1_heading'),
                                FieldPanel('accordion_1_statistic_1_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_1_statistic_2_number'),
                                FieldPanel('accordion_1_statistic_2_heading'),
                                FieldPanel('accordion_1_statistic_2_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_1_statistic_3_number'),
                                FieldPanel('accordion_1_statistic_3_heading'),
                                FieldPanel('accordion_1_statistic_3_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_1_statistic_4_number'),
                                FieldPanel('accordion_1_statistic_4_heading'),
                                FieldPanel('accordion_1_statistic_4_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_1_statistic_5_number'),
                                FieldPanel('accordion_1_statistic_5_heading'),
                                FieldPanel('accordion_1_statistic_5_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_1_statistic_6_number'),
                                FieldPanel('accordion_1_statistic_6_heading'),
                                FieldPanel('accordion_1_statistic_6_smallprint'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Industry two',
            classname='collapsible collapsed',
            children=[
                HelpPanel(content=ACCORDION_FIELDS_HELP_TEXT, classname='help-panel-font-large'),
                ImageChooserPanel('accordion_2_icon'),
                FieldPanel('accordion_2_title'),
                FieldPanel('accordion_2_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_2_subsection_1_icon'),
                                FieldPanel('accordion_2_subsection_1_heading'),
                                FieldPanel('accordion_2_subsection_1_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_2_subsection_2_icon'),
                                FieldPanel('accordion_2_subsection_2_heading'),
                                FieldPanel('accordion_2_subsection_2_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_2_subsection_3_icon'),
                                FieldPanel('accordion_2_subsection_3_heading'),
                                FieldPanel('accordion_2_subsection_3_body'),
                            ]
                        ),
                    ]
                ),
                MultiFieldPanel(
                    [
                        ImageChooserPanel('accordion_2_case_study_hero_image'),
                        FieldPanel('accordion_2_case_study_button_text'),
                        FieldPanel('accordion_2_case_study_button_link'),
                        FieldPanel('accordion_2_case_study_title'),
                        FieldPanel('accordion_2_case_study_description'),
                    ]
                ),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_2_statistic_1_number'),
                                FieldPanel('accordion_2_statistic_1_heading'),
                                FieldPanel('accordion_2_statistic_1_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_2_statistic_2_number'),
                                FieldPanel('accordion_2_statistic_2_heading'),
                                FieldPanel('accordion_2_statistic_2_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_2_statistic_3_number'),
                                FieldPanel('accordion_2_statistic_3_heading'),
                                FieldPanel('accordion_2_statistic_3_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_2_statistic_4_number'),
                                FieldPanel('accordion_2_statistic_4_heading'),
                                FieldPanel('accordion_2_statistic_4_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_2_statistic_5_number'),
                                FieldPanel('accordion_2_statistic_5_heading'),
                                FieldPanel('accordion_2_statistic_5_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_2_statistic_6_number'),
                                FieldPanel('accordion_2_statistic_6_heading'),
                                FieldPanel('accordion_2_statistic_6_smallprint'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Industry three',
            classname='collapsible collapsed',
            children=[
                HelpPanel(content=ACCORDION_FIELDS_HELP_TEXT, classname='help-panel-font-large'),
                ImageChooserPanel('accordion_3_icon'),
                FieldPanel('accordion_3_title'),
                FieldPanel('accordion_3_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_3_subsection_1_icon'),
                                FieldPanel('accordion_3_subsection_1_heading'),
                                FieldPanel('accordion_3_subsection_1_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_3_subsection_2_icon'),
                                FieldPanel('accordion_3_subsection_2_heading'),
                                FieldPanel('accordion_3_subsection_2_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_3_subsection_3_icon'),
                                FieldPanel('accordion_3_subsection_3_heading'),
                                FieldPanel('accordion_3_subsection_3_body'),
                            ]
                        ),
                    ]
                ),
                MultiFieldPanel(
                    [
                        ImageChooserPanel('accordion_3_case_study_hero_image'),
                        FieldPanel('accordion_3_case_study_button_text'),
                        FieldPanel('accordion_3_case_study_button_link'),
                        FieldPanel('accordion_3_case_study_title'),
                        FieldPanel('accordion_3_case_study_description'),
                    ]
                ),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_3_statistic_1_number'),
                                FieldPanel('accordion_3_statistic_1_heading'),
                                FieldPanel('accordion_3_statistic_1_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_3_statistic_2_number'),
                                FieldPanel('accordion_3_statistic_2_heading'),
                                FieldPanel('accordion_3_statistic_2_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_3_statistic_3_number'),
                                FieldPanel('accordion_3_statistic_3_heading'),
                                FieldPanel('accordion_3_statistic_3_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_3_statistic_4_number'),
                                FieldPanel('accordion_3_statistic_4_heading'),
                                FieldPanel('accordion_3_statistic_4_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_3_statistic_5_number'),
                                FieldPanel('accordion_3_statistic_5_heading'),
                                FieldPanel('accordion_3_statistic_5_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_3_statistic_6_number'),
                                FieldPanel('accordion_3_statistic_6_heading'),
                                FieldPanel('accordion_3_statistic_6_smallprint'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Industry four',
            classname='collapsible collapsed',
            children=[
                HelpPanel(content=ACCORDION_FIELDS_HELP_TEXT, classname='help-panel-font-large'),
                ImageChooserPanel('accordion_4_icon'),
                FieldPanel('accordion_4_title'),
                FieldPanel('accordion_4_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_4_subsection_1_icon'),
                                FieldPanel('accordion_4_subsection_1_heading'),
                                FieldPanel('accordion_4_subsection_1_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_4_subsection_2_icon'),
                                FieldPanel('accordion_4_subsection_2_heading'),
                                FieldPanel('accordion_4_subsection_2_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_4_subsection_3_icon'),
                                FieldPanel('accordion_4_subsection_3_heading'),
                                FieldPanel('accordion_4_subsection_3_body'),
                            ]
                        ),
                    ]
                ),
                MultiFieldPanel(
                    [
                        ImageChooserPanel('accordion_4_case_study_hero_image'),
                        FieldPanel('accordion_4_case_study_button_text'),
                        FieldPanel('accordion_4_case_study_button_link'),
                        FieldPanel('accordion_4_case_study_title'),
                        FieldPanel('accordion_4_case_study_description'),
                    ]
                ),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_4_statistic_1_number'),
                                FieldPanel('accordion_4_statistic_1_heading'),
                                FieldPanel('accordion_4_statistic_1_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_4_statistic_2_number'),
                                FieldPanel('accordion_4_statistic_2_heading'),
                                FieldPanel('accordion_4_statistic_2_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_4_statistic_3_number'),
                                FieldPanel('accordion_4_statistic_3_heading'),
                                FieldPanel('accordion_4_statistic_3_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_4_statistic_4_number'),
                                FieldPanel('accordion_4_statistic_4_heading'),
                                FieldPanel('accordion_4_statistic_4_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_4_statistic_5_number'),
                                FieldPanel('accordion_4_statistic_5_heading'),
                                FieldPanel('accordion_4_statistic_5_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_4_statistic_6_number'),
                                FieldPanel('accordion_4_statistic_6_heading'),
                                FieldPanel('accordion_4_statistic_6_smallprint'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Industry five',
            classname='collapsible collapsed',
            children=[
                HelpPanel(content=ACCORDION_FIELDS_HELP_TEXT, classname='help-panel-font-large'),
                ImageChooserPanel('accordion_5_icon'),
                FieldPanel('accordion_5_title'),
                FieldPanel('accordion_5_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_5_subsection_1_icon'),
                                FieldPanel('accordion_5_subsection_1_heading'),
                                FieldPanel('accordion_5_subsection_1_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_5_subsection_2_icon'),
                                FieldPanel('accordion_5_subsection_2_heading'),
                                FieldPanel('accordion_5_subsection_2_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_5_subsection_3_icon'),
                                FieldPanel('accordion_5_subsection_3_heading'),
                                FieldPanel('accordion_5_subsection_3_body'),
                            ]
                        ),
                    ]
                ),
                MultiFieldPanel(
                    [
                        ImageChooserPanel('accordion_4_case_study_hero_image'),
                        FieldPanel('accordion_5_case_study_button_text'),
                        FieldPanel('accordion_5_case_study_button_link'),
                        FieldPanel('accordion_5_case_study_title'),
                        FieldPanel('accordion_5_case_study_description'),
                    ]
                ),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_5_statistic_1_number'),
                                FieldPanel('accordion_5_statistic_1_heading'),
                                FieldPanel('accordion_5_statistic_1_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_5_statistic_2_number'),
                                FieldPanel('accordion_5_statistic_2_heading'),
                                FieldPanel('accordion_5_statistic_2_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_5_statistic_3_number'),
                                FieldPanel('accordion_5_statistic_3_heading'),
                                FieldPanel('accordion_5_statistic_3_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_5_statistic_4_number'),
                                FieldPanel('accordion_5_statistic_4_heading'),
                                FieldPanel('accordion_5_statistic_4_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_5_statistic_5_number'),
                                FieldPanel('accordion_5_statistic_5_heading'),
                                FieldPanel('accordion_5_statistic_5_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_5_statistic_6_number'),
                                FieldPanel('accordion_5_statistic_6_heading'),
                                FieldPanel('accordion_5_statistic_6_smallprint'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Industry six',
            classname='collapsible collapsed',
            children=[
                HelpPanel(content=ACCORDION_FIELDS_HELP_TEXT, classname='help-panel-font-large'),
                ImageChooserPanel('accordion_6_icon'),
                FieldPanel('accordion_6_title'),
                FieldPanel('accordion_6_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_6_subsection_1_icon'),
                                FieldPanel('accordion_6_subsection_1_heading'),
                                FieldPanel('accordion_6_subsection_1_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_6_subsection_2_icon'),
                                FieldPanel('accordion_6_subsection_2_heading'),
                                FieldPanel('accordion_6_subsection_2_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('accordion_6_subsection_3_icon'),
                                FieldPanel('accordion_6_subsection_3_heading'),
                                FieldPanel('accordion_6_subsection_3_body'),
                            ]
                        ),
                    ]
                ),
                MultiFieldPanel(
                    [
                        ImageChooserPanel('accordion_6_case_study_hero_image'),
                        FieldPanel('accordion_6_case_study_button_text'),
                        FieldPanel('accordion_6_case_study_button_link'),
                        FieldPanel('accordion_6_case_study_title'),
                        FieldPanel('accordion_6_case_study_description'),
                    ]
                ),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_6_statistic_1_number'),
                                FieldPanel('accordion_6_statistic_1_heading'),
                                FieldPanel('accordion_6_statistic_1_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_6_statistic_2_number'),
                                FieldPanel('accordion_6_statistic_2_heading'),
                                FieldPanel('accordion_6_statistic_2_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_6_statistic_3_number'),
                                FieldPanel('accordion_6_statistic_3_heading'),
                                FieldPanel('accordion_6_statistic_3_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_6_statistic_4_number'),
                                FieldPanel('accordion_6_statistic_4_heading'),
                                FieldPanel('accordion_6_statistic_4_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_6_statistic_5_number'),
                                FieldPanel('accordion_6_statistic_5_heading'),
                                FieldPanel('accordion_6_statistic_5_smallprint'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('accordion_6_statistic_6_number'),
                                FieldPanel('accordion_6_statistic_6_heading'),
                                FieldPanel('accordion_6_statistic_6_smallprint'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Fact sheet',
            classname='collapsible',
            children=[
                FieldPanel('fact_sheet_title'),
                FieldPanel('fact_sheet_teaser'),
                FieldRowPanel(
                    [
                        FieldPanel('fact_sheet_column_1_title'),
                        FieldPanel('fact_sheet_column_1_teaser'),
                        FieldPanel('fact_sheet_column_1_body'),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel('fact_sheet_column_2_title'),
                        FieldPanel('fact_sheet_column_2_teaser'),
                        FieldPanel('fact_sheet_column_2_body'),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Need help', classname='collapsible', children=[FieldPanel('duties_and_custom_procedures_cta_link')]
        ),
        MultiFieldPanel(
            heading='News and events',
            children=[
                FieldRowPanel(
                    [
                        PageChooserPanel(
                            'related_page_one',
                            [
                                'export_readiness.ArticlePage',
                                'export_readiness.CampaignPage',
                                'export_readiness.ArticleListingPage',
                            ],
                        ),
                        PageChooserPanel(
                            'related_page_two',
                            [
                                'export_readiness.ArticlePage',
                                'export_readiness.CampaignPage',
                                'export_readiness.ArticleListingPage',
                            ],
                        ),
                        PageChooserPanel(
                            'related_page_three',
                            [
                                'export_readiness.ArticlePage',
                                'export_readiness.CampaignPage',
                                'export_readiness.ArticleListingPage',
                            ],
                        ),
                    ]
                )
            ],
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple),
        FieldPanel('country'),
    ]


class CampaignPagePanels:

    content_panels = [
        MultiFieldPanel(
            heading='Hero section',
            children=[
                FieldPanel('campaign_heading'),
                ImageChooserPanel('campaign_hero_image'),
            ],
        ),
        MultiFieldPanel(
            heading='Section one',
            children=[
                FieldPanel('section_one_heading'),
                FieldPanel('section_one_intro'),
                ImageChooserPanel('section_one_image'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            children=[
                                ImageChooserPanel('selling_point_one_icon'),
                                FieldPanel('selling_point_one_heading'),
                                FieldPanel('selling_point_one_content'),
                            ]
                        ),
                        MultiFieldPanel(
                            children=[
                                ImageChooserPanel('selling_point_two_icon'),
                                FieldPanel('selling_point_two_heading'),
                                FieldPanel('selling_point_two_content'),
                            ]
                        ),
                        MultiFieldPanel(
                            children=[
                                ImageChooserPanel('selling_point_three_icon'),
                                FieldPanel('selling_point_three_heading'),
                                FieldPanel('selling_point_three_content'),
                            ]
                        ),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel('section_one_contact_button_text'),
                        FieldPanel('section_one_contact_button_url'),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Section two',
            children=[
                FieldPanel('section_two_heading'),
                FieldPanel('section_two_intro'),
                ImageChooserPanel('section_two_image'),
                FieldRowPanel(
                    [
                        FieldPanel('section_two_contact_button_text'),
                        FieldPanel('section_two_contact_button_url'),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Related content section',
            children=[
                FieldPanel('related_content_heading'),
                FieldPanel('related_content_intro'),
                FieldRowPanel(
                    [
                        PageChooserPanel('related_page_one', 'export_readiness.ArticlePage'),
                        PageChooserPanel('related_page_two', 'export_readiness.ArticlePage'),
                        PageChooserPanel('related_page_three', 'export_readiness.ArticlePage'),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Contact box',
            children=[
                FieldRowPanel(
                    [
                        FieldPanel('cta_box_message', widget=Textarea),
                        MultiFieldPanel(
                            [
                                FieldPanel('cta_box_button_url'),
                                FieldPanel('cta_box_button_text'),
                            ]
                        ),
                    ]
                )
            ],
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
    ]


class ArticlePagePanels:

    content_panels = [
        FieldPanel('article_title'),
        MultiFieldPanel(
            heading='Article content',
            children=[
                FieldPanel('article_subheading'),
                FieldPanel('article_teaser'),
                ImageChooserPanel('article_image'),
                FieldPanel('article_video', widget=AdminMediaChooser),
                FieldPanel('article_video_transcript'),
                FieldPanel('article_body_text'),
            ],
        ),
        MultiFieldPanel(
            heading='CTA fields',
            children=[
                FieldPanel('cta_title'),
                FieldPanel('cta_teaser'),
                FieldPanel('cta_link_label'),
                FieldPanel('cta_link'),
            ],
        ),
        MultiFieldPanel(
            heading='Related articles',
            children=[
                FieldRowPanel(
                    [
                        PageChooserPanel('related_page_one', 'export_readiness.ArticlePage'),
                        PageChooserPanel('related_page_two', 'export_readiness.ArticlePage'),
                        PageChooserPanel('related_page_three', 'export_readiness.ArticlePage'),
                    ]
                ),
            ],
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('type_of_article', widget=Select),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple),
    ]


class MarketingArticlePagePanels:

    content_panels = [
        FieldPanel('article_title'),
        MultiFieldPanel(
            heading='Article content',
            children=[
                FieldPanel('article_teaser'),
                ImageChooserPanel('article_image'),
                FieldPanel('article_body_text'),
            ],
        ),
        MultiFieldPanel(
            heading='CTA fields',
            children=[
                FieldPanel('cta_title'),
                FieldPanel('cta_teaser'),
                FieldPanel('cta_link_label'),
                FieldPanel('cta_link'),
            ],
        ),
        MultiFieldPanel(
            heading='Related articles',
            children=[
                FieldRowPanel(
                    [
                        PageChooserPanel('related_page_one', 'export_readiness.ArticlePage'),
                        PageChooserPanel('related_page_two', 'export_readiness.ArticlePage'),
                        PageChooserPanel('related_page_three', 'export_readiness.ArticlePage'),
                    ]
                ),
            ],
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple),
    ]


class ArticleListingPagePanels:

    content_panels = [
        FieldPanel('landing_page_title'),
        MultiFieldPanel(heading='Hero', children=[ImageChooserPanel('hero_image'), FieldPanel('hero_teaser')]),
        FieldPanel('list_teaser'),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
    ]
