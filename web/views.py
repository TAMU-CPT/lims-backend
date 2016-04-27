from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from web.models import StorageLocation, Box, EnvironmentalSample, Experiment, ExperimentalResult
from django.core.urlresolvers import reverse_lazy



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

    def form_valid(self, form):
        form.instance.location = StorageLocation.objects.get(pk=self.kwargs['container_id'])
        return super(BoxCreate, self).form_valid(form)

class BoxEdit(UpdateView):
    model = Box
    fields = ('name', 'location')

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

class
