from django.conf.urls import url, include
from views import Index, AppViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'apps', AppViewSet)

# from web import views

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),

    url(r'api/', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'api-token-auth/','rest_framework_jwt.views.obtain_jwt_token'),
    # url(r'api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
    # url(r'api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),
]
