from django.conf.urls import url, include
from django.contrib import admin
# from directory.models import PersonTag
# import tagulous.views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^lims/', include('lims.urls')),
    url(r'^bioproject/', include('bioproject.urls')),
    url(r'^directory/', include('directory.urls')),
    url(r'^search/', include('search.urls')),

    # url(r'^announcements/', include('pinax.announcements.urls')),
    # url(
        # r'^api/peopletags/$',
        # tagulous.views.autocomplete,
        # {'tag_model': PersonTag},
        # name='person_tags_autocomplete',
    # ),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
