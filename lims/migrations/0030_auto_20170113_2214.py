# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0029_auto_20170113_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bacteria',
            name='species',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='bacteria',
            name='strain',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]