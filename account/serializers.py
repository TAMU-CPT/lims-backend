
from rest_framework import serializers
from account.models import Account, EmailConfirmation, SignupCodeResult, SignupCode, EmailAddress, AccountDeletion, AnonymousAccount

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('phone_number', 'name', 'language', 'netid', 'tags', 'theme', 'original_id', 'user', 'orgs', 'orcid', 'timezone', 'nickname', 'id', 'initials',)

class EmailConfirmationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmailConfirmation
        fields = ('created', 'objects', 'key', 'email_address', 'id', 'sent',)

class SignupCodeResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SignupCodeResult
        fields = ('timestamp', 'signup_code', 'user', 'id',)

class SignupCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SignupCode
        fields = ('code', 'created', 'notes', 'expiry', 'use_count', 'id', 'max_uses', 'inviter', 'email', 'sent',)

class EmailAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ('verified', 'primary', 'email', 'objects', 'user', 'id',)

class AccountDeletionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountDeletion
        fields = ('id', 'date_requested', 'user', 'date_expunged', 'email',)

class AnonymousAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnonymousAccount
        fields = ('id',)
