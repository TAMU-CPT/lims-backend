# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-23 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0006_environmentalsample_collected_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='environmentalsamplecollection',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
