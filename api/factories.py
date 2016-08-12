from api.models import Session, Game, Question, Player

class QuestionFactory():
    def create(self, number_of_questions):
        for i in range(0, number_of_questions):
            Question.objects.create(
                text='hey',
                # answer=1,
                first_option='hey',
                second_option='hey',
                third_option='hey',
                fourth_option='hey',
            )

class PlayerFactory():
    def create(self, session, number_of_players):
        for i in range(0, number_of_players):
            player = Player.objects.create()
            session.players.add(player)
