from django.conf.urls import url
from django.conf import settings
import search.views

# from web import views

urlpatterns = [
    url(r'^$', 'search.views.Index', name='index'),
]
