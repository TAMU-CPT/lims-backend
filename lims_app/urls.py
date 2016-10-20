from django.conf.urls import url, include
from rest_framework import routers
from lims_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'apps', views.AppViewSet)

urlpatterns = [
    url(r'^lims_app/', include(router.urls)),
]