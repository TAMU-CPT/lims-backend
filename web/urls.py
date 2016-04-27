from django.conf.urls import url
from django.conf import settings
from views import \
    StorageLocationList, StorageLocationDetail, StorageLocationCreate, StorageLocationEdit, StorageLocationDelete, \
    ExperimentList, ExperimentDetail, \
    ExperimentalResultList, ExperimentalResultDetail, \
    BoxList, BoxDetail, BoxCreate, BoxEdit, BoxDelete, \
    EnvSample_create, EnvSample_list, EnvSample_view, EnvSample_edit, EnvSample_delete, \
    Lysate_create, Lysate_list, Lysate_view, Lysate_edit, Lysate_delete, \
    PhageDNAPrep_create, PhageDNAPrep_list, PhageDNAPrep_view, PhageDNAPrep_edit, PhageDNAPrep_delete, \
    LIMSDataDump, \
    Index


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

    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/env_sample/create',     EnvSample_create.as_view(),    name='env-sample-create'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/lysate/create',         Lysate_create.as_view(),       name='lysate-create'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/phage_dna_prep/create', PhageDNAPrep_create.as_view(), name='phage-dna-prep-create'),

    url(r'^env_sample/',                          EnvSample_list.as_view(),     name='env-sample-list'),
    url(r'^env_sample/(?P<pk>[0-9]+)',            EnvSample_view.as_view(),     name='env-sample-detail'),
    url(r'^env_sample/(?P<pk>[0-9]+)/edit',       EnvSample_edit.as_view(),     name='env-sample-edit'),
    url(r'^env_sample/(?P<pk>[0-9]+)/delete',     EnvSample_delete.as_view(),   name='env-sample-delete'),

    url(r'^lysate/',                              Lysate_list.as_view(),        name='lysate-list'),
    url(r'^lysate/(?P<pk>[0-9]+)',                Lysate_view.as_view(),        name='lysate-detail'),
    url(r'^lysate/(?P<pk>[0-9]+)/edit',           Lysate_edit.as_view(),        name='lysate-edit'),
    url(r'^lysate/(?P<pk>[0-9]+)/delete',         Lysate_delete.as_view(),      name='lysate-delete'),

    url(r'^phage_dna_prep/',                      PhageDNAPrep_list.as_view(),   name='phage-dna-prep-list'),
    url(r'^phage_dna_prep/(?P<pk>[0-9]+)',        PhageDNAPrep_view.as_view(),   name='phage-dna-prep-detail'),
    url(r'^phage_dna_prep/(?P<pk>[0-9]+)/edit',   PhageDNAPrep_edit.as_view(),   name='phage-dna-prep-edit'),
    url(r'^phage_dna_prep/(?P<pk>[0-9]+)/delete', PhageDNAPrep_delete.as_view(), name='phage-dna-prep-delete'),

    url(r'^experiment/$', ExperimentList.as_view(), name='experiment-list'),
    url(r'^experiment/(?P<pk>[0-9a-f-]{36})/$', ExperimentDetail.as_view(), name='experiment-detail'),

    # url(r'^experiment-result/$', ExperimentalResultList.as_view(), name='experiment-result-list'),
    url(r'^experiment-result/(?P<pk>[0-9a-f-]{36})/$', ExperimentalResultDetail.as_view(), name='experiment-result-detail'),
]
