# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 00:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_app_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='priority',
            field=models.IntegerField(default=100),
        ),
    ]