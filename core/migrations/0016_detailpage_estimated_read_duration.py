# Generated by Django 2.2.13 on 2020-07-06 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200623_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailpage',
            name='estimated_read_duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
