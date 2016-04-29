from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from web.models import StorageLocation, Box, EnvironmentalSample, Lysate, PhageDNAPrep, Experiment, ExperimentalResult, Bacteria
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
