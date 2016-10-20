from django.conf.urls import url, include
from django.contrib import admin
from directory.models import PersonTag
import tagulous.views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lims/', include('lims.urls', namespace='lims')),
    url(r'^bioproject/', include('bioproject.urls', namespace='project')),
    url(r'^directory/', include('directory.urls', namespace='directory')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^account/', include('account.urls')),
    url(r'^announcements/', include('pinax.announcements.urls', namespace='pinax_announcements')),
    url(r'^', include('lims_app.urls', namespace='base')),
    url(
        r'^api/peopletags/$',
        tagulous.views.autocomplete,
        {'tag_model': PersonTag},
        name='person_tags_autocomplete',
    ),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
