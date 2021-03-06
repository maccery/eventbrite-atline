from django.db import models


class Game(models.Model):
    event_id = models.IntegerField


class Question(models.Model):
    text = models.CharField(max_length=90)
    answer = models.IntegerField(default=0)
    first_option = models.CharField(max_length=15)
    second_option = models.CharField(max_length=15)
    third_option = models.CharField(max_length=15)
    fourth_option = models.CharField(max_length=15)
    first_count = models.IntegerField
    second_count = models.IntegerField
    third_count = models.IntegerField
    fourth_count = models.IntegerField


class Prize(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    inventory_count = models.IntegerField


class Player(models.Model):
    prize = models.ManyToManyField(Prize)
    points = models.IntegerField(default=0)


class Session(models.Model):
    status = models.CharField(max_length=30, default="unavailable")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Question)
    players = models.ManyToManyField(Player)
    num_answered = models.IntegerField(default=0)
