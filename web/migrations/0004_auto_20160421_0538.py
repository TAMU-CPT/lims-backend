# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 05:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20160421_0529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experimentalresult',
            name='result_type',
        ),
        migrations.AddField(
            model_name='experimentalresult',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 5, 38, 40, 247580, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
