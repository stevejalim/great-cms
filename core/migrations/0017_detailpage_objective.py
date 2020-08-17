# Generated by Django 2.2.14 on 2020-08-13 10:13

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_detailpage_estimated_read_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailpage',
            name='objective',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(options={'class': 'objectives'})), ('ListItem', wagtail.core.blocks.StructBlock([('item', wagtail.core.blocks.CharBlock(max_length=255))]))], default=None),
            preserve_default=False,
        ),
    ]