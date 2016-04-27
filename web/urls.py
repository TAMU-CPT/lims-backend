from django.conf.urls import url
from django.conf import settings
from views import \
    StorageLocationList, StorageLocationDetail, StorageLocationCreate, StorageLocationEdit, StorageLocationDelete, \
    ExperimentList, ExperimentDetail, \
    ExperimentalResultList, ExperimentalResultDetail, \
    BoxList, BoxDetail, BoxCreate, BoxEdit, BoxDelete, \
    LIMSDataDump, \
    Index

# from web import views

urlpatterns = [
    url(r'^$',                                         Index.as_view(),                   name='index'),
    url(r'^storage_location/$',                        StorageLocationList.as_view(),     name='storage-location-list'),
    url(r'^storage_location/create$',                  StorageLocationCreate.as_view(),   name='storage-location-create'),
    url(r'^storage_location/(?P<pk>[0-9]+)/$',         StorageLocationDetail.as_view(),   name='storage-location-detail'),
    url(r'^storage_location/(?P<pk>[0-9]+)/edit$',     StorageLocationEdit.as_view(),     name='storage-location-edit'),
    url(r'^storage_location/(?P<pk>[0-9]+)/delete$',   StorageLocationDelete.as_view(),   name='storage-location-delete'),

    url(r'^dump', LIMSDataDump.as_view(), name='lims-data-dump'),

    url(r'^box$',                                                                   BoxList.as_view(),     name='box-list'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/create$',                  BoxCreate.as_view(),   name='box-create'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/$',         BoxDetail.as_view(),   name='box-detail'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/edit$',     BoxEdit.as_view(),     name='box-edit'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/delete$',   BoxDelete.as_view(),   name='box-delete'),

    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/add/env_sample',     BoxDelete.as_view(),   name='env-sample-create'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/add/lysate',         BoxDelete.as_view(),   name='lysate-create'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/add/phage_dna_prep', BoxDelete.as_view(),   name='phage-dna-prep-create'),

    url(r'^experiment/$', ExperimentList.as_view(), name='experiment-list'),
    url(r'^experiment/(?P<pk>[0-9a-f-]{36})/$', ExperimentDetail.as_view(), name='experiment-detail'),

    # url(r'^experiment-result/$', ExperimentalResultList.as_view(), name='experiment-result-list'),
    url(r'^experiment-result/(?P<pk>[0-9a-f-]{36})/$', ExperimentalResultDetail.as_view(), name='experiment-result-detail'),
]
