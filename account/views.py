from rest_framework import viewsets

from account.serializers import AccountSerializer, EmailConfirmationSerializer, SignupCodeResultSerializer, SignupCodeSerializer, EmailAddressSerializer, AccountDeletionSerializer
from account.models import Account, EmailConfirmation, SignupCodeResult, SignupCode, EmailAddress, AccountDeletion

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class EmailConfirmationViewSet(viewsets.ModelViewSet):
    queryset = EmailConfirmation.objects.all()
    serializer_class = EmailConfirmationSerializer

class SignupCodeResultViewSet(viewsets.ModelViewSet):
    queryset = SignupCodeResult.objects.all()
    serializer_class = SignupCodeResultSerializer

class SignupCodeViewSet(viewsets.ModelViewSet):
    queryset = SignupCode.objects.all()
    serializer_class = SignupCodeSerializer

class EmailAddressViewSet(viewsets.ModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer

class AccountDeletionViewSet(viewsets.ModelViewSet):
    queryset = AccountDeletion.objects.all()
    serializer_class = AccountDeletionSerializer

