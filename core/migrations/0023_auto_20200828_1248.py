# Generated by Django 2.2.14 on 2020-08-28 12:48

import core.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail_personalisation.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_detailpage_recap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailpage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock())], icon='fa-font', template='core/personalised_page_struct_paragraph_block.html')), ('video', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('video', wagtail.core.blocks.StructBlock([('width', wagtail.core.blocks.IntegerBlock()), ('height', wagtail.core.blocks.IntegerBlock()), ('video', core.blocks.MediaChooserBlock())]))], icon='fa-play', template='core/personalised_page_struct_video_block.html')), ('content_module', core.blocks.ModularContentStaticBlock()), ('Step', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255)), ('body', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False))], icon='cog')), ('fiction', wagtail.core.blocks.StructBlock([('fiction_body', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('image', core.blocks.ImageBlock(required=False))], icon='fa-commenting-o', template='learn/fictional_company_example.html'))]),
        ),
    ]
