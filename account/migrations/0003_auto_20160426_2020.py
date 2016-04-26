# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 20:20
from __future__ import unicode_literals

from django.db import migrations, models
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
        ('account', '0002_fix_str'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='initials',
            field=models.CharField(default='', help_text='Their first and middle initials (PubMed format)', max_length=16),
        ),
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(default='', help_text='The full name of the person', max_length=255),
        ),
        migrations.AddField(
            model_name='account',
            name='netid',
            field=models.CharField(blank=True, help_text='Their netid, if available', max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='nickname',
            field=models.CharField(blank=True, help_text='Their preferred name, if applicable. Many non-American students choose to go by a different name.', max_length=255),
        ),
        migrations.AddField(
            model_name='account',
            name='orcid',
            field=models.CharField(blank=True, help_text="See <a href='https://orcid.org' target='_blank'>https://orcid.org</a>", max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='orgs',
            field=models.ManyToManyField(blank=True, help_text='Organisations the person is associated with. Please add an appropriate organisation if there is not one available', to='directory.Organisation'),
        ),
        migrations.AddField(
            model_name='account',
            name='original_id',
            field=models.CharField(blank=True, help_text='Internal use only', max_length=4),
        ),
        migrations.AddField(
            model_name='account',
            name='phone_number',
            field=models.CharField(blank=True, help_text='A phone number which they will continue to be reachable at (i.e. not an office phone #)', max_length=16),
        ),
        migrations.AddField(
            model_name='account',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, autocomplete_view='person_tags_autocomplete', blank=True, help_text="Tags allow us to group users easily and see in what way they were involved with the CPT's research", initial='BICH464/2012, BICH464/2013, BICH464/2014, BICH464/2015, BICH464/2016, CPT/Gill, CPT/Gonzalez, CPT/PI, CPT/Young, Staff', space_delimiter=True, to='directory.PersonTag', tree=True),
        ),
        migrations.AddField(
            model_name='account',
            name='theme',
            field=models.CharField(choices=[(b'default', b'Default'), (b'amelia', b'Amelia'), (b'cerulean', b'Cerulean'), (b'cosmo', b'Cosmo'), (b'cyborg', b'Cyborg'), (b'flatly', b'Flatly'), (b'journal', b'Journal'), (b'readable', b'Readable'), (b'simplex', b'Simplex'), (b'slate', b'Slate'), (b'spacelab', b'SpaceLab'), (b'united', b'United'), (b'superhero', b'Superhero'), (b'lumen', b'Lumen')], default='default', max_length=255),
        ),
    ]