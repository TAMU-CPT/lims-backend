from __future__ import unicode_literals

from django.db import models
from directory.models import Person, Organisation

class ContainerType(models.Model):
    name = models.CharField(max_length=32)

class TubeType(models.Model):
    name = models.CharField(max_length=32)

class SampleType(models.Model):
    name = models.CharField(max_length=32)

class StorageLocation(models.Model):
    # Human readable name that gets written on it
    name = models.CharField(max_length=64)
    # Human readable location
    location = models.CharField(max_length=64)
    # Type of container
    container_type = models.ForeignKey(ContainerType)

class Box(models.Model):
    # Human readable name that gets written on it
    name = models.CharField(max_length=64)
    location = models.ForeignKey(StorageLocation)

class Tube(models.Model):
    tube_type = models.ForeignKey(TubeType)
    box = models.ForeignKey(Box)

class EnvironmentalSample(models.Model):
    collection = models.DateTimeField()
    # location = models.
    # TODO: location
    sample_type = models.ForeignKey(SampleType)
    tube = models.ForeignKey(Tube)

class Bacteria(models.Model):
    genus = models.CharField(max_length=64)
    species = models.CharField(max_length=64)
    strain = models.CharField(max_length=64)

class Lysate(models.Model):
    env_sample = models.ForeignKey(EnvironmentalSample)
    host_lims = models.ManyToManyField(Bacteria)
    tube = models.ForeignKey(Tube)
    oldid = models.CharField(max_length=64)
    isolation = models.DateTimeField()
    owner = models.ForeignKey(Person)
    source = models.ForeignKey(Organisation)
