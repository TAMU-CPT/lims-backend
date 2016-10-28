from rest_framework import serializers
from bioproject.models import EditingRoleUser, EditingRoleGroup, Bioproject
from directory.serializers import GrouplessUserSerializer, GroupSerializer
from lims.serializers import PhageSerializerList
from lims.models import Phage

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
    editingrolegroup_set = EditingRoleGroupSerializer(many=True, read_only=True)
    editingroleuser_set = EditingRoleUserSerializer(many=True, read_only=True)
    sample = PhageSerializerList(many=True)

    class Meta:
        model = Bioproject
        fields = ('id', 'name', 'description',
                  # read only
                  'sample', 'editingrolegroup_set', 'editingroleuser_set', 'date')
        read_only = ('sample', 'date', 'editingrolegroup_set', 'editingroleuser_set')

    # def to_internal_value(self, data):
        # print 'asdf'
        # return data

    def create(self, validated_data):
        bp = Bioproject.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
        )
        bp.save()
        return bp

    def update(self, instance, validated_data):
        new_samples = []
        for sample in validated_data['sample']:
            try:
                phage = Phage.objects.get(id=sample['id'])
            except Phage.DoesNotExist:
                phage = Phage.objects.create(
                    primary_name=sample['primary_name'],
                    historical_names=sample['historical_names'],
                )
                # Overwrite the ID because the validated data is sent back to
                # the end user
                sample['id'] = phage.id

            new_samples.append(phage)

        # Set the samples
        instance.sample = new_samples
        return validated_data
