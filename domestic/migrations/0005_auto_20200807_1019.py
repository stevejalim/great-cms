# Generated by Django 2.2.14 on 2020-08-07 10:19

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('domestic', '0004_domesticdashboard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domesticdashboard',
            name='routes',
        ),
        migrations.AddField(
            model_name='domesticdashboard',
            name='components',
            field=wagtail.core.fields.StreamField([('route', wagtail.core.blocks.StructBlock([('route_type', wagtail.core.blocks.ChoiceBlock(choices=[('learn', 'Learning'), ('plan', 'Export plan'), ('target', 'Target market')], icon='redirect')), ('title', wagtail.core.blocks.CharBlock(max_length=255)), ('body', wagtail.core.blocks.TextBlock(max_length=4096)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('button', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(max_length=255)), ('link', wagtail.core.blocks.StructBlock([('internal_link', wagtail.core.blocks.PageChooserBlock(label='Internal link', required=False)), ('external_link', wagtail.core.blocks.CharBlock(label='External link', max_length=255, required=False))], required=False))], icon='cog', required=False))], icon='pick'))], blank=True, null=True),
        ),
    ]