from __future__ import unicode_literals
from django.db import models
from lims.models import Phage
import uuid


class AnnotationRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phage = models.ForeignKey(Phage)

    chado_id = models.IntegerField(blank=True, null=True)
    apollo_id = models.TextField(blank=True)
