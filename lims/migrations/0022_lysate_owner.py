# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 23:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20161221_1908'),
        ('lims', '0021_auto_20170111_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='lysate',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]
