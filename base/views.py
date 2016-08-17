from django.shortcuts import render
from django.views.generic import TemplateView
from base.models import App
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters
from base.serializers import AppSerializer


class Index(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['apps'] = App.objects.order_by('-id').all()
        return context


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all().order_by('-priority')
    serializer_class = AppSerializer
