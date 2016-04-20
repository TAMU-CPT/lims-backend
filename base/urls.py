from django.conf.urls import url
from django.conf import settings
from views import Index

# from web import views

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
]
