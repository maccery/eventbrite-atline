from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=90)
    answer = models.IntegerField(max_length=1)
    first_option = models.CharField(max_length=15)
    second_option = models.CharField(max_length=15)
    third_option = models.CharField(max_length=15)
    fourth_option = models.CharField(max_length=15)
    first_count = models.IntegerField
    second_count = models.IntegerField
    third_count = models.IntegerField
    fourth_count = models.IntegerField


class Prize(models.Model):
    game_id = models.IntegerField
    inventory_count = models.IntegerField


class Player(models.Model):
    ticket_id = models.IntegerField
    prize = models.ManyToManyField(Prize)


class Session(models.Model):
    status = models.CharField(max_length=30)
    game_id = models.IntegerField
    questions = models.ManyToManyField(Question)
    players = models.ManyToManyField(Player)


class Game(models.Model):
    event_id = models.IntegerField
