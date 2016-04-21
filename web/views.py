from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from web.models import StorageLocation, Box

class StorageLocationList(ListView):
    model = StorageLocation

class StorageLocationDetail(DetailView):
    model = StorageLocation

class BoxDetail(DetailView):
    model = Box

class Index(TemplateView):
    template_name = "web/index.html"
