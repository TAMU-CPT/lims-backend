from django.conf.urls import url, include
from rest_framework import routers
from directory import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# router.register(r'persontags', views.PersonTagViewSet)
router.register(r'organisations', views.OrganisationViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
