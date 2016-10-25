from rest_framework import viewsets
from django.db.models import Q

from lims.serializers import BoxSerializer, StorageLocationSerializer, AssemblySerializer, TubeTypeSerializer, ExperimentalResultSerializer, SequencingRunSerializer, TubeSerializer, SampleTypeSerializer, ExperimentSerializer, PhageSerializer, PhageDNAPrepSerializer, SequencingRunPoolSerializer, SequencingRunPoolItemSerializer, ContainerTypeSerializer, EnvironmentalSampleSerializer, LysateSerializer, BacteriaSerializer
from lims.models import Box, StorageLocation, Assembly, TubeType, ExperimentalResult, SequencingRun, Tube, SampleType, Experiment, Phage, PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, ContainerType, EnvironmentalSample, Lysate, Bacteria

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

class StorageLocationViewSet(viewsets.ModelViewSet):
    queryset = StorageLocation.objects.all()
    serializer_class = StorageLocationSerializer

class AssemblyViewSet(viewsets.ModelViewSet):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer

class TubeTypeViewSet(viewsets.ModelViewSet):
    queryset = TubeType.objects.all()
    serializer_class = TubeTypeSerializer

class ExperimentalResultViewSet(viewsets.ModelViewSet):
    queryset = ExperimentalResult.objects.all()
    serializer_class = ExperimentalResultSerializer

class SequencingRunViewSet(viewsets.ModelViewSet):
    queryset = SequencingRun.objects.all()
    serializer_class = SequencingRunSerializer

class TubeViewSet(viewsets.ModelViewSet):
    queryset = Tube.objects.all()
    serializer_class = TubeSerializer

class SampleTypeViewSet(viewsets.ModelViewSet):
    queryset = SampleType.objects.all()
    serializer_class = SampleTypeSerializer

class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

class PhageViewSet(viewsets.ModelViewSet):
    # queryset = Phage.objects.all()
    serializer_class = PhageSerializer

    def get_queryset(self):
        qs = Phage.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            qs = qs.filter(
                Q(primary_name__icontains=name) |
                Q(historical_names__icontains=name)
            )
        return qs


class PhageDNAPrepViewSet(viewsets.ModelViewSet):
    queryset = PhageDNAPrep.objects.all()
    serializer_class = PhageDNAPrepSerializer

class SequencingRunPoolViewSet(viewsets.ModelViewSet):
    queryset = SequencingRunPool.objects.all()
    serializer_class = SequencingRunPoolSerializer

class SequencingRunPoolItemViewSet(viewsets.ModelViewSet):
    queryset = SequencingRunPoolItem.objects.all()
    serializer_class = SequencingRunPoolItemSerializer

class ContainerTypeViewSet(viewsets.ModelViewSet):
    queryset = ContainerType.objects.all()
    serializer_class = ContainerTypeSerializer

class EnvironmentalSampleViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalSample.objects.all()
    serializer_class = EnvironmentalSampleSerializer

class LysateViewSet(viewsets.ModelViewSet):
    queryset = Lysate.objects.all()
    serializer_class = LysateSerializer

class BacteriaViewSet(viewsets.ModelViewSet):
    queryset = Bacteria.objects.all()
    serializer_class = BacteriaSerializer
