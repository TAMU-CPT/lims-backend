from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from web.models import StorageLocation, Box, EnvironmentalSample, Experiment, ExperimentalResult


class LIMSDataDump(ListView):
    model = EnvironmentalSample

class StorageLocationList(ListView):
    model = StorageLocation

class StorageLocationDetail(DetailView):
    model = StorageLocation

class BoxDetail(DetailView):
    model = Box

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
