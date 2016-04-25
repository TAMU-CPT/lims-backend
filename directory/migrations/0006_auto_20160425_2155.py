# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0005_persontag_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persontag',
            name='type',
            field=models.CharField(choices=[('default', 'Default'), ('primary', 'PI'), ('info', 'BICH464')], default='default', max_length=12),
        ),
    ]
