from django.shortcuts import render
from models import Bioproject
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy

class BioprojectList(ListView):
    model = Bioproject

class BioprojectDetail(DetailView):
    model = Bioproject

class BioprojectCreate(CreateView):
    model = Bioproject
    fields = ('name', 'description', 'sample')
    success_url = reverse_lazy('project:bioproject-list')

class BioprojectEdit(UpdateView):
    model = Bioproject
    fields = ('name', 'description', 'sample')
    success_url = reverse_lazy('project:bioproject-list')

class BioprojectDelete(DeleteView):
    model = Bioproject
    success_url = reverse_lazy('project:bioproject-list')
