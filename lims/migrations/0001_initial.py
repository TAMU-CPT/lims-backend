# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 23:29
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assembly',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('galaxy_dataset', models.URLField()),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'assemblies',
            },
        ),
        migrations.CreateModel(
            name='Bacteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genus', models.CharField(max_length=64)),
                ('species', models.CharField(blank=True, max_length=64)),
                ('strain', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'verbose_name_plural': 'bacteria',
            },
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name which is written on the outside of the box.', max_length=64)),
            ],
            options={
                'verbose_name_plural': 'boxes',
            },
        ),
        migrations.CreateModel(
            name='ContainerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentalSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('collection', models.DateTimeField()),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentalSampleCollection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('env_sample', models.ManyToManyField(blank=True, to='lims.EnvironmentalSample')),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('short_name', models.CharField(max_length=32)),
                ('full_name', models.TextField()),
                ('methods', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentalResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('result', models.TextField()),
                ('date', models.DateTimeField()),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.Experiment')),
                ('run_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Lysate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oldid', models.CharField(blank=True, max_length=64)),
                ('isolation', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_name', models.CharField(max_length=64, unique=True)),
                ('historical_names', models.TextField()),
                ('assembly', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.Assembly')),
                ('env_sample_collection', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='lims.EnvironmentalSampleCollection')),
                ('host_lims', models.ManyToManyField(blank=True, to='lims.Bacteria')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='directory.Organisation')),
            ],
        ),
        migrations.CreateModel(
            name='PhageDNAPrep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('morphology', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Podophage'), (2, 'Myophage'), (3, 'Siphophage')])),
                ('experiments', models.ManyToManyField(blank=True, to='lims.ExperimentalResult')),
                ('lysate', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.Lysate')),
            ],
        ),
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='SequencingRun',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('galaxy_history', models.URLField()),
                ('name', models.TextField()),
                ('date', models.DateField()),
                ('bioanalyzer_qc', models.TextField()),
                ('run_prep_spreadsheet', models.URLField()),
                ('methods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='SequencingRunPool',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pool', models.CharField(max_length=16)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.SequencingRun')),
            ],
        ),
        migrations.CreateModel(
            name='SequencingRunPoolItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dna_conc', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='lims.ExperimentalResult')),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.SequencingRunPool')),
            ],
        ),
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=64)),
                ('container_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.ContainerType')),
            ],
        ),
        migrations.CreateModel(
            name='Tube',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.Box')),
            ],
        ),
        migrations.CreateModel(
            name='TubeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='tube',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.TubeType'),
        ),
        migrations.AddField(
            model_name='phagednaprep',
            name='tube',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lims.Tube'),
        ),
        migrations.AddField(
            model_name='lysate',
            name='phage',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lims.Phage'),
        ),
        migrations.AddField(
            model_name='lysate',
            name='tube',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lims.Tube'),
        ),
        migrations.AddField(
            model_name='environmentalsample',
            name='sample_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.SampleType'),
        ),
        migrations.AddField(
            model_name='environmentalsample',
            name='tube',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lims.Tube'),
        ),
        migrations.AddField(
            model_name='box',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.StorageLocation'),
        ),
        migrations.AddField(
            model_name='assembly',
            name='sequencing_run_pool_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.SequencingRunPoolItem'),
        ),
        migrations.AlterUniqueTogether(
            name='sequencingrunpool',
            unique_together=set([('pool', 'run')]),
        ),
    ]
