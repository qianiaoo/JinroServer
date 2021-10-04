from django.db import models
from enum import Enum


# Create your models here.

class ProfessionChoice(Enum):
    Oracle = 'OR'
    Wolf = "WF"
    Knight = "KN"
    Human = "HM"
    Observation = "OB"
    Hunter = "HN"
    No = "NO"


class GameStateChoice(Enum):
    Before = "BF"
    Execution = 'TR'
    Eve = 'EV'
    Begin = "BE"
    Talk = "TL"


class WinChoice(Enum):
    Human = "人類たちの勝利"
    Wolf = "人狼たちの勝利"


# class Player:
#     name = ''
#     profession = ProfessionChoice.Human
#     alive = True
#
#
# class Game:
#     mode = []
#     state = GameStateChoice.Begin
#     players = []

#


class Game(models.Model):
    state = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in GameStateChoice], default=GameStateChoice.Before.value)


class Player(models.Model):
    name_text = models.CharField(max_length=100)
    profession = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in ProfessionChoice], default=ProfessionChoice.No.value)
    alive = models.BooleanField(default=True)
    win = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in WinChoice], default=WinChoice.Human.value)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

