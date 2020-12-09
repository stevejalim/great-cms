# Generated by Django 2.2.10 on 2020-06-01 10:53

import django.db.models.deletion
from django.db import migrations, models

import core.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('exportplan', '0002_auto_20200408_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportPlanDashboardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=(core.mixins.WagtailAdminExclusivePageMixin, core.mixins.EnableTourMixin, core.mixins.AnonymousUserRequired, 'wagtailcore.page'),
        ),
    ]
