
from rest_framework import serializers
from directory.models import PersonTag, Organisation

class PersonTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonTag
        fields = ('id',)

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ('phone_number', 'website', 'name', 'fax_number', 'id', 'emails', 'street_address',)
