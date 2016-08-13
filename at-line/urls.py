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
    url(r'^join/', api.views.JoinAPI.as_view(), name='join'),
    url(r'^question/', api.views.QuestionAPI.as_view(), name='question'),
    url(r'^session/', api.views.SessionAPI.as_view(), name='session'),
    url(r'^create_player/', api.views.CreatePlayerAPI.as_view(), name='create_player'),
    url(r'^prizes_game/', api.views.PrizesforGameAPI.as_view(), name='prizes_game'),
    url(r'^prizes_player/', api.views.PrizesforPlayerAPI.as_view(), name='prizes_player'),
    url(r'^create_game/', csrf_exempt(api.views.CreateGameAPI.as_view()), name='create_game'),
    url(r'^results/', csrf_exempt(api.views.ResultsAPI.as_view()), name='result'),
    url(r'^answer/', csrf_exempt(api.views.AnswerAPI.as_view()), name='answer'),
    url(r'^question_seeder/', csrf_exempt(api.views.CreateQuestions.as_view()), name='question_seeder'),
]
