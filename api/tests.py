from django.test import TestCase
from api.views import JoinAPI
from django.test import TestCase, RequestFactory
from api.models import Session, Game, Question
from mock import patch
from rest_framework.test import APIRequestFactory

class TestJoin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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

    def test_join_with_post(self):

        pass

    def test_join_with_get(self):
        pass

    # integration tests
    def test_api_with_everything_okay(self):
        # make a game and questions
        #game = Game.objects.create(event_id='6')
        # make random questions
        questions = Question.objects.create(
            text='hey',
            answer=1,
            first_option='hey',
            second_option='hey',
            third_option='hey',
            fourth_option='hey',
        )


        request = self.apifactory.post('/join/', {'title': 'new idea'})
        response = self.api.join(request)
        print response
