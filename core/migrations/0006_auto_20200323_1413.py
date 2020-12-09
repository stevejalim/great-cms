# Generated by Django 2.2.10 on 2020-03-20 16:15

import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail_personalisation.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_personalisation', '0025_auto_20190822_0627'),
        ('core', '0005_matchcountryquerystring_matchfirstcountryofinterestrule_matchproductquerystring_personalisedpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalisedpage',
            name='body',
            field=wagtail.core.fields.StreamField([('body', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock())], icon='pilcrow', template='core/personalised_page_struct_paragraph_block.html'))]),
        ),
        migrations.CreateModel(
            name='MatchFirstIndustryOfInterestRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry', models.TextField(choices=[('SL10001', 'Advanced Engineering'), ('SL10002', 'Aerospace'), ('SL10003', 'Agriculture, Horticulture and Fisheries'), ('SL10004', 'Airports'), ('SL10005', 'Automotive'), ('SL10006', 'Biotechnology & Pharmaceuticals'), ('SL10007', 'Chemicals'), ('SL10008', 'Construction'), ('SL10009', 'Consumer, Retail and Luxury'), ('SL10010', 'Creative and Media'), ('SL10011', 'Cyber Security'), ('SL10012', 'Defence'), ('SL10013', 'Education & Training'), ('SL10014', 'Energy'), ('SL10015', 'Environment'), ('SL10016', 'Financial & Professional Services'), ('SL10017', 'Food & Drink'), ('SL10018', 'Healthcare & Medical'), ('SL10019', 'Leisure & Tourism'), ('SL10020', 'Life Sciences'), ('SL10021', 'Maritme'), ('SL10022', 'Mining'), ('SL10023', 'Railways'), ('SL10024', 'Security'), ('SL10025', 'Space'), ('SL10026', 'Sports Economy'), ('SL10027', 'Technology & Smart Cities'), ('SL10028', 'Water')])),
                ('segment', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_matchfirstindustryofinterestrules', to='wagtail_personalisation.Segment')),
            ],
            options={
                'verbose_name': 'Match first industry of interest rule',
            },
        ),
    ]
