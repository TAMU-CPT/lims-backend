from django.conf.urls import url
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

from views import BacteriaList, BacteriaDetail, BacteriaCreate, BacteriaEdit, BacteriaDelete

from django.conf.urls import include
from rest_framework import routers
router = routers.DefaultRouter()

from lims.views import AssemblyViewSet, BacteriaViewSet, BoxViewSet, \
    ContainerTypeViewSet, EnvironmentalSampleViewSet, ExperimentViewSet, \
    ExperimentalResultViewSet, LysateViewSet, PhageDNAPrepViewSet, \
    SampleTypeViewSet, SequencingRunViewSet, SequencingRunPoolViewSet, \
    SequencingRunPoolItemViewSet, StorageLocationViewSet, TubeViewSet, \
    TubeTypeViewSet

router.register('web/assembly', AssemblyViewSet)
router.register('web/bacteria', BacteriaViewSet)
router.register('web/box', BoxViewSet)
router.register('web/containertype', ContainerTypeViewSet)
router.register('web/environmentalsample', EnvironmentalSampleViewSet)
router.register('web/experiment', ExperimentViewSet)
router.register('web/experimentalresult', ExperimentalResultViewSet)
router.register('web/lysate', LysateViewSet)
router.register('web/phagednaprep', PhageDNAPrepViewSet)
router.register('web/sampletype', SampleTypeViewSet)
router.register('web/sequencingrun', SequencingRunViewSet)
router.register('web/sequencingrunpool', SequencingRunPoolViewSet)
router.register('web/sequencingrunpoolitem', SequencingRunPoolItemViewSet)
router.register('web/storagelocation', StorageLocationViewSet)
router.register('web/tube', TubeViewSet)
router.register('web/tubetype', TubeTypeViewSet)


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

    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/env_sample/create$',     EnvSample_create.as_view(),    name='envsample-create'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/lysate/create$',         Lysate_create.as_view(),       name='lysate-create'),
    url(r'^storage_location/(?P<container_id>[0-9]+)/box/(?P<pk>[0-9]+)/phage_dna_prep/create$', PhageDNAPrep_create.as_view(), name='phagednaprep-create'),

    url(r'^env_sample/$',                          EnvSample_list.as_view(),     name='envsample-list'),
    url(r'^env_sample/(?P<pk>[0-9]+)$',            EnvSample_view.as_view(),     name='envsample-detail'),
    url(r'^env_sample/(?P<pk>[0-9]+)/edit$',       EnvSample_edit.as_view(),     name='envsample-edit'),
    url(r'^env_sample/(?P<pk>[0-9]+)/delete$',     EnvSample_delete.as_view(),   name='envsample-delete'),

    url(r'^lysate/$',                              Lysate_list.as_view(),        name='lysate-list'),
    url(r'^lysate/(?P<pk>[0-9]+)$',                Lysate_view.as_view(),        name='lysate-detail'),
    url(r'^lysate/(?P<pk>[0-9]+)/edit$',           Lysate_edit.as_view(),        name='lysate-edit'),
    url(r'^lysate/(?P<pk>[0-9]+)/delete$',         Lysate_delete.as_view(),      name='lysate-delete'),

    url(r'^phage_dna_prep/$',                      PhageDNAPrep_list.as_view(),   name='phagednaprep-list'),
    url(r'^phage_dna_prep/(?P<pk>[0-9]+)$',        PhageDNAPrep_view.as_view(),   name='phagednaprep-detail'),
    url(r'^phage_dna_prep/(?P<pk>[0-9]+)/edit$',   PhageDNAPrep_edit.as_view(),   name='phagednaprep-edit'),
    url(r'^phage_dna_prep/(?P<pk>[0-9]+)/delete$', PhageDNAPrep_delete.as_view(), name='phagednaprep-delete'),


    url(r'^bacteria/$',                          BacteriaList.as_view(),     name='bacteria-list'),
    url(r'^bacteria/create$',                    BacteriaCreate.as_view(),   name='bacteria-create'),
    url(r'^bacteria/(?P<pk>[0-9]+)$',            BacteriaDetail.as_view(),     name='bacteria-detail'),
    url(r'^bacteria/(?P<pk>[0-9]+)/edit$',       BacteriaEdit.as_view(),     name='bacteria-edit'),
    url(r'^bacteria/(?P<pk>[0-9]+)/delete$',     BacteriaDelete.as_view(),   name='bacteria-delete'),



    url(r'^experiment/$', ExperimentList.as_view(), name='experiment-list'),
    url(r'^experiment/(?P<pk>[0-9a-f-]{36})/$', ExperimentDetail.as_view(), name='experiment-detail'),

    url(r'^experiment-result/$', ExperimentalResultList.as_view(), name='experiment-result-list'),
    url(r'^experiment-result/(?P<pk>[0-9a-f-]{36})/$', ExperimentalResultDetail.as_view(), name='experiment-result-detail'),


    url(r'', include(router.urls)),
]
