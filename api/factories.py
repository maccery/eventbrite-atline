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


class SessionFactory():
    def create(self, session, number_of_questions, num_answered):
        session.num_answered = num_answered
        session.save()
        for i in range(0, number_of_questions):
            question = Question.objects.create(answer=3)
            session.questions.add(question)

class QuestionSeeder(object):
    def seed(self):
        Question.objects.create(
            text='Who is the coolest intern at Eventbrite?',
            answer=1,
            first_option='Chris',
            second_option='Tom',
            third_option='Calvin',
            fourth_option='Liz',
        )
        Question.objects.create(
            text='How many people signed up for this event',
            answer=1,
            first_option=400,
            second_option=500,
            third_option=2000,
            fourth_option=1000,
        )
        Question.objects.create(
            text='How many people signed up for this event',
            answer=1,
            first_option=400,
            second_option=500,
            third_option=2000,
            fourth_option=1000,
        )
        Question.objects.create(
            text='How many people signed up for this event',
            answer=1,
            first_option=400,
            second_option=500,
            third_option=2000,
            fourth_option=1000,
        )
        Question.objects.create(
            text='How many people signed up for this event',
            answer=1,
            first_option=400,
            second_option=500,
            third_option=2000,
            fourth_option=1000,
        )
        Question.objects.create(
            text='How many people signed up for this event',
            answer=1,
            first_option=400,
            second_option=500,
            third_option=2000,
            fourth_option=1000,
        )
