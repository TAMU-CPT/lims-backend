from django.contrib.auth.models import User, Group
from rest_framework import serializers
from directory.models import PersonTag, Organisation

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',)

class GrouplessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class PersonTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonTag
        fields = ('id',)

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ('phone_number', 'website', 'name', 'fax_number', 'id', 'emails', 'street_address',)
