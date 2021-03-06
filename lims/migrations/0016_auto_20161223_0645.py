# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-23 06:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0015_auto_20161223_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencingrunpoolitem',
            name='dna_conc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.ExperimentalResult'),
        ),
        migrations.AlterField(
            model_name='sequencingrunpoolitem',
            name='dna_prep',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lims.PhageDNAPrep'),
        ),
        migrations.AlterField(
            model_name='sequencingrunpoolitem',
            name='pool',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.SequencingRunPool'),
        ),
    ]
