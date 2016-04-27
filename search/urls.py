from django.conf.urls import url
from django.conf import settings
import search.views

# from web import views
from search.views import Index

urlpatterns = [
    url(r'^$', Index, name='index'),
]
