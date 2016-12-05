from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from directory.serializers import UserSerializer, GroupSerializer, OrganisationSerializer, OrganisationSerializerList
from directory.models import Organisation
import django_filters


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_expr="contains")

    class Meta:
        model = Group
        fields = ['name', 'id']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    # filter_fields = ('name', 'id')
    filter_class = GroupFilter
    serializer_class = GroupSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OrganisationSerializerList

        return OrganisationSerializer
