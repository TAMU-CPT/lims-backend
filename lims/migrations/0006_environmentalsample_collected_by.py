# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-23 00:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('lims', '0005_experiment_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='environmentalsample',
            name='collected_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]
