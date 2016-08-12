from django.shortcuts import render_to_response
from django.http import HttpResponse

from api.models import Session, Game, Question
from django.db.models import Count


def join(request):
    game_id = request.get.GET('game_id')

    # check if the game id is valid
    game = Game(pk=game_id)
    if not game:
        render_to_response({'Invalid game id'})

    # Find available sessions
    available_session = Session.objects.annotate(players_count=Count('players')).filter(players_count__lte=7).count()

    # If none available create one and return that
    if available_session:
        session = available_session

    else:
        session = Session(game_id=game_id)
        session.save()

        # Get 6 random questions and add it to the session
        questions = Question.objects.all().order_by('?')[:6]
        session.related_set.set(questions)

    return render_to_response(session)
