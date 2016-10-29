from django.contrib.auth.models import User, Group
from account.serializers import AccountSerializerLight
from rest_framework import serializers
from directory.models import Organisation

from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

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
        return super(GroupSerializer, self).to_internal_value(data)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'account')


class GrouplessUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name')

    def get_name(self, obj):
        try:
            return obj.account.name
        except:
            try:
                u = User.objects.get(username=obj['username'])
                return u.account.name
            except:
                return 'temporarily-unknown-username'

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
        return super(GrouplessUserSerializer, self).to_internal_value(data)

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Organisation
        fields = ('id', 'phone_number', 'website', 'name', 'fax_number', 'emails', 'street_address', 'account_set', 'members')

    def get_members(self, obj):
        for idx, account in enumerate(obj.account_set.all()):
            yield AccountSerializerLight(account).data

class OrganisationSerializerList(serializers.HyperlinkedModelSerializer):
    members = serializers.SerializerMethodField(read_only=True)
    members_size = serializers.SerializerMethodField()

    class Meta:
        model = Organisation
        fields = ('id', 'name', 'members', 'members_size')

    def get_members(self, obj):
        MAX_LIST = 5
        for idx, account in enumerate(obj.account_set.all()):
            if idx >= MAX_LIST:
                break

            yield AccountSerializerLight(account).data

    def get_members_size(self, obj):
        return obj.account_set.count()
