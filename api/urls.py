from django.conf.urls import url, include
from rest_framework import routers
router = routers.DefaultRouter()

from base.views import AppViewSet
router.register(r'apps', AppViewSet)

from directory.views import PersonViewSet, OrganisationViewSet
router.register('dir/account', PersonViewSet)
router.register('dir/org', OrganisationViewSet)


urlpatterns = [
    url(r'', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'api-token-auth/','rest_framework_jwt.views.obtain_jwt_token'),
    # url(r'api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
    # url(r'api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),
]

