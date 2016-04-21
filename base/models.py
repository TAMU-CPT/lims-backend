from __future__ import unicode_literals
from fontawesome.fields import IconField
from django.db import models

class App(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    url = models.CharField(max_length=32)
    hidden = models.BooleanField(default=False)
    icon = IconField()

    def __str__(self):
        return self.name
