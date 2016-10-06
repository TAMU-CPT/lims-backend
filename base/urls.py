from django.conf.urls import url, include
from views import Index

from rest_framework import routers
router = routers.DefaultRouter()

from base.views import AppViewSet
router.register(r'apps', AppViewSet)

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'', include(router.urls)),
]
