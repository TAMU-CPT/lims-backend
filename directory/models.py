from __future__ import unicode_literals

from django.db import models

PERSONTAG_TYPES = (
    ('default', 'Default'),
    ('primary', 'PI'),
    ('info', 'BICH464')
)


# import tagulous.models

# class PersonTag(tagulous.models.TagTreeModel):
    # class TagMeta:
        # initial = [
            # 'BICH464/2012',
            # 'BICH464/2013',
            # 'BICH464/2014',
            # 'BICH464/2015',
            # 'BICH464/2016',
            # 'CPT/PI',
            # 'CPT/Gill',
            # 'CPT/Young',
            # 'CPT/Gonzalez',
            # 'Staff',
        # ]
        # space_delimiter = True
        # # autocomplete_view = 'person_tags_autocomplete'


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
