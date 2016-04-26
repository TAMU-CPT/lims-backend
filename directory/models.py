from __future__ import unicode_literals

from django.db import models

PERSONTAG_TYPES = (
    ('default', 'Default'),
    ('primary', 'PI'),
    ('info', 'BICH464')
)

class PersonTag(models.Model):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=12, choices=PERSONTAG_TYPES, default='default')

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

    def email_iter(self):
        for email in self.emails.split('\n'):
            yield email

    def primary_email(self):
        return self.emails.split('\n')[0]
