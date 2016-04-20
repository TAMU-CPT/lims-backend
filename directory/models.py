from __future__ import unicode_literals

from django.db import models

class PersonTag(models.Model):
    name = models.CharField(max_length=32)

class Organisation(models.Model):
    name = models.TextField()
    emails = models.TextField()
    phone_number = models.CharField(max_length=16)
    fax_number = models.CharField(max_length=16)
    street_address = models.TextField()
    website = models.URLField()

class Person(models.Model):
    name = models.TextField()
    initials = models.TextField()
    netid = models.CharField(max_length=32)
    emails = models.TextField()
    phone_number = models.CharField(max_length=16)
    tags = models.ManyToManyField(PersonTag)
    orcid = models.CharField(max_length=32)
    orgs = models.ManyToManyField(Organisation)
