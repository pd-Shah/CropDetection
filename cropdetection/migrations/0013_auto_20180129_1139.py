# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 11:39
from __future__ import unicode_literals

import cropdetection.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropdetection', '0012_auto_20180127_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyze',
            name='input_path',
            field=models.FileField(help_text='Select input path file directory(.txt).', max_length=300, upload_to=cropdetection.models.analyze_upload_dir),
        ),
    ]
