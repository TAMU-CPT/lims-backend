from rest_framework import viewsets
import django_filters
from django.db.models import Q
from lims.serializers import StorageSerializer, \
    AssemblySerializer, ExperimentalResultSerializer, \
    SequencingRunSerializer, SampleTypeSerializer, \
    ExperimentSerializer, PhageSerializerList, PhageSerializerDetail, \
    PhageDNAPrepSerializer, SequencingRunPoolSerializer, \
    SequencingRunPoolItemSerializer, \
    EnvironmentalSampleSerializer, LysateSerializer, BacteriaSerializer, \
    EnvironmentalSampleCollectionSerializer
from lims.models import Storage, Assembly, \
    ExperimentalResult, SequencingRun, SampleType, Experiment, Phage, \
    PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, \
    EnvironmentalSample, Lysate, Bacteria, EnvironmentalSampleCollection


class StorageFilter(django_filters.FilterSet):
    room = django_filters.CharFilter(name="room", lookup_type="contains")

    class Meta:
        model = Storage
        fields = ['room', 'id']


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    filter_class = StorageFilter
    serializer_class = StorageSerializer


class AssemblyViewSet(viewsets.ModelViewSet):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer


class ExperimentalResultViewSet(viewsets.ModelViewSet):
    queryset = ExperimentalResult.objects.all()
    serializer_class = ExperimentalResultSerializer


class SequencingRunViewSet(viewsets.ModelViewSet):
    queryset = SequencingRun.objects.all()
    serializer_class = SequencingRunSerializer


class SampleTypeViewSet(viewsets.ModelViewSet):
    queryset = SampleType.objects.all()
    serializer_class = SampleTypeSerializer


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    filter_fields = ('full_name', 'id', 'short_name', 'category')


class PhageViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        qs = Phage.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            qs = qs.filter(
                Q(primary_name__icontains=name) |
                Q(historical_names__icontains=name)
            )
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return PhageSerializerList
        return PhageSerializerDetail


class PhageDNAPrepViewSet(viewsets.ModelViewSet):
    queryset = PhageDNAPrep.objects.all()
    serializer_class = PhageDNAPrepSerializer


class SequencingRunPoolViewSet(viewsets.ModelViewSet):
    queryset = SequencingRunPool.objects.all()
    serializer_class = SequencingRunPoolSerializer


class SequencingRunPoolItemViewSet(viewsets.ModelViewSet):
    queryset = SequencingRunPoolItem.objects.all()
    serializer_class = SequencingRunPoolItemSerializer


class EnvironmentalSampleViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalSample.objects.all()
    serializer_class = EnvironmentalSampleSerializer


class EnvironmentalSampleCollectionViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalSampleCollection.objects.all()
    serializer_class = EnvironmentalSampleCollectionSerializer


class LysateViewSet(viewsets.ModelViewSet):
    queryset = Lysate.objects.all()
    serializer_class = LysateSerializer


class BacteriaViewSet(viewsets.ModelViewSet):
    queryset = Bacteria.objects.all()
    serializer_class = BacteriaSerializer
