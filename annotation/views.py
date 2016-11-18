from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from .models import AnnotationRecord
from .serializers import AnnotationRecordSerializer
import django_filters


class AnnotationRecordViewSet(viewsets.ModelViewSet):
    queryset = AnnotationRecord.objects.all()
    serializer_class = AnnotationRecordSerializer
