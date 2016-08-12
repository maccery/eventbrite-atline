from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import api.views

# Examples:
# url(r'^$', 'at-line.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^join/', api.views.JoinAPI.as_view(), name='join'),
    url(r'^session/', api.views.SessionAPI.as_view(), name='session'),
    url(r'^create_player/', api.create_player.CreatePlayerAPI.as_view(), name='create_player'),
]
