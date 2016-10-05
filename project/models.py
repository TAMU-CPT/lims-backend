from __future__ import unicode_literals

from django.db import models
from web.models import Phage
# Create your models here.

class Bioproject(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    sample = models.ManyToManyField(Phage, blank=True)
    date = models.DateTimeField(auto_now_add=True)
