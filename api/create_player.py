from api.views import API
from api.models import Player

class CreatePlayerAPI(API):
    """ Class based view for create player API"""
    def post(self, request):
        if request.method == 'POST':
            player = self._create_new_player()
            return self._return_as_json(player)
        else:
            self._throw_api_error('Please make a POST request')

    def _create_new_player(self):
        return Player.objects.create()
