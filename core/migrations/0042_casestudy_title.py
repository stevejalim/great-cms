# Generated by Django 2.2.14 on 2020-10-20 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_drop_pages_listblock_from_curatedlistpage_topics_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='casestudy',
            name='title',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]