from django.conf.urls import url
from search.views import Index


urlpatterns = [
    url(r'', Index, name='index'),
]
