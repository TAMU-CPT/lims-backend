# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-16 23:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='environmentalsamplecollection',
            name='true_collection',
            field=models.BooleanField(default=False, help_text="Whether or not this is a 'true' collection of multiple phages, or simply the default collection instance auto-created for an environmental sample"),
        ),
    ]
