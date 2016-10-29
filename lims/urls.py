from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from lims import views

router = routers.DefaultRouter()


router.register(r'boxs', views.BoxViewSet)
router.register(r'storagelocations', views.StorageLocationViewSet)
router.register(r'assemblys', views.AssemblyViewSet)
router.register(r'tubetypes', views.TubeTypeViewSet)
router.register(r'experimentalresults', views.ExperimentalResultViewSet)
router.register(r'sequencingruns', views.SequencingRunViewSet)
router.register(r'tubes', views.TubeViewSet)
router.register(r'sampletypes', views.SampleTypeViewSet)
router.register(r'experiments', views.ExperimentViewSet)
router.register(r'phages', views.PhageViewSet, base_name='phages')
router.register(r'phagednapreps', views.PhageDNAPrepViewSet)
router.register(r'sequencingrunpools', views.SequencingRunPoolViewSet)
router.register(r'sequencingrunpoolitems', views.SequencingRunPoolItemViewSet)
router.register(r'containertypes', views.ContainerTypeViewSet)
router.register(r'environmentalsamples', views.EnvironmentalSampleViewSet)
router.register(r'lysates', views.LysateViewSet)
router.register(r'bacterias', views.BacteriaViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
