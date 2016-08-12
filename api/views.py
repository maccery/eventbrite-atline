from django.core import serializers
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import View
from django.http import JsonResponse
from django.forms import model_to_dict
from api import NUM_QUESTIONS_PER_SESSION
from api.models import Session, Game, Player, Question

import json
from django.views.decorators.csrf import csrf_exempt

class API(object):
    """ Generic methods for all APIs """
    def _throw_api_error(self, message):
        message = [message]
        raise Exception('Failed')

    def _check_game_id_valid(self, game_id):
        game = Game.objects.filter(pk=game_id)

        if not game:
            self._throw_api_error('No game with this ID')
        else:
            return game[0]

    def _check_session_id_valid(self, session_id):
        session = Session.objects.filter(pk=session_id)

        if not session:
            self._throw_api_error('No session with this ID')
        else:
            return session[0]


    def _check_player_id_valid(self, player_id):
        player = Player.objects.filter(pk=player_id)

        if not player:
            self._throw_api_error('No game with this ID')
        else:
            return player[0]

    def _return_as_json(self, hey):
        hey = model_to_dict(hey)
        return JsonResponse(hey, safe=False)


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

            self._throw_api_error('We need a POST request')
        else:
            self._throw_api_error('We need a POST request')

    def _add_player_to_session(self, session, player):
        session.players.add(player)
        if (len(session.players.all())) >= 6:
            session.status = 'ready'
            session.save()

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
            session_as_dict = json.loads(serializers.serialize('json', [session]))[0]
            session_as_dict['player_count'] = len(session.players.all())
            return HttpResponse(json.dumps(session_as_dict))
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
                return self._return_as_json(question)

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


class ResultsAPI(View, API):
    """ Class based view for results player API"""
    def get(self, request):
        if request.method == 'GET':
            args = {}
            session_pk = request.GET.get('session_id')
            try:
                session = Session.objects.get(pk=session_pk)
            except Session.DoesNotExist:
                self._throw_api_error('No session with this ID')

            # increment number of questions answered
            session.num_answered += 1
            session.save()

            sessions_to_render = session.players.all().values()
            return HttpResponse(json.dumps(session.players.all().values()))
        else:
            self._throw_api_error('Please make a GET request')

class AnswerAPI(View, API):
    """ Class based view for answering a question API"""
    def post(self, request):
        if request.method == 'POST':
            session_id = request.POST.get('session_id')
            player_id = request.POST.get('player_id')
            answer_id = request.POST.get('answer')

            session = self._check_session_id_valid(session_id)
            question = self._get_latest_question(session)
            player = self._check_player_id_valid(player_id)

            answered_right = self._check_answer_right(question, answer_id)
            if answered_right:
                print ('update points')
                self._update_points(player)

            return self._return_as_json(question)
        else:
            self._throw_api_error('Please make a POST request')

    def _get_latest_question(self, session):
        question_number = session.num_answered + 1
        questions = session.questions.all()

        if question_number < 0 or question_number > 4:
            self._throw_api_error('invalid question')

        return questions[question_number]

    def _check_answer_right(self, question, answer_id):
        answer_id = int(answer_id)
        print ('answer_id', answer_id)
        if answer_id > 4 or answer_id < 0:
            self._throw_api_error('Invalid answer ID')

        # check for answer
        correct_answer = question.answer
        print ("correct answer", correct_answer)
        if answer_id == correct_answer:
            print ("correct")
            return True
        else:
            return False

    def _update_points(self, player):
        player.points = player.points + 3
        player.save()
