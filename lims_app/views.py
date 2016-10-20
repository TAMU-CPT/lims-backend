from rest_framework import viewsets

from .serializers import lims_appAppSerializer
from lims_app.models import App

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
