from directory.models import Organisation
from account.models import Account
import hashlib
from rest_framework import serializers


class AccountLessOrgSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = (
            'name', 'emails', 'phone_number', 'fax_number',
            'street_address', 'website', 'id'
        )

class AccountSerializer(serializers.ModelSerializer):
    orgs = serializers.SerializerMethodField()
    gravatar_email = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            'user', 'timezone', 'language', 'name', 'initials',
            'nickname', 'netid', 'phone_number', 'tags', 'orcid', 'orgs',
            'original_id', 'gravatar_email'
        )

    def get_orgs(self, obj):
        for org in obj.orgs.all():
            yield AccountLessOrgSerializer(org).data

    def get_gravatar_email(self, obj):
        for email in obj.emails():
            return hashlib.md5(email.email).hexdigest()


class OrgLessUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            'user', 'timezone', 'language', 'name', 'initials',
            'nickname', 'netid', 'phone_number', 'tags', 'orcid',
            'original_id'
        )


class OrganisationSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Organisation
        fields = (
            'name', 'emails', 'phone_number', 'fax_number',
            'street_address', 'website', 'users'
        )

    def get_users(self, obj):
        for user in obj.account_set.all():
            yield OrgLessUserSerializer(user).data
