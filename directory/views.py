from rest_framework import viewsets

from .serializers import directoryPersonTagSerializer, OrganisationSerializer
from directory.models import PersonTag, Organisation

class PersonTagViewSet(viewsets.ModelViewSet):
    queryset = PersonTag.objects.all()
    serializer_class = PersonTagSerializer

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
