import api.views

from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
from django.views.decorators.csrf import csrf_exempt


# Examples:
# url(r'^$', 'at-line.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^join/', csrf_exempt(api.views.JoinAPI.as_view()), name='join'),
    url(r'^question/', csrf_exempt(api.views.QuestionAPI.as_view()), name='question'),
    url(r'^session/', csrf_exempt(api.views.SessionAPI.as_view()), name='session'),
    url(r'^create_player/', csrf_exempt(api.views.CreatePlayerAPI.as_view()), name='create_player'),
    url(r'^results/', csrf_exempt(api.views.ResultsAPI.as_view()), name='result'),
    url(r'^answer/', csrf_exempt(api.views.AnswerAPI.as_view()), name='answer'),
]
