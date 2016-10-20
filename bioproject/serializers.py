
from rest_framework import serializers
from bioproject.models import EditingRoleUser, EditingRoleGroup, Bioproject

class EditingRoleUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EditingRoleUser
        fields = ('id', 'role', 'user', 'bioproject',)

class EditingRoleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EditingRoleGroup
        fields = ('role', 'group', 'id', 'bioproject',)

class BioprojectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bioproject
        fields = ('name', 'sample', 'access_group', 'access_user', 'date', 'id', 'description',)
