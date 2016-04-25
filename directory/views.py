from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from directory.models import Organisation, Person, PersonTag

class PersonList(ListView):
    model = Person

class PersonDetail(DetailView):
    model = Person

class OrganisationList(ListView):
    model = Organisation

class OrganisationDetail(DetailView):
    model = Organisation

class Index(TemplateView):
    template_name = "directory/index.html"

class TagDetail(DetailView):
    model = PersonTag
