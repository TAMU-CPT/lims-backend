from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django import forms
from easy_select2 import apply_select2
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
import tagulous

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

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

class PersonCreate(CreateView):
    model = Account
    fields = ('name', 'initials', 'nickname', 'netid', 'phone_number', 'tags', 'orcid', 'orgs')
    success_url = reverse_lazy('directory:person-list')

    def form_valid(self, form):
        import pprint; pprint.pprint(form.data)
        import pprint; pprint.pprint(form.cleaned_data)
        raise Exception('asdf')

        self.object = form.save(commit=False)
        # import pprint; pprint.pprint(dir(self.object))

        name = form.data['name'].lower().replace(' ', '_')
        # Set up the user object
        u = User.objects.get_or_create(
            username=name
        )
        print u


        # self.object.course = self.course
        # self.object.save()
        success_url = reverse_lazy('person-list')
        return HttpResponseRedirect(reverse_lazy('directory:person-list'))
