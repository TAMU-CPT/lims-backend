# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 01:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0025_auto_20170112_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='assembly',
            name='complete',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='phage',
            name='closure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.ExperimentalResult'),
        ),
        migrations.AddField(
            model_name='phage',
            name='end_determination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_determ_result', to='lims.ExperimentalResult'),
        ),
        migrations.AddField(
            model_name='phage',
            name='end_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='phage',
            name='head_size',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='doi',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]