from django.conf.urls import url
from django.conf import settings
from views import PersonList, PersonDetail, OrganisationList, OrganisationDetail, Index

# from web import views

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^people/$', PersonList.as_view(), name='person-list'),
    url(r'^people/(?P<pk>[0-9]+)/$', PersonDetail.as_view(), name='person-detail'),
    url(r'^org/$', OrganisationList.as_view()),
    url(r'^org/(?P<pk>[0-9]+)/$', OrganisationDetail.as_view()),
]
