# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-17 07:23
from __future__ import unicode_literals

import cropdetection.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropdetection', '0006_auto_20180117_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyze',
            name='result',
            field=models.FileField(blank=True, help_text='Select the result file(.tif).', max_length=300, upload_to=cropdetection.models.analyze_upload_dir),
        ),
        migrations.AlterField(
            model_name='shapefile',
            name='shape_file',
            field=models.FileField(help_text='Select the shape file.', max_length=300, upload_to=cropdetection.models.shape_files_upload_dir),
        ),
    ]
