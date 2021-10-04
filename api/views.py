from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
import random
from .models import Game, Player, GameStateChoice, ProfessionChoice
import json

def hall_list(request):
    game = Game.objects.get_or_create(GameStateChoice=GameStateChoice.Before)
    res_json = serialize('json', game.player_set.all())
    return HttpResponse(res_json)


def join_game(request):
    if request.method == 'POST':
        name = request.POST.get('name', 0)
        hope_profession = request.POST.get('hp', 0)
        game = Game.objects.last()
        if game.state != GameStateChoice.Before:
            hope_profession = "OB"
        player = Player(name_text=name, profession=hope_profession)
        player.game = game
        player.save()
    return hall_list(request)


def default_game_mode(total):
    # if total ==
    pass

def assign_profession_by(profession, players, count):
    if count == 0:
        return
    pro_players = []
    for pl in players:
        if pl.profession == profession:
            pro_players.append(pl)
    if len(pro_players) == count:
        return
    elif len(pro_players) > count:
        for i in range(len(pro_players) - count):
            random.choice(pro_players).profession = ProfessionChoice.No
    else:
        other_hope = list(set(players) - set(pro_players))
        no_list = []
        for i in other_hope:
            if i.profession == ProfessionChoice.No:
                no_list.append(i)
        for j in range(count - len(pro_players)):
            random.choice(no_list).profession = profession
    for p in players:
        p.save()

def game_start(request):
    game = Game.objects.last()
    players = game.player_set.all()
    if request.method == 'POST':
        is_default = request.POST.get("isDefault", 0)
        pro_dict = {}
        if is_default == "NO":
            pro_dict = default_game_mode(game.player_set.count())
        else:
            pro_dict = json.loads((request.POST.get("mode", 0)))
        for k in pro_dict:
            count = pro_dict[k]
            assign_profession_by(k, players, count)






