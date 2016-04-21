from __future__ import unicode_literals

from django.db import models

class PersonTag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Organisation(models.Model):
    name = models.TextField()
    emails = models.TextField(blank=True)
    phone_number = models.CharField(max_length=16,blank=True)
    fax_number = models.CharField(max_length=16,blank=True)
    street_address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.TextField()
    initials = models.TextField()
    nickname = models.TextField(blank=True)
    netid = models.CharField(max_length=32, blank=True)
    emails = models.TextField(blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    tags = models.ManyToManyField(PersonTag, blank=True)
    orcid = models.CharField(max_length=32, blank=True)
    orgs = models.ManyToManyField(Organisation, blank=True)
    original_id = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return self.name

    def email_iter(self):
        for email in self.emails.split('\n'):
            yield email

    def primary_email(self):
        return self.emails.split('\n')[0]

    class Meta:
        verbose_name_plural = "people"
