# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20160427_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lysate',
            name='isolation',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]