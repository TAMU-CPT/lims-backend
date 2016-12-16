from rest_framework import viewsets, filters
import django_filters
from django.db.models import Q
from lims.serializers import StorageSerializer, \
    AssemblySerializer, ExperimentalResultSerializer, \
    SequencingRunSerializer, SampleTypeSerializer, \
    ExperimentSerializer, PhageSerializerList, PhageSerializerDetail, \
    PhageDNAPrepSerializer, SequencingRunPoolSerializer, \
    SequencingRunPoolItemSerializer, \
    EnvironmentalSampleSerializer, LysateSerializer, BacteriaSerializer, \
    EnvironmentalSampleCollectionSerializer, RoomStorageSerializer, \
    ContainerLabelStorageSerializer
from lims.models import Storage, Assembly, \
    ExperimentalResult, SequencingRun, SampleType, Experiment, Phage, \
    PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, \
    EnvironmentalSample, Lysate, Bacteria, EnvironmentalSampleCollection


class StorageFilter(django_filters.FilterSet):
    room = django_filters.CharFilter(name="room", lookup_expr="icontains")
    rooms = django_filters.CharFilter(method="get_rooms")
    container_label = django_filters.CharFilter(name="container_label", lookup_expr="icontains")
    container_labels = django_filters.CharFilter(method="get_container_labels")
    box = django_filters.CharFilter(name="box", lookup_expr="icontains")
    sample_label = django_filters.CharFilter(name="sample_label", lookup_expr="icontains")
    sample_category = django_filters.CharFilter(method="get_category")
    phage = django_filters.CharFilter(method="get_phage")

    class Meta:
        model = Storage
        fields = ['id', 'room', 'rooms', 'type', 'container_label', 'container_labels', 'shelf', 'box', 'sample_label', 'sample_category', 'phage']

    def get_rooms(self, queryset, name, value):
        return queryset.filter(room__in=value.split(','))

    def get_container_labels(self, queryset, name, value):
        return queryset.filter(container_label__in=value.split(','))

    def get_category(self, queryset, name, value):
        ids = []
        for q in queryset:
            if q.what_category == value:
                ids.append(q.id)

        return queryset.filter(pk__in=ids)

    def get_phage(self, queryset, name, value):
        ids = []
        for q in queryset:
            if q.what_category == 'lysate':
                try:
                    p = q.lysate.phage
                    if p.primary_name == value:
                        ids.append(q.id)
                except:
                    pass

            elif q.what_category == 'phagednaprep':
                try:
                    ps = q.phagednaprep.phage_set
                    for p in ps.all():
                        if p.primary_name == value:
                            ids.append(q.id)
                except:
                    pass

            elif q.what_category == 'envsample':
                try:
                    lysate_set = q.environmentalsamplecollection.lysate_set
                    for lysate in lysate_set.all():
                        try:
                            p = lysate.phage
                            if p.primary_name == value:
                                ids.append(q.id)
                        except:
                            pass
                except:
                    pass

        return queryset.filter(pk__in=ids)


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('__all__')
    filter_class = StorageFilter


class RoomStorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.values('room').distinct()
    serializer_class = RoomStorageSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('__all__')
    filter_class = StorageFilter
    paginate_by = None


class ContainerLabelStorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.values('container_label').distinct()
    serializer_class = ContainerLabelStorageSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('__all__')
    filter_class = StorageFilter
    paginate_by = None


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
