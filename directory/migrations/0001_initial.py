# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tagulous.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('emails', models.TextField(blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=16)),
                ('fax_number', models.CharField(blank=True, max_length=16)),
                ('street_address', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
                ('path', models.TextField(unique=True)),
                ('label', models.CharField(help_text='The name of the tag, without ancestors', max_length=255)),
                ('level', models.IntegerField(default=1, help_text='The level of the tag in the tree')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='directory.PersonTag')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(tagulous.models.models.BaseTagTreeModel, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='persontag',
            unique_together=set([('slug', 'parent')]),
        ),
    ]
