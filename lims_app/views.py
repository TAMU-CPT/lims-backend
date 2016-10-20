from rest_framework import viewsets

from lims_app.serializers import AppSerializer
from lims_app.models import App

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
