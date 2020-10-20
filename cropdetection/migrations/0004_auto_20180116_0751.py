# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-16 07:51
from __future__ import unicode_literals

import cropdetection.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropdetection', '0003_auto_20180115_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analyze',
            name='result',
        ),
        migrations.AddField(
            model_name='analyze',
            name='result_s1',
            field=models.FileField(blank=True, help_text='Select the result file(.tif).', upload_to=cropdetection.models.analyze_upload_dir),
        ),
        migrations.AddField(
            model_name='analyze',
            name='result_s2',
            field=models.FileField(blank=True, help_text='Select the result file(.tif).', upload_to=cropdetection.models.analyze_upload_dir),
        ),
    ]