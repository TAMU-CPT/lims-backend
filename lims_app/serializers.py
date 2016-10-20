
from rest_framework import serializers
from lims_app.models import App

class AppSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = App
        fields = ('name', 'url', 'description', 'enabled', 'priority', 'hidden', 'id')
