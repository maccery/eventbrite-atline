import api.views

from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()


# Examples:
# url(r'^$', 'at-line.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^join/', api.views.JoinAPI.as_view(), name='join'),
    url(r'^question/', api.views.QuestionAPI.as_view(), name='question'),
    url(r'^session/', api.views.SessionAPI.as_view(), name='session'),
]
