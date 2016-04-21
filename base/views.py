from django.shortcuts import render
from django.views.generic import TemplateView
from base.models import App


class Index(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['apps'] = App.objects.order_by('-id').all()
        return context
