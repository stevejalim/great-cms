from django.forms import CheckboxSelectMultiple, Textarea, Select
from wagtailmedia.widgets import AdminMediaChooser
from wagtail.admin.edit_handlers import (
    HelpPanel,
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    PageChooserPanel,
    TabbedInterface,
)
from wagtail.images.edit_handlers import ImageChooserPanel

from domestic.panels import SearchEngineOptimisationPanel


class BaseInternationalSectorPagePanels:

    content_panels = [
        FieldPanel('title'),
        MultiFieldPanel(
            heading='Heading',
            children=[
                FieldPanel('heading'),
                FieldPanel('sub_heading'),
                ImageChooserPanel('hero_image'),
                FieldPanel('heading_teaser'),
                FieldPanel('featured_description'),
            ],
        ),
        MultiFieldPanel(
            heading='Unique selling points',
            children=[
                HelpPanel(
                    'Use H2 (##) markdown for the three subheadings.'
                    ' Required fields for section to show: 3 Unique Selling '
                    'Points Markdown'
                ),
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
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Statistics',
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
            heading='Spotlight',
            children=[
                FieldPanel('section_two_heading'),
                FieldPanel('section_two_teaser'),
                HelpPanel('Each icon needs a heading for it to show on the page.'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('section_two_subsection_one_icon'),
                                FieldPanel('section_two_subsection_one_heading'),
                                FieldPanel('section_two_subsection_one_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('section_two_subsection_two_icon'),
                                FieldPanel('section_two_subsection_two_heading'),
                                FieldPanel('section_two_subsection_two_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('section_two_subsection_three_icon'),
                                FieldPanel('section_two_subsection_three_heading'),
                                FieldPanel('section_two_subsection_three_body'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Case Study',
            classname='collapsible',
            children=[
                HelpPanel('Required fields for section to show: ' 'Case Study Image, Case Study Title'),
                FieldPanel('case_study_title'),
                FieldPanel('case_study_description'),
                FieldPanel('case_study_cta_text'),
                HelpPanel('Cta\'s require both text and a link to show ' 'on page. '),
                PageChooserPanel(
                    'case_study_cta_page',
                    [
                        'international.InternationalArticlePage',
                        'international.InternationalCampaignPage',
                    ],
                ),
                ImageChooserPanel('case_study_image'),
            ],
        ),
        MultiFieldPanel(
            heading='Fact Sheets',
            classname='collapsible collapsed',
            children=[
                FieldPanel('section_three_heading'),
                FieldPanel('section_three_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('section_three_subsection_one_heading'),
                                FieldPanel('section_three_subsection_one_teaser'),
                                HelpPanel(
                                    'For accessibility reasons, use only '
                                    '"#### [Your text here]" for subheadings '
                                    'in this markdown field'
                                ),
                                FieldPanel('section_three_subsection_one_body'),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('section_three_subsection_two_heading'),
                                FieldPanel('section_three_subsection_two_teaser'),
                                HelpPanel(
                                    'For accessibility reasons, use only '
                                    '"#### [Your text here]" for subheadings '
                                    'in this markdown field'
                                ),
                                FieldPanel('section_three_subsection_two_body'),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        MultiFieldPanel(
            heading='Related articles',
            children=[
                FieldRowPanel(
                    [
                        PageChooserPanel(
                            'related_page_one',
                            [
                                'international.InternationalArticlePage',
                                'international.InternationalCampaignPage',
                            ],
                        ),
                        PageChooserPanel(
                            'related_page_two',
                            [
                                'international.InternationalArticlePage',
                                'international.InternationalCampaignPage',
                            ],
                        ),
                        PageChooserPanel(
                            'related_page_three',
                            [
                                'international.InternationalArticlePage',
                                'international.InternationalCampaignPage',
                            ],
                        ),
                    ]
                )
            ],
        ),
        MultiFieldPanel(
            heading='Project Opportunities',
            classname='collapsible ',
            children=[
                FieldPanel('project_opportunities_title'),
                HelpPanel('Up to 3 random opportunities that are related ' 'to this sector will appear here.'),
                FieldPanel('related_opportunities_cta_text'),
                FieldPanel('related_opportunities_cta_link'),
            ],
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [FieldPanel('slug'), FieldPanel('tags', widget=CheckboxSelectMultiple)]


class InternationalArticlePagePanels:

    content_panels = [
        FieldPanel('title'),
        FieldPanel('article_title'),
        MultiFieldPanel(
            heading='Article content',
            children=[FieldPanel('article_subheading'), FieldPanel('article_teaser'), FieldPanel('article_body_text')],
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
                        PageChooserPanel('related_page_one', 'international.InternationalArticlePage'),
                        PageChooserPanel('related_page_two', 'international.InternationalArticlePage'),
                        PageChooserPanel('related_page_three', 'international.InternationalArticlePage'),
                    ]
                ),
            ],
        ),
        SearchEngineOptimisationPanel(),
    ]

    image_panels = [
        ImageChooserPanel('article_image'),
        FieldPanel('article_video', widget=AdminMediaChooser),
    ]

    settings_panels = [
        FieldPanel('type_of_article', widget=Select),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple),
    ]


class InternationalCampaignPagePanels:

    content_panels = [
        FieldPanel('title'),
        MultiFieldPanel(
            heading='Hero section',
            children=[
                FieldPanel('campaign_heading'),
                FieldPanel('campaign_subheading'),
                FieldPanel('campaign_teaser'),
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
                        PageChooserPanel('related_page_one', 'international.InternationalArticlePage'),
                        PageChooserPanel('related_page_two', 'international.InternationalArticlePage'),
                        PageChooserPanel('related_page_three', 'international.InternationalArticlePage'),
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

    settings_panels = [FieldPanel('slug'), FieldPanel('tags', widget=CheckboxSelectMultiple)]
