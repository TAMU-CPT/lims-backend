from django.contrib.auth.models import User, Group
from account.serializers import AccountSerializerLight
from rest_framework import serializers
from directory.models import PersonTag, Organisation

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'account')

# class AccountSerializerLight(serializers.HyperlinkedModelSerializer):
    # class Meta:
        # model = Account
        # fields


class GrouplessUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name')

    def get_name(self, obj):
        return obj.account.name

class PersonTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonTag
        fields = ('id',)

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
