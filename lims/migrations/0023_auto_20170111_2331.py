# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 23:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0022_lysate_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lysate',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.Bacteria'),
        ),
    ]
