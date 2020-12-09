# Generated by Django 2.2.10 on 2020-03-17 17:25

import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail_personalisation.blocks
import wagtail_personalisation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtail_personalisation', '0025_auto_20190822_0627'),
        ('core', '0004_country_product'),
        ('learn', '0002_delete_lessonpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('generic_content', wagtail.core.fields.StreamField([('generic_content', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock())], icon='pilcrow'))])),
                ('country_specific_content', wagtail.core.fields.StreamField([('country_specific_content', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock())], icon='pilcrow'))])),
                ('product_specific_content', wagtail.core.fields.StreamField([('product_specific_content', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock())], icon='pilcrow'))])),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(wagtail_personalisation.models.PersonalisablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='MatchProductQuerystring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product')),
                ('segment', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='learn_matchproductquerystrings', to='wagtail_personalisation.Segment')),
            ],
            options={
                'verbose_name': 'Match product rule',
            },
        ),
        migrations.CreateModel(
            name='MatchCountryQuerystring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Country')),
                ('segment', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='learn_matchcountryquerystrings', to='wagtail_personalisation.Segment')),
            ],
            options={
                'verbose_name': 'Match country rule',
            },
        ),
    ]
