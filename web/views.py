from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from web.models import Assembly, StorageLocation, Box, EnvironmentalSample, Lysate, PhageDNAPrep, Experiment, ExperimentalResult, Bacteria, ContainerType, SampleType, SequencingRun, SequencingRunPool, SequencingRunPoolItem, Tube, TubeType
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from datetimewidget.widgets import DateTimeWidget

class LIMSDataDump(ListView):
    model = EnvironmentalSample

class StorageLocationList(ListView):
    model = StorageLocation

class StorageLocationDetail(DetailView):
    model = StorageLocation

class StorageLocationCreate(CreateView):
    model = StorageLocation
    fields = ('name', 'location', 'container_type')

class StorageLocationEdit(UpdateView):
    model = StorageLocation
    fields = ('name', 'location', 'container_type')

class StorageLocationDelete(DeleteView):
    model = StorageLocation
    success_url = reverse_lazy('lims:storage-location-list')


class BoxList(ListView):
    model = Box

class BoxDetail(DetailView):
    model = Box

class BoxCreate(CreateView):
    model = Box
    fields = ('name',)
    template_name_suffix = '_create'

    def form_valid(self, form):
        form.instance.location = StorageLocation.objects.get(pk=self.kwargs['container_id'])
        return super(BoxCreate, self).form_valid(form)

class BoxEdit(UpdateView):
    model = Box
    fields = ('name', 'location')
    template_name_suffix = '_update'

class BoxDelete(DeleteView):
    model = Box
    success_url = reverse_lazy('lims:box-list')


class Index(TemplateView):
    template_name = "web/index.html"

class ExperimentList(ListView):
    model = Experiment

class ExperimentDetail(DetailView):
    model = Experiment

class ExperimentalResultList(ListView):
    model = ExperimentalResult

class ExperimentalResultDetail(DetailView):
    model = ExperimentalResult


class EnvSample_list(ListView):
    model = EnvironmentalSample

class EnvSample_view(DetailView):
    model = EnvironmentalSample

class EnvSample_create(CreateView):
    model = EnvironmentalSample
    fields = ('collection', 'location', 'sample_type', 'tube')
    template_name_suffix = '_create'

class EnvSample_edit(UpdateView):
    model = EnvironmentalSample
    fields = ('collection', 'location', 'sample_type', 'tube')
    template_name_suffix = '_update'

class EnvSample_delete(DeleteView):
    model = EnvironmentalSample
    success_url = reverse_lazy('lims:env-sample-list')


class Lysate_list(ListView):
    model = Lysate

class Lysate_view(DetailView):
    model = Lysate

class Lysate_create(CreateView):
    model = Lysate
    template_name_suffix = '_create'
    form_class =  modelform_factory(
        Lysate,
        fields=('env_sample', 'host_lims', 'oldid', 'isolation', 'owner', 'source', 'tube'),
        widgets={"isolation": DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)}
    )

class Lysate_edit(UpdateView):
    model = Lysate
    template_name_suffix = '_update'
    form_class =  modelform_factory(
        Lysate,
        fields=('env_sample', 'host_lims', 'oldid', 'isolation', 'owner', 'source', 'tube'),
        widgets={"isolation": DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)}
    )

class Lysate_delete(DeleteView):
    model = Lysate


class PhageDNAPrep_list(ListView):
    model = PhageDNAPrep

class PhageDNAPrep_view(DetailView):
    model = PhageDNAPrep

class PhageDNAPrep_create(CreateView):
    model = PhageDNAPrep
    # Exempt are experiments
    fields = ('lysate', 'morphology', 'tube')
    template_name_suffix = '_create'

class PhageDNAPrep_edit(UpdateView):
    model = PhageDNAPrep
    fields = ('lysate', 'morphology', 'tube')
    template_name_suffix = '_update'

class PhageDNAPrep_delete(DeleteView):
    model = PhageDNAPrep


class BacteriaList(ListView):
    model = Bacteria

class BacteriaDetail(DetailView):
    model = Bacteria

class BacteriaCreate(CreateView):
    model = Bacteria
    fields = ("genus", "species", "strain")
    template_name_suffix = '_create'

class BacteriaEdit(UpdateView):
    model = Bacteria
    fields = ("genus", "species", "strain")
    template_name_suffix = '_update'

class BacteriaDelete(DeleteView):
    model = Bacteria
    success_url = reverse_lazy('lims:bacteria-list')

from rest_framework import viewsets
from web.serializers import AssemblySerializer, BacteriaSerializer, BoxSerializer, ContainerTypeSerializer, EnvironmentalSampleSerializer, ExperimentSerializer, ExperimentalResultSerializer, LysateSerializer, PhageDNAPrepSerializer, SampleTypeSerializer, SequencingRunSerializer, SequencingRunPoolSerializer, SequencingRunPoolItemSerializer, StorageLocationSerializer, TubeSerializer, TubeTypeSerializer

class AssemblyViewSet(viewsets.ModelViewSet):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer

class BacteriaViewSet(viewsets.ModelViewSet):
    queryset = Bacteria.objects.all()
    serializer_class = BacteriaSerializer

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

class ContainerTypeViewSet(viewsets.ModelViewSet):
    queryset = ContainerType.objects.all()
    serializer_class = ContainerTypeSerializer

class EnvironmentalSampleViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalSample.objects.all()
    serializer_class = EnvironmentalSampleSerializer

class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

class ExperimentalResultViewSet(viewsets.ModelViewSet):
    queryset = ExperimentalResult.objects.all()
    serializer_class = ExperimentalResultSerializer

class LysateViewSet(viewsets.ModelViewSet):
    queryset = Lysate.objects.all()
    serializer_class = LysateSerializer

class PhageDNAPrepViewSet(viewsets.ModelViewSet):
    queryset = PhageDNAPrep.objects.all()
    serializer_class = PhageDNAPrepSerializer

class SampleTypeViewSet(viewsets.ModelViewSet):
    queryset = SampleType.objects.all()
    serializer_class = SampleTypeSerializer

class SequencingRunViewSet(viewsets.ModelViewSet):
    queryset = SequencingRun.objects.all()
    serializer_class = SequencingRunSerializer

class SequencingRunPoolViewSet(viewsets.ModelViewSet):
    queryset = SequencingRunPool.objects.all()
    serializer_class = SequencingRunPoolSerializer

class SequencingRunPoolItemViewSet(viewsets.ModelViewSet):
    queryset = SequencingRunPoolItem.objects.all()
    serializer_class = SequencingRunPoolItemSerializer

class StorageLocationViewSet(viewsets.ModelViewSet):
    queryset = StorageLocation.objects.all()
    serializer_class = StorageLocationSerializer

class TubeViewSet(viewsets.ModelViewSet):
    queryset = Tube.objects.all()
    serializer_class = TubeSerializer

class TubeTypeViewSet(viewsets.ModelViewSet):
    queryset = TubeType.objects.all()
    serializer_class = TubeTypeSerializer
