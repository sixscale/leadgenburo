# Generated by Django 5.0 on 2024-02-01 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0012_rename_configprojectsname_configprojectnames'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ConfigProjectNames',
        ),
        migrations.AddField(
            model_name='integrationsdata',
            name='skorozvon_scenario_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
