# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 20:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='tags',
        ),
    ]
