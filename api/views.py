from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers

from api.models import Session, Game, Question
from django.db.models import Count


class JoinAPI(object):

    def join(self, request):
        if request.method == 'POST':
            game_id = request.POST.get('game_id')

            # check if the game id is valid
            self._check_game_id_valid(game_id)
            # Find available sessions
            session = self._get_or_create_session(game_id)
            # Get 6 random questions and add it to the session
            self._assign_questions_to_session(session)

            return serializers.serialize('json', session)
        else:
            self._throw_api_error('We need a GET request')

    def _check_game_id_valid(self, game_id):
        game = Game.objects.filter(pk=game_id)

        if not game:
            self._throw_api_error('No game with this ID')

    def _assign_questions_to_session(self, session):
        questions = Question.objects.all().order_by('?')[:6]
        print dir(session)
        session.related_set.set(questions)

    def _get_or_create_session(self, game_id):
        available_session = Session.objects.annotate(players_count=Count('players')).filter(players_count__lte=7).count()

        if available_session:
            session = available_session

        else:
            session = Session.objects.create(game_id=game_id)
            session.save()

        return session

    def _throw_api_error(self, message):
        message = [message]

        return message
