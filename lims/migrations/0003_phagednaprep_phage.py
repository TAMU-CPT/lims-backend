# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-31 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0002_auto_20161031_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='phagednaprep',
            name='phage',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='lims.Phage'),
            preserve_default=False,
        ),
    ]