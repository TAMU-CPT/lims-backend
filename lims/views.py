from rest_framework import viewsets, filters
import django_filters
import django_filters.rest_framework

from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q, Count
from lims.serializers import StorageSerializer, \
    AssemblySerializer, ExperimentalResultSerializer, \
    SequencingRunSerializerDetail, \
    SequencingRunSerializerList, \
    ExperimentSerializer, PhageSerializerList, PhageSerializerDetail, \
    PhageDNAPrepSerializer, SequencingRunPoolSerializer, \
    SequencingRunPoolItemSerializer, \
    EnvironmentalSampleSerializer, TypesEnvironmentalSampleSerializer, LysateSerializer, BacteriaSerializer, \
    EnvironmentalSampleCollectionSerializer, RoomStorageSerializer, \
    SimpleEnvironmentalSampleCollectionSerializer, \
    ContainerLabelStorageSerializer, BoxStorageSerializer
from lims.models import Storage, Assembly, \
    ExperimentalResult, SequencingRun, Experiment, Phage, \
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


class BoxStorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.values('box').distinct()
    serializer_class = BoxStorageSerializer
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

    def get_serializer_class(self):
        if self.action == 'list':
            return SequencingRunSerializerList
        return SequencingRunSerializerDetail


    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user.account
        )


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

    paginate_by = None


class PhageDNAPrepViewSet(viewsets.ModelViewSet):
    queryset = PhageDNAPrep.objects.all()
    serializer_class = PhageDNAPrepSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError as ie:
            if 'storage_id' in str(ie):
                raise ValidationError('Duplicate storage')


class SequencingRunPoolViewSet(viewsets.ModelViewSet):
    queryset = SequencingRunPool.objects.all()
    serializer_class = SequencingRunPoolSerializer


class SRPIFilter(django_filters.FilterSet):
    no_pool = django_filters.CharFilter(method="get_no_pool")

    class Meta:
        model = SequencingRunPoolItem
        fields = ['id', 'no_pool']

    def get_no_pool(self, qs, name, value):
        return qs.filter(pool=None)


class SequencingRunPoolItemViewSet(viewsets.ModelViewSet):
    queryset = SequencingRunPoolItem.objects.all()
    serializer_class = SequencingRunPoolItemSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = SRPIFilter
    # TODO:
    # paginate_by = None


class EnvironmentalSampleViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalSample.objects.all()
    serializer_class = EnvironmentalSampleSerializer

    def perform_create(self, serializer):
        # Fetch location or crash if none
        loc = self.request.data.get('location', None)
        if loc is None:
            raise Exception("Must provide location")

        loc['lat'] = float(loc['lat'])
        loc['lng'] = float(loc['lng'])

        assert -90 <= loc['lat'] <= 90
        assert -180 <= loc['lng'] <= 180

        # Make changes
        serializer.save(
            location="SRID=4326;POINT (%s %s)" % (loc['lng'], loc['lat']),
            collected_by=self.request.user.account,
            sample_type=self.request.data.get('sample_type', 'Unknown'),
        )
        print self.request.data

class TypesEnvironmentalSampleFilter(django_filters.FilterSet):
    sample_type = django_filters.CharFilter(name="sample_type", lookup_expr="icontains")

    class Meta:
        model = EnvironmentalSample
        fields = ['id', 'sample_type']

class TypesEnvironmentalSampleViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalSample.objects.values('sample_type').distinct()
    serializer_class = TypesEnvironmentalSampleSerializer
    filter_class = TypesEnvironmentalSampleFilter
    paginate_by = None


class EnvironmentalSampleCollectionFilter(django_filters.FilterSet):
    custom = django_filters.CharFilter(method="get_custom")
    true_collection = django_filters.BooleanFilter(name="true_collection")

    class Meta:
        model = EnvironmentalSampleCollection
        fields = ['id', 'custom', 'true_collection']

    def get_custom(self, queryset, name, value):
        # Here we wish to choose the union of:
        #
        # - those which are true collection (i.e. envsamplecollections with multiple samples)
        # - everything not in a true collection (i.e. ESCs which are solely in a single (default) ESC)
        #
        interesting_ids = [x.id for x in EnvironmentalSampleCollection.objects.all().filter(true_collection=True)]
        for x in EnvironmentalSample.objects.annotate(esr_count=Count('environmentalsamplerelation')).filter(esr_count=1):
            interesting_ids.append(x.environmentalsamplerelation_set.first().esc.id)

        return queryset.filter(id__in=interesting_ids)


class EnvironmentalSampleCollectionViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalSampleCollection.objects.all()
    serializer_class = EnvironmentalSampleCollectionSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = EnvironmentalSampleCollectionFilter
    ordering_fields = ('__all__')


class SimpleEnvironmentalSampleCollectionViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalSampleCollection.objects.all()
    serializer_class = SimpleEnvironmentalSampleCollectionSerializer


class LysateViewSet(viewsets.ModelViewSet):
    queryset = Lysate.objects.all()
    serializer_class = LysateSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError as ie:
            if 'storage_id' in str(ie):
                raise ValidationError('Duplicate storage')


class BacteriaFilter(django_filters.FilterSet):
    genus = django_filters.CharFilter(name="genus", lookup_expr="icontains")
    species = django_filters.CharFilter(name="species", lookup_expr="icontains")
    full = django_filters.CharFilter(method="get_full")

    class Meta:
        model = Bacteria
        fields = ['id', 'genus', 'species', 'strain']

    def get_full(self, queryset, name, value):
        ids = []
        for q in queryset:
            if value in q.full:
                ids.append(q.id)
        return queryset.filter(pk__in=ids)


class BacteriaViewSet(viewsets.ModelViewSet):
    queryset = Bacteria.objects.all()
    serializer_class = BacteriaSerializer
    ordering_fields = ('__all__')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = BacteriaFilter
