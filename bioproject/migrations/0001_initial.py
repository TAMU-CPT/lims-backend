# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-31 18:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lims', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bioproject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EditingRoleGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.IntegerField(choices=[(0, 'Viewer'), (1, 'Editor'), (2, 'Administrator')], default=0)),
                ('bioproject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bioproject.Bioproject')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='EditingRoleUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.IntegerField(choices=[(0, 'Viewer'), (1, 'Editor'), (2, 'Administrator')], default=0)),
                ('bioproject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bioproject.Bioproject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bioproject',
            name='access_group',
            field=models.ManyToManyField(blank=True, through='bioproject.EditingRoleGroup', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='bioproject',
            name='access_user',
            field=models.ManyToManyField(blank=True, through='bioproject.EditingRoleUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bioproject',
            name='sample',
            field=models.ManyToManyField(blank=True, to='lims.Phage'),
        ),
    ]
