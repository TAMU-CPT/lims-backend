from django.conf.urls import url
from django.conf import settings
from views import \
    StorageLocationList, StorageLocationDetail, \
    BoxDetail, \
    Index

# from web import views

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^storage_location/$', StorageLocationList.as_view(), name='storage-location-list'),
    url(r'^storage_location/(?P<pk>[0-9]+)/$', StorageLocationDetail.as_view(), name='storage-location-detail'),
    url(r'^box/(?P<pk>[0-9]+)/$', BoxDetail.as_view(), name='box-detail'),
]
