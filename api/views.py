from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
from api.models import Session, Game, Player, Question
from django.db.models import Count
from django.views.generic import View
import json

class API(object):
    """ Generic methods for all APIs """
    def _throw_api_error(self, message):
        message = [message]
        raise Exception('ERROR')

    def _check_game_id_valid(self, game_id):
        game = Game.objects.filter(pk=game_id)

        if not game:
            self._throw_api_error('No game with this ID')
        else:
            return game[0]

    def _return_as_json(self, object):
        return serializers.serialize('json', [object,])

class JoinAPI(View, API):
    """ Class based viewed for /join endpoint"""
    def post(self, request):
        if request.method == 'POST':
            game_id = request.POST.get('game_id')
            player_id = request.POST.get('player_id')

            # check if the game id is valid
            game = self._check_game_id_valid(game_id)

            # Find available sessions
            session = self._get_or_create_session(game)
            # Get 6 random questions and add it to the session
            self._assign_questions_to_session(session)
            # Add player to session
            player = self._check_player_id_valid(player_id)
            self._add_player_to_session(session, player)

            return serializers.serialize('json', [session,])
        else:
            self._throw_api_error('We need a POST request')

    def _add_player_to_session(self, session, player):
        session.players.add(player)
        if (len(session.players.all())) >= 6:
            session.status = 'ready'
            session.save()

    def _check_player_id_valid(self, player_id):
        player = Player.objects.filter(pk=player_id)

        if not player:
            self._throw_api_error('No game with this ID')
        else:
            return player[0]

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

class SessionAPI(View, API):
    def get(self, request):
        if request.method == 'GET':
            # Session id and primary key in this case are the same thing
            session_pk = request.GET.get('session_id')
            try:
                session = Session.objects.get(pk=session_pk)
            except Session.DoesNotExist:
                self._throw_api_error('No session with this ID')
            session_as_dict = json.loads(serializers.serialize('json', [session]))[0]
            session_as_dict['player_count'] = len(session.players.all())
            return HttpResponse(json.dumps(session_as_dict))
        else:
            self._throw_api_error('We need a GET request')

class CreatePlayerAPI(View, API):
    """ Class based view for create player API"""
    def post(self, request):
        if request.method == 'POST':
            player = self._create_new_player()
            return self._return_as_json(player)
        else:
            self._throw_api_error('Please make a POST request')

    def _create_new_player(self):
        return Player.objects.create()
