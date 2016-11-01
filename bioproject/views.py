from rest_framework import viewsets

from bioproject.serializers import EditingRoleUserSerializer, EditingRoleGroupSerializer, BioprojectSerializer
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

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(
                owner=self.request.user,
            )
