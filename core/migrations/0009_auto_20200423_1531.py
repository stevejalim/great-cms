# Generated by Django 2.2.10 on 2020-04-23 15:31

import core.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail_personalisation.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200408_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailpage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock())], icon='pilcrow', template='core/personalised_page_struct_paragraph_block.html')), ('video', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('video', wagtail.core.blocks.StructBlock([('width', wagtail.core.blocks.IntegerBlock()), ('height', wagtail.core.blocks.IntegerBlock()), ('video', core.blocks.MediaChooserBlock())]))], icon='media'))]),
        ),
        migrations.AlterField(
            model_name='listpage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock())], icon='pilcrow', template='core/personalised_page_struct_paragraph_block.html')), ('video', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('video', wagtail.core.blocks.StructBlock([('width', wagtail.core.blocks.IntegerBlock()), ('height', wagtail.core.blocks.IntegerBlock()), ('video', core.blocks.MediaChooserBlock())]))], icon='media'))]),
        ),
    ]