from __future__ import unicode_literals

from django.db import models
from web.models import EnvironmentalSample
# Create your models here.

class Bioproject(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    sample = models.ForeignKey(EnvironmentalSample)
    date = models.DateTimeField()
