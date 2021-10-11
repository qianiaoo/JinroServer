from django.db import models
from enum import Enum



class ProfessionChoice(Enum):
    Oracle = 'OR'
    Wolf = "WF"
    Knight = "KN"
    Human = "HM"
    Observation = "OB"
    Hunter = "HN"
    No = "NO"
    Spiritualist = 'SP'
    Witch = "WH"
    WitchAfS = "WHAFS"
    WitchAfK = "WHAFK"
    WitchAFA = 'WHAFA'
    CrazyBoy = 'CB'



class GameStatusChoice(Enum):
    Before = "BF"
    Execution = 'TR'
    Eve = 'EV'
    Begin = "BE"
    Talk = "TL"
    OnGame = 'OG'


class WinChoice(Enum):
    Human = "人類たちの勝利"
    Wolf = "人狼たちの勝利"



class Game(models.Model):
    state = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in GameStatusChoice],
                             default=GameStatusChoice.Before.value)
    gameStatus = models.IntegerField(default=0)
    setting = models.CharField(max_length=500,default='')

class Player(models.Model):
    name_text = models.CharField(max_length=100,unique=True)
    profession = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in ProfessionChoice],
                                  default=ProfessionChoice.No.value)
    alive = models.BooleanField(default=True)
    game_id = models.CharField(max_length=100,default='')
    first_job = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in ProfessionChoice],
                                 default=ProfessionChoice.No.value)
    icon = models.ImageField(upload_to="icon", default='icon/default/default.png')
    is_ready = models.BooleanField(default=False)
    to_player_id = models.CharField(max_length=100, default='')
    last_connect_time = models.DateTimeField(auto_now=True)



