# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 20:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_auto_20160426_2020'),
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assembly',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('galaxy_dataset', models.URLField()),
                ('notes', models.TextField()),
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
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': 'boxes',
            },
        ),
        migrations.CreateModel(
            name='ContainerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentalSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.DateTimeField()),
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
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Experiment')),
                ('run_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Lysate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oldid', models.CharField(blank=True, max_length=64)),
                ('isolation', models.DateTimeField(blank=True)),
                ('env_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.EnvironmentalSample')),
                ('host_lims', models.ManyToManyField(blank=True, to='web.Bacteria')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='directory.Organisation')),
            ],
        ),
        migrations.CreateModel(
            name='PhageDNAPrep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('morphology', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Podophage'), (2, 'Myophage'), (3, 'Siphophage')])),
                ('pfge_expected_size', models.FloatField(blank=True)),
                ('experiments', models.ManyToManyField(blank=True, to='web.ExperimentalResult')),
                ('lysate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Lysate')),
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
                ('methods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='SequencingRunPool',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pool', models.CharField(max_length=16)),
                ('dna_preps', models.ManyToManyField(to='web.PhageDNAPrep')),
            ],
        ),
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=64)),
                ('container_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ContainerType')),
            ],
        ),
        migrations.CreateModel(
            name='Tube',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Box')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.TubeType'),
        ),
        migrations.AddField(
            model_name='sequencingrun',
            name='pools',
            field=models.ManyToManyField(to='web.SequencingRunPool'),
        ),
        migrations.AddField(
            model_name='phagednaprep',
            name='tube',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.Tube'),
        ),
        migrations.AddField(
            model_name='lysate',
            name='tube',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.Tube'),
        ),
        migrations.AddField(
            model_name='environmentalsample',
            name='sample_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.SampleType'),
        ),
        migrations.AddField(
            model_name='environmentalsample',
            name='tube',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.Tube'),
        ),
        migrations.AddField(
            model_name='box',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.StorageLocation'),
        ),
        migrations.AddField(
            model_name='assembly',
            name='dna_prep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.PhageDNAPrep'),
        ),
        migrations.AddField(
            model_name='assembly',
            name='sequencing_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.SequencingRunPool'),
        ),
    ]
