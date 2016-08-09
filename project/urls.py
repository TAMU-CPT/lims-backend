from django.conf.urls import url
from django.conf import settings
from project.views import *

# from web import views

urlpatterns = [

    url(r'^$',                        BioprojectList.as_view(),     name='bioproject-list'),
    url(r'^create$',                  BioprojectCreate.as_view(),   name='bioproject-create'),
    url(r'^(?P<pk>[0-9]+)/$',         BioprojectDetail.as_view(),   name='bioproject-detail'),
    url(r'^(?P<pk>[0-9]+)/edit$',     BioprojectEdit.as_view(),     name='bioproject-edit'),
    url(r'^(?P<pk>[0-9]+)/delete$',   BioprojectDelete.as_view(),   name='bioproject-delete'),
    # url(r'^$', views.index, name='index'),
    # url(r'progress/(?P<iteration_id>[0-9]+)/', views.iteration_progress, name='iter_prog'),
    # url(r'assessment/(?P<assessment_id>[0-9]+)/', views.assessment_progress, name='assess_prog'),
    # url(r'^submit$', views.submit),
]
