from django.conf.urls import url
from django.conf import settings
from views import \
    StorageLocationList, StorageLocationDetail, \
    ExperimentList, ExperimentDetail, \
    ExperimentalResultList, ExperimentalResultDetail, \
    BoxDetail, \
    LIMSDataDump, \
    Index

# from web import views

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^storage_location/$', StorageLocationList.as_view(), name='storage-location-list'),
    url(r'^storage_location/(?P<pk>[0-9]+)/$', StorageLocationDetail.as_view(), name='storage-location-detail'),

    url(r'^dump', LIMSDataDump.as_view(), name='lims-data-dump'),
    url(r'^box/(?P<pk>[0-9]+)/$', BoxDetail.as_view(), name='box-detail'),

    url(r'^experiment/$', ExperimentList.as_view(), name='experiment-list'),
    url(r'^experiment/(?P<pk>[0-9a-f-]{36})/$', ExperimentDetail.as_view(), name='experiment-detail'),

    # url(r'^experiment-result/$', ExperimentalResultList.as_view(), name='experiment-result-list'),
    url(r'^experiment-result/(?P<pk>[0-9a-f-]{36})/$', ExperimentalResultDetail.as_view(), name='experiment-result-detail'),
]
