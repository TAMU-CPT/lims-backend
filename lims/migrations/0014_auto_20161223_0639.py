# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-23 06:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0013_auto_20161223_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencingrunpoolitem',
            name='dna_prep',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.PhageDNAPrep'),
        ),
    ]
