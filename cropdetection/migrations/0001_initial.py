# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-15 06:30
from __future__ import unicode_literals

import cropdetection.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analyze',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('result_s1', models.FileField(blank=True, help_text='Select the result file(.tif).', upload_to=cropdetection.models.analyze_upload_dir)),
                ('result_s2', models.FileField(blank=True, help_text='Select the result file(.tif).', upload_to=cropdetection.models.analyze_upload_dir)),
            ],
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('1', 'band red'), ('2', 'ndvi'), ('3', 'band green'), ('4', 'near infrared')], help_text='Select band.', max_length=300)),
                ('band', models.FileField(help_text='Select band file(.tif).', upload_to=cropdetection.models.band_upload_dir)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('analyze', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropdetection.Analyze')),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Set the calendar name.', max_length=300)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True, help_text='any more comment?', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Set the crop name.', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Phenology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='maximum greenness date for example', max_length=300)),
                ('start', models.DateField(help_text='Set the start date.')),
                ('end', models.DateField(help_text='Set the end date.')),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropdetection.Calendar')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Set the region name.', max_length=300, unique=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShapeFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('shape_file', models.FileField(help_text='Select the shape file.', upload_to=cropdetection.models.shape_files_upload_dir)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropdetection.Region')),
            ],
        ),
        migrations.AddField(
            model_name='crop',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropdetection.Region'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='crop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cropdetection.Crop'),
        ),
        migrations.AddField(
            model_name='analyze',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropdetection.Region'),
        ),
    ]