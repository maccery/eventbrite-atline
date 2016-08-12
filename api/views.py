from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
from api.models import Session, Game, Player, Question
from django.db.models import Count
from django.views.generic import View


class API(object):
    """ Generic methods for all APIs """
    def _throw_api_error(self, message):
        message = [message]
        raise Exception('ERROR')


class JoinAPI(View, API):
    """ Class based viewed for /join endpoint"""

    def post(self, request):
        if request.method == 'POST':
            game_id = request.POST.get('game_id')

            # check if the game id is valid
            game = self._check_game_id_valid(game_id)

            # Find available sessions
            session = self._get_or_create_session(game)
            # Get 6 random questions and add it to the session
            self._assign_questions_to_session(session)

            return serializers.serialize('json', [session,])
        else:
            self._throw_api_error('We need a GET request')

    def _check_game_id_valid(self, game_id):
        game = Game.objects.filter(pk=game_id)

        if not game:
            self._throw_api_error('No game with this ID')
        else:
            return game[0]

    def _assign_questions_to_session(self, session):
        questions = Question.objects.all().order_by('?')[:6]
        session.questions.set(questions)

    def _get_or_create_session(self, game):
        available_session = Session.objects.annotate(players_count=Count('players')).filter(players_count__lte=7).count()

        if available_session:
            session = Session.objects.filter(pk=available_session)[0]

        else:
            session = Session.objects.create(game=game)

        return session
