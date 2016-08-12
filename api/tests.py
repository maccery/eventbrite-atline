from django.test import TestCase
from api.views import JoinAPI
from django.test import TestCase, RequestFactory
from api.models import Session, Game, Question, Player
from mock import patch
from rest_framework.test import APIRequestFactory
from factories import QuestionFactory, PlayerFactory


class TestJoin(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.question_factory = QuestionFactory()
        self.player_factory = PlayerFactory()
        self.apifactory = APIRequestFactory()
        self.request = self.factory.get('/join')
        self.api = JoinAPI()

    # unit tests
    @patch('api.views.JoinAPI._throw_api_error')
    def test_check_game_id_invalid(self, mock_throw_api_error):
        id_doesnt_exist = 0
        self.api._check_game_id_valid(id_doesnt_exist)
        self.assertTrue(mock_throw_api_error.called)

    @patch('api.views.JoinAPI._throw_api_error')
    def test_check_game_id_valid(self, mock_throw_api_error):
        game = Game.objects.create()
        self.api._check_game_id_valid(game.id)
        self.assertFalse(mock_throw_api_error.called)

    def test_get_or_create_session_no_session(self):
        game = Game.objects.create()
        session = self.api._get_or_create_session(game)
        self.assertIsInstance(session, Session)

    def test_get_or_create_session_available_session(self):
        # make a session which is available
        game = Game.objects.create()
        expected_session = Session.objects.create(game=game)
        actual_session = self.api._get_or_create_session(game)
        self.assertEqual(expected_session, actual_session)

    def test_get_or_create_session_unavailable_session(self):
        # make a session which is unavailable - 8 ppl assigned
        game = Game.objects.create()
        unexpected_session = Session.objects.create(game=game)
        self.player_factory.create(unexpected_session, 8)

        actual_session = self.api._get_or_create_session(game)
        self.assertNotEqual(unexpected_session, actual_session)

    def test_get_or_create_session_available_session(self):
        # make a session which is available - 4 ppl assigned
        game = Game.objects.create()
        expected_session = Session.objects.create(game=game)
        self.player_factory.create(expected_session, 4)

        actual_session = self.api._get_or_create_session(game)
        self.assertEqual(expected_session, actual_session)

    def test_get_or_create_session_multiple_available_session(self):
        # multiple sessions available, we expect it to be the latest session
        game = Game.objects.create()
        another_session = Session.objects.create(game=game)
        expected_session = Session.objects.create(game=game)
        self.player_factory.create(expected_session, 4)

        actual_session = self.api._get_or_create_session(game)
        self.assertEqual(expected_session, actual_session)
        self.assertNotEqual(another_session, actual_session)

    def test_assign_questions_to_session(self):
        game = Game.objects.create()
        session = Session.objects.create(game=game)
        self.question_factory.create(6)

        self.api._assign_questions_to_session(session)
        questions = Question.objects.all()
        for question in session.questions.all():
            self.assertTrue([question in questions])

        # checking that we all have valid questions, that we have 6 questions
        # associated now
        self.assertEqual(len(session.questions.all()), 6)

    # integration tests
    def test_api_with_everything_okay(self):
        # make a game and questions
        game = Game.objects.create()
        # make random questions
        self.question_factory.create(1)
        request = self.apifactory.post('/join/', {'game_id': game.id})
        self.api.post(request)

    def test_api_no_game_id(self):
        with self.assertRaises(Exception):
            request = self.apifactory.post('/join/', {})
            self.api.post(request)
            self.assertRaises(Exception)

    # integration tests
    def test_api_with_everything_okay_but_get(self):
        with self.assertRaises(Exception):
            # make a game and questions
            game = Game.objects.create()
            # make random questions
            request = self.apifactory.get('/join/', {'game_id': game.id})
            self.api.post(request)
