from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from directory.models import Organisation, PersonTag
from account.models import Account

class PersonList(ListView):
    model = Account

class PersonDetail(DetailView):
    model = Account

class OrganisationList(ListView):
    model = Organisation

class OrganisationDetail(DetailView):
    model = Organisation

class Index(TemplateView):
    template_name = "directory/index.html"

class TagDetail(DetailView):
    model = PersonTag
