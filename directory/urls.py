from django.conf.urls import url
from django.conf import settings
from views import PersonList, PersonDetail, OrganisationList, OrganisationDetail, Index, TagDetail

# from web import views

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^people/$', PersonList.as_view(), name='person-list'),
    url(r'^people/(?P<pk>[0-9]+)/$', PersonDetail.as_view(), name='person-detail'),
    url(r'^org/$', OrganisationList.as_view(), name='org-list'),
    url(r'^org/(?P<pk>[0-9]+)/$', OrganisationDetail.as_view(), name='org-detail'),
    url(r'^tag/(?P<pk>[0-9]+)/$', TagDetail.as_view(), name='tag-detail'),
]
