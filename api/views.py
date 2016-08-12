from django.core import serializers
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import View

from api import NUM_QUESTIONS_PER_SESSION
from api.models import Session, Game, Player, Question


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
            self._throw_api_error('We need a POST request')

    def _check_game_id_valid(self, game_id):
        game = Game.objects.filter(pk=game_id)

        if not game:
            self._throw_api_error('No game with this ID')
        else:
            return game[0]

    def _assign_questions_to_session(self, session):
        questions = Question.objects.all().order_by('?')[:NUM_QUESTIONS_PER_SESSION]
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
            return HttpResponse(serializers.serialize('json', [session]))
        else:
            self._throw_api_error('We need a GET request')


class QuestionAPI(View, API):

    def post(self, request):
        if request.method == 'POST':
            session_id = request.POST.get('session_id')

            # Check if session ID is valid
            session = self._check_session_id_valid(session_id)
            # Check if user has answered max questions permitted per session
            if session.num_answered < NUM_QUESTIONS_PER_SESSION:
                # Grab all questions associated given session ID
                set_of_questions = session.questions.all()
                # Send a question
                question = set_of_questions[session.num_answered]
                return serializers.serialize('json', [question,])

            # If max questions reached, then mark session as complete
            elif session.num_answered == NUM_QUESTIONS_PER_SESSION:
                Session.objects.filter(pk=session_id).update(status='complete')
        else:
            self._throw_api_error('We need a POST request')

    def _check_session_id_valid(self, session_id):
        session = Session.objects.filter(pk=session_id)

        if not session:
            self._throw_api_error('No session with this ID')
        else:
            return session[0]
