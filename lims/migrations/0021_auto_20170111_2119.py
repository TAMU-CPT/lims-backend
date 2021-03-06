# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0020_auto_20170111_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phage',
            name='source',
        ),
        migrations.AddField(
            model_name='phage',
            name='refseq_id',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='phage',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='directory.Organisation'),
        ),
    ]
