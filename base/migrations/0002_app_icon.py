# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 23:52
from __future__ import unicode_literals

from django.db import migrations
import fontawesome.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='icon',
            field=fontawesome.fields.IconField(blank=True, max_length=60),
        ),
    ]