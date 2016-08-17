from django.conf.urls import url, include
from rest_framework import routers
router = routers.DefaultRouter()

from base.views import AppViewSet
router.register(r'apps', AppViewSet)

from directory.views import PersonViewSet, OrganisationViewSet
router.register('dir/account', PersonViewSet)
router.register('dir/org', OrganisationViewSet)

from web.views import AssemblyViewSet, BacteriaViewSet, BoxViewSet, \
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
    url(r'', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'api-token-auth/','rest_framework_jwt.views.obtain_jwt_token'),
    # url(r'api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
    # url(r'api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),
]

