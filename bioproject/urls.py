from django.conf.urls import url, include
from rest_framework import routers
from bioproject import views

router = routers.DefaultRouter()


router.register(r'editingroleusers', views.EditingRoleUserViewSet)
router.register(r'editingrolegroups', views.EditingRoleGroupViewSet)
router.register(r'bioprojects', views.BioprojectViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
