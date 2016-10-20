from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from directory.serializers import UserSerializer, GroupSerializer, PersonTagSerializer, OrganisationSerializer
from directory.models import PersonTag, Organisation

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PersonTagViewSet(viewsets.ModelViewSet):
    queryset = PersonTag.objects.all()
    serializer_class = PersonTagSerializer

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
