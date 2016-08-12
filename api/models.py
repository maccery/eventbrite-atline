from django.db import models


class Game(models.Model):
    event_id = models.IntegerField(default=0)


class Question(models.Model):
    text = models.CharField(max_length=90)
    answer = models.IntegerField(default=0)
    first_option = models.CharField(max_length=15)
    second_option = models.CharField(max_length=15)
    third_option = models.CharField(max_length=15)
    fourth_option = models.CharField(max_length=15)
    first_count = models.IntegerField(default=0)
    second_count = models.IntegerField(default=0)
    third_count = models.IntegerField(default=0)
    fourth_count = models.IntegerField(default=0)


class Prize(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=90, default='')
    inventory_count = models.IntegerField(default=0)


class Player(models.Model):
    prize = models.ManyToManyField(Prize)


class Session(models.Model):
    status = models.CharField(max_length=30, default="unavailable")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Question)
    players = models.ManyToManyField(Player)
    num_answered = models.IntegerField(default=0)
