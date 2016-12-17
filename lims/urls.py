from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from lims import views

router = routers.DefaultRouter()


router.register(r'assemblys', views.AssemblyViewSet)
router.register(r'bacterias', views.BacteriaViewSet)
router.register(r'environmentalsamplecollection', views.EnvironmentalSampleCollectionViewSet)
router.register(r'environmentalsamples', views.EnvironmentalSampleViewSet)
router.register(r'experimentalresults', views.ExperimentalResultViewSet)
router.register(r'experiments', views.ExperimentViewSet)
router.register(r'lysates', views.LysateViewSet)
router.register(r'phagednapreps', views.PhageDNAPrepViewSet)
router.register(r'phages', views.PhageViewSet, base_name='phages')
router.register(r'sequencingrunpoolitems', views.SequencingRunPoolItemViewSet)
router.register(r'sequencingrunpools', views.SequencingRunPoolViewSet)
router.register(r'sequencingruns', views.SequencingRunViewSet)
router.register(r'storage/rooms', views.RoomStorageViewSet)
router.register(r'storage/container_labels', views.ContainerLabelStorageViewSet)
router.register(r'storage/boxes', views.BoxStorageViewSet)
router.register(r'storage', views.StorageViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
