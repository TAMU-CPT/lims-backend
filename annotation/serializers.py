from rest_framework import serializers
from .models import AnnotationRecord
from lims.serializers import PhageSerializer


class AnnotationRecordSerializer(serializers.HyperlinkedModelSerializer):
    phage = PhageSerializer()

    class Meta:
        model = AnnotationRecord
        fields = ('id', 'phage', 'chado_id', 'apollo_id')
