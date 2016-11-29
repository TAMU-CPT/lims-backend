from rest_framework import serializers
from bioproject.models import EditingRoleUser, EditingRoleGroup, Bioproject
from directory.serializers import GrouplessUserSerializer, GroupSerializer
from lims.serializers import PhageSerializerList
from lims.models import Phage
from django.contrib.auth.models import User, Group

from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator
import logging
logger = logging.getLogger(__name__)


class EditingRoleUserSerializer(serializers.ModelSerializer):
    user = GrouplessUserSerializer(partial=True)

    class Meta:
        model = EditingRoleUser
        fields = ('id', 'role', 'user', 'bioproject')

    def to_internal_value(self, data):
        # https://github.com/tomchristie/django-rest-framework/issues/2403#issuecomment-95528016
        if 'id' in data and 'id' in self.fields:
            try:
                obj_id = self.fields['id'].to_internal_value(data['id'])
            except ValidationError as exc:
                raise ValidationError({'id': exc.detail})
            for field in self.fields.values():
                for validator in field.validators:
                    if type(validator) == UniqueValidator:
                        # Exclude id from queryset for checking uniqueness
                        validator.queryset = validator.queryset.exclude(id=obj_id)
        return super(EditingRoleUserSerializer, self).to_internal_value(data)


class EditingRoleGroupSerializer(serializers.ModelSerializer):
    group = GroupSerializer(partial=True)

    class Meta:
        model = EditingRoleGroup
        fields = ('id', 'role', 'group', 'bioproject')

    def to_internal_value(self, data):
        if 'id' in data and 'id' in self.fields:
            try:
                obj_id = self.fields['id'].to_internal_value(data['id'])
            except ValidationError as exc:
                raise ValidationError({'id': exc.detail})
            for field in self.fields.values():
                for validator in field.validators:
                    if type(validator) == UniqueValidator:
                        # Exclude id from queryset for checking uniqueness
                        validator.queryset = validator.queryset.exclude(id=obj_id)
        return super(EditingRoleGroupSerializer, self).to_internal_value(data)


class BioprojectSerializer(serializers.ModelSerializer):
    editingrolegroup_set = EditingRoleGroupSerializer(many=True)
    editingroleuser_set = EditingRoleUserSerializer(many=True)
    owner = GrouplessUserSerializer(partial=True)
    sample = PhageSerializerList(many=True)

    class Meta:
        model = Bioproject
        fields = ('id', 'name', 'description', 'sample',
                  'editingrolegroup_set', 'editingroleuser_set', 'date',
                  'owner')
        read_only = ('date')

    # def to_internal_value(self, data):
        # print 'asdf'
        # return data

    def create(self, validated_data):
        bp = Bioproject.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            owner=validated_data['owner'],
        )
        bp.save()
        return bp

    def update(self, instance, validated_data):
        new_samples = []

        # To handle roles first we need the full set of roles (so we know which
        # ones to delete eventually)
        previous_erus = [r.user.id for r in instance.editingroleuser_set.all()]
        previous_ergs = [r.group.id for r in instance.editingrolegroup_set.all()]

        for user in validated_data['editingroleuser_set']:
            u = User.objects.get(username=user['user']['username'])
            role, created = EditingRoleUser.objects.get_or_create(
                user=u,
                bioproject=instance,
            )
            role.role = user['role']
            role.save()

            # We can safely ignore this role now in the previous_erus.
            if u.id in previous_erus:
                previous_erus.remove(u.id)

        # Anything left in the previous_erus, we have not seen in the latest
        # erus, so we delete.
        for user_id in previous_erus:
            tmp = EditingRoleUser.objects.get(
                bioproject=instance,
                user=User.objects.get(id=user_id),
            )
            logging.info("Revoking %s permission for %s on %s", tmp.role, tmp.user, tmp.bioproject)
            print("Revoking %s permission for %s on %s" % (tmp.role, tmp.user, tmp.bioproject))
            tmp.delete()

        for group in validated_data['editingrolegroup_set']:
            g = Group.objects.get(name=group['group']['name'])
            role, created = EditingRoleGroup.objects.get_or_create(
                group=g,
                bioproject=instance,
            )
            role.role = group['role']
            role.save()

            if g.id in previous_ergs:
                previous_ergs.remove(g.id)

        # Anything left in the previous_ergs, we have not seen in the latest
        # ergs, so we delete.
        for group_id in previous_ergs:
            tmp = EditingRoleGroup.objects.get(
                bioproject=instance,
                group=Group.objects.get(id=group_id),
            )
            logging.info("Revoking %s permission for %s on %s", tmp.role, tmp.group, tmp.bioproject)
            print("Revoking %s permission for %s on %s" % (tmp.role, tmp.group, tmp.bioproject))
            tmp.delete()

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

    def to_internal_value(self, data):
        # https://github.com/tomchristie/django-rest-framework/issues/2403#issuecomment-95528016
        if 'id' in data and 'id' in self.fields:
            try:
                obj_id = self.fields['id'].to_internal_value(data['id'])
            except ValidationError as exc:
                raise ValidationError({'id': exc.detail})
            for field in self.fields.values():
                for validator in field.validators:
                    if type(validator) == UniqueValidator:
                        # Exclude id from queryset for checking uniqueness
                        validator.queryset = validator.queryset.exclude(id=obj_id)
        return super(BioprojectSerializer, self).to_internal_value(data)
