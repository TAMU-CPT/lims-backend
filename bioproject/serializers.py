
from rest_framework import serializers
from bioproject.models import EditingRoleUser, EditingRoleGroup, Bioproject
from directory.serializers import GrouplessUserSerializer, GroupSerializer

class EditingRoleUserSerializer(serializers.HyperlinkedModelSerializer):
    user = GrouplessUserSerializer()

    class Meta:
        model = EditingRoleUser
        fields = ('id', 'role', 'user')

class EditingRoleGroupSerializer(serializers.HyperlinkedModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = EditingRoleGroup
        fields = ('id', 'role', 'group')

class BioprojectSerializer(serializers.HyperlinkedModelSerializer):
    editingrolegroup_set = EditingRoleGroupSerializer(many=True)
    editingroleuser_set = EditingRoleUserSerializer(many=True)

    class Meta:
        model = Bioproject
        fields = ('name', 'sample', 'editingrolegroup_set',
                  'editingroleuser_set', 'date', 'id', 'description',)
