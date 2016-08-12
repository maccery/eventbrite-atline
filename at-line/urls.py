from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import api.views

# Examples:
# url(r'^$', 'at-line.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', api.views.index, name='index'),
    url(r'^db', api.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
