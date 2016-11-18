from rest_framework import serializers
from .models import AnnotationRecord
from lims.serializers import PhageSerializerList


class AnnotationRecordSerializer(serializers.HyperlinkedModelSerializer):
    phage = PhageSerializerList()

    class Meta:
        model = AnnotationRecord
        fields = ('id', 'phage', 'chado_id', 'apollo_id')
