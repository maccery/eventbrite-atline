from django.test import TestCase
from api.views import JoinAPI, SessionAPI, CreatePlayerAPI
from django.test import TestCase, RequestFactory

from mock import patch
from rest_framework.test import APIRequestFactory

from api import NUM_QUESTIONS_PER_SESSION
from api.models import Session, Game, Question, Player
from api.views import JoinAPI, QuestionAPI, SessionAPI
from factories import QuestionFactory, PlayerFactory, SessionFactory


class TestResults(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.apifactory = APIRequestFactory()
        self.api = SessionAPI()

    # Integration tests
    @patch('api.views.ResultsAPI._throw_api_error')
    def test_request_with_invalid_session_id(self, mock_throw_api_error):
        test_session = Session.objects.create(pk=200)
        self.apifactory.get('/results/', {'session_id': 321})
        self.assertTrue(mock_throw_api_error.called)

    @patch('api.views.ResultsAPI._throw_api_error')
    def test_request_with_invalid_session_id(self, mock_throw_api_error):
        test_session = Session.objects.create(pk=321)
        request = self.apifactory.get('/results/', {'session_id': 321})
        response = self.api.get(request)
        print response
        self.assertFalse(mock_throw_api_error.called)

class TestGetSession(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.apifactory = APIRequestFactory()
        self.api = SessionAPI()

    # Integration tests
    @patch('api.views.SessionAPI._throw_api_error')
    def test_request_with_invalid_session_id(self, mock_throw_api_error):
        test_session = Session.objects.create(pk=200)
        self.apifactory.get('/session/', {'session_id': 321})
        self.assertTrue(mock_throw_api_error.called)

    @patch('api.views.SessionAPI._throw_api_error')
    def test_request_with_invalid_session_id(self, mock_throw_api_error):
        test_session = Session.objects.create(pk=321)
        request = self.apifactory.get('/session/', {'session_id': 321})
        response = self.api.get(request)
        print response
        self.assertFalse(mock_throw_api_error.called)


class TestJoin(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.apifactory = APIRequestFactory()
        self.player_factory = PlayerFactory()
        self.question_factory = QuestionFactory()
        self.request = self.factory.get('/join')
        self.api = JoinAPI()

    # Unit tests
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

    # Unit tests
    @patch('api.views.JoinAPI._throw_api_error')
    def test_check_player_id_invalid(self, mock_throw_api_error):
        id_doesnt_exist = 0
        self.api._check_player_id_valid(id_doesnt_exist)
        self.assertTrue(mock_throw_api_error.called)

    @patch('api.views.JoinAPI._throw_api_error')
    def test_check_player_id_valid(self, mock_throw_api_error):
        player = Player.objects.create()
        self.api._check_player_id_valid(player.id)
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

    def test_assign_player_to_session(self):
        game = Game.objects.create()
        session = Session.objects.create(game=game)
        player = Player.objects.create()
        self.api._add_player_to_session(session, player)
        self.assertEqual(session.players.all()[0], player)
        self.assertEqual(session.status, "unavailable")

    def test_assign_questions_to_session(self):
        game = Game.objects.create()
        session = Session.objects.create(game=game)
        self.question_factory.create(NUM_QUESTIONS_PER_SESSION)

        self.api._assign_questions_to_session(session)
        questions = Question.objects.all()
        for question in session.questions.all():
            self.assertTrue([question in questions])

        # checking that we all have valid questions, that we have 6 questions
        # associated now
        self.assertEqual(len(session.questions.all()), NUM_QUESTIONS_PER_SESSION)

    # integration tests
    def test_api_with_everything_okay(self):
        # make a game and questions
        game = Game.objects.create()
        player = Player.objects.create()
        # make random questions
        self.question_factory.create(1)
        request = self.apifactory.post('/join/', {'game_id': game.id, 'player_id': player.id})
        self.api.post(request)

    def test_api_no_game_id(self):
        with self.assertRaises(Exception):
            request = self.apifactory.post('/join/', {})
            self.api.post(request)
            self.assertRaises(Exception)

    def test_api_with_everything_okay_but_get(self):
        with self.assertRaises(Exception):
            # make a game and questions
            game = Game.objects.create()
            # make random questions
            request = self.apifactory.get('/join/', {'game_id': game.id})
            self.api.post(request)


class QuestionAPITests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.apifactory = APIRequestFactory()
        self.session_factory = SessionFactory()
        self.question_factory = QuestionFactory()
        self.request = self.factory.get('/question')
        self.api = QuestionAPI()

    @patch('api.views.QuestionAPI._throw_api_error')
    def test_check_session_id_invalid(self, mock_throw_api_error):
        id_doesnt_exist = 0
        self.api._check_session_id_valid(id_doesnt_exist)
        self.assertTrue(mock_throw_api_error.called)

    @patch('api.views.QuestionAPI._throw_api_error')
    def test_check_session_id_valid(self, mock_throw_api_error):
        session = Session.objects.create()
        self.api._check_session_id_valid(session.id)
        self.assertFalse(mock_throw_api_error.called)

    # integration tests
    def test_api_max_questions_not_answered(self):
        session = Session.objects.create()
        self.session_factory.create(session, NUM_QUESTIONS_PER_SESSION, 1)
        request = self.apifactory.post('/question/', {'session_id': session.id})
        response = self.api.post(request)
        self.assertEqual(1, session.num_answered)

    def test_api_all_questions_answered(self):
        session = Session.objects.create()
        self.session_factory.create(session, NUM_QUESTIONS_PER_SESSION, NUM_QUESTIONS_PER_SESSION)
        request = self.apifactory.post('/question/', {'session_id': session.id})
        response = self.api.post(request)
        self.assertEqual(NUM_QUESTIONS_PER_SESSION, session.num_answered)

    def test_api_no_session_id(self):
        with self.assertRaises(Exception):
            request = self.apifactory.post('/question/', {})
            self.api.post(request)
            self.assertRaises(Exception)

    def test_api_with_everything_okay_but_get(self):
        with self.assertRaises(Exception):
            session = Session.objects.create()
            request = self.apifactory.get('/question/', {'session_id': session.id})
            self.api.post(request)


class TestCreatePlayer(TestCase):
    def setUp(self):
        self.api = CreatePlayerAPI()
        self.apifactory = APIRequestFactory()

    def test_create_player(self):
        player = self.api._create_new_player()
        self.assertIsInstance(player, Player)

    def test_api(self):
        request = self.apifactory.post('/create_player/', {})
        response = self.api.post(request)
        print response
