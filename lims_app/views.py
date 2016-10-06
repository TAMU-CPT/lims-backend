from django.views.generic import TemplateView
from lims_app.models import App
from lims_app.serializers import AppSerializer
from rest_framework import viewsets


class Index(TemplateView):
    template_name = "lims_app/index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['apps'] = App.objects.order_by('-id').all()
        return context


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all().order_by('-priority')
    serializer_class = AppSerializer
