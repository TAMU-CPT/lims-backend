from lims_app.models import App
from rest_framework import serializers


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ('name', 'description', 'url', 'hidden', 'enabled', 'icon')
