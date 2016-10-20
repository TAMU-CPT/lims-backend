from rest_framework import viewsets

from .serializers import bioprojectEditingRoleUserSerializer, EditingRoleGroupSerializer, BioprojectSerializer
from bioproject.models import EditingRoleUser, EditingRoleGroup, Bioproject

class EditingRoleUserViewSet(viewsets.ModelViewSet):
    queryset = EditingRoleUser.objects.all()
    serializer_class = EditingRoleUserSerializer

class EditingRoleGroupViewSet(viewsets.ModelViewSet):
    queryset = EditingRoleGroup.objects.all()
    serializer_class = EditingRoleGroupSerializer

class BioprojectViewSet(viewsets.ModelViewSet):
    queryset = Bioproject.objects.all()
    serializer_class = BioprojectSerializer
