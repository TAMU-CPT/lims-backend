# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-21 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0002_auto_20161217_0120'),
        ('bioproject', '0002_auto_20161221_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='bioproject',
            name='sample_env',
            field=models.ManyToManyField(blank=True, to='lims.EnvironmentalSampleCollection'),
        ),
    ]
