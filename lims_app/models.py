from __future__ import unicode_literals
from fontawesome import fields
from django.db import models

class App(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    url = models.CharField(max_length=32)
    hidden = models.BooleanField(default=False)
    enabled = models.BooleanField(default=False)
    icon = fields.IconField()
    # 0 is lower
    priority = models.IntegerField(default=100)

    def __str__(self):
        return self.name
