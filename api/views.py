from collections import Counter
import time
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
import random
from .models import Game, Player, GameStatusChoice, ProfessionChoice
import json


def hall_list(request):
    # game = Game.objects.get_or_create(gameStatusChoice=GameStatusChoice.Before)
    # res_json = serialize('json',  Player.objects.all().filter(game_id=game.pk))
    # return HttpResponse(res_json)
    if request.method == "GET":
        game_id = request.GET.get('gameId')
        player_id = request.GET.get("id")
        game = Game.objects.get(pk=game_id)
        player = Player.objects.get(pk=player_id)
        player.game_id = game_id
        player.save()
        players = Player.objects.all().filter(game_id=game_id).only("is_ready",'icon', 'name_text')
        player_data = []
        for i in players:
            last_conn_time = i.last_connect_time.timestamp()

            delay_time = time.time() - last_conn_time
            if delay_time > 3600:
                i.game_id = ''
                i.save()

            player_data.append({'name': str(i.name_text), 'isReady': str(i.is_ready), 'img_url': str(i.icon.url)})
        af_s_player_data = serializers.serialize('json', players, fields=("is_ready",'icon', 'name_text'))
        data = {
            'list': player_data,
            "setting": game.setting,
            'gameStatus': game.gameStatus
        }

        json_data = json.dumps(data)
        return JsonResponse(data, safe=False)

def kick_player(request):
    if request.method == "GET":
        kick_name = request.GET.get("kick_name")
        player = Player.objects.get(name_text=kick_name)
        player.game_id = ''
        player.save()
        return JsonResponse({})




def join_game(request):
    if request.method == 'POST':
        name = request.POST.get('name', 0)
        hope_profession = request.POST.get('hp', 0)
        game = Game.objects.last()
        if game.state != GameStatusChoice.Before:
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
    players = Player.objects.all().filter(game_id=game.pk)
    if request.method == 'POST':
        is_default = request.POST.get("isDefault", 0)
        pro_dict = {}
        if is_default == "NO":
            pro_dict = default_game_mode(len(Player.objects.all().filter(game_id=game.pk)))
        else:
            pro_dict = json.loads((request.POST.get("mode", 0)))
        for k in pro_dict:
            count = pro_dict[k]
            assign_profession_by(k, players, count)


def upload_icon(request):
    if request.method == 'POST':
        print(request)
        return JsonResponse({"msg": "666"})


def update_profile(request):
    pass


def update_first_job(request):
    if request.method == "GET":
        first_job = request.GET.get("first_job")
        player_id = request.session.get('id')
        player = Player.objects.get(pk=player_id)
        player.first_job = first_job
        player.save()
        return JsonResponse({})

@csrf_exempt
def update_game_setting(request):
    if request.method == "POST":
        print(request.POST)
        print(request.body)
        json_body = json.loads(request.body)

        setting = json_body['setting']
        game_id = json_body['gameId']
        game = Game.objects.get(pk=game_id)
        print(setting.items())
        game.setting = json.dumps(setting)
        game.save()

        data = {
            "msg": "success"
        }
        return JsonResponse(data)


def exile_player(request):
    if request.method == 'GET':
        player_id = request.session.get('id')
        to_player_id = request.GET.get('to')
        game_id = request.session.get("game_id")
        player = Player.objects.get(player_id)
        player.to_player_id = to_player_id
        player.save()
        game = Game.objects.get(pk=game_id)
        players = Player.objects.all().filter(game_id=game.pk)
        need_exile = {}
        for p in players:
            if p.to_player_id == '':
                return JsonResponse({'gameStatus': game.gameStatus})
            need_exile[p.to_player_id] = need_exile.get(p.to_player_id,0) + 1
        need_kill_player = ''
        count = 0
        for k,v in need_exile.items():
            if v > count:
                count = v
                need_kill_player = k
        exile_p = Player.objects.get(pk=need_kill_player)
        exile_p.alive = False
        exile_p.save()
        reset_to_player(players)
        game.gameStatus += 1
        data = {
            'gameStatus': game.gameStatus,
            "dead": exile_p.name_text
        }
        return JsonResponse(data)


def reset_to_player(players):
    for p in players:
        p.to_player_id = ''
        p.save()



def do_at_night(request):
    global operation
    if request.method == 'GET':
        player_id = request.session.get('id')
        to_player_id = request.GET.get('to')
        game_id = request.session.get("game_id")
        player = Player.objects.get(player_id)
        game = Game.objects.get(pk=game_id)
        to_player = Player.objects.get(to_player_id)
        job = player.profession
        if job == ProfessionChoice.Witch or job == ProfessionChoice.WitchAfK or job == ProfessionChoice.WitchAfS:
            operation = request.GET.get('operation')
        player.to_player_id = to_player_id
        player.save()

        if job == ProfessionChoice.Oracle or job == ProfessionChoice.Spiritualist:
            data = {
                'gameStatus': game.gameStatus,
                'job': to_player.profession
            }
            return JsonResponse(data)
        players = Player.objects.all().filter(game_id=game.pk)
        need_bite = []
        need_save = []
        need_kill = []
        need_doubt = {}
        for p in players:
            if p.alive:
                if p.to_player_id == '':
                    return JsonResponse({'gameStatus': game.gameStatus})
                if p.profession == ProfessionChoice.Wolf:
                    need_bite.append(p.to_player_id)
                if p.profession == ProfessionChoice.Knight:
                    need_save.append(p.to_player_id)
                if p.profession == ProfessionChoice.Human or p.profession == ProfessionChoice.WitchAFA :
                    need_doubt[p.to_player_id] = need_doubt.get(p.to_player_id, '0') + 1

                if operation is not None:
                    if operation == "KILL":
                        need_kill.append(p.to_player_id)
                        if p.profession == ProfessionChoice.Witch:
                            p.profession = ProfessionChoice.WitchAfK
                        elif p.profession == ProfessionChoice.WitchAfS:
                            p.profession = ProfessionChoice.WitchAFA
                    if operation == "SAVE":
                        need_save.append(p.to_player_id)
                        if p.profession == ProfessionChoice.WitchAfK:
                            p.profession = ProfessionChoice.WitchAFA
                        elif p.profession == ProfessionChoice.Witch:
                            p.profession = ProfessionChoice.WitchAfS
                    p.save()
        really_need_bite = need_bite[random.randint(need_bite)]
        reset_to_player(players)
        if really_need_bite not in need_kill:
            need_kill.append(really_need_bite)
        really_need_kill = list(set(need_kill).difference(set(need_save)))
        really_need_kill_names = [Player.objects.get(pk=i).name_text for i in really_need_kill]
        for p in really_need_kill:
            p.alive = False
            p.save()
        game.gameStatus += 1
        game.save()
        data = {
            'gameStatus': game.gameStatus,
            'dead': really_need_kill_names,

        }
        return JsonResponse(data)


def ready_game(request):
    if request.method == 'GET':
        player_id = request.GET.get('id')
        first_job = request.GET.get("firstJob", ProfessionChoice.No)
        game_id = request.GET.get('gameId')
        player = Player.objects.get(pk=player_id)
        is_ready = request.GET.get("isReady")
        player.is_ready = True if is_ready == 'true' else False
        player.first_job = first_job
        player.save()

        game = Game.objects.get(pk=game_id)
        players = Player.objects.all().filter(game_id=game.pk)
        not_ready = []
        want_job_player = []
        job_counter = {}
        no_people = []
        for p in players:
            if p.first_job == ProfessionChoice.No.value:
                no_people.append(p.pk)
            want_job_player.append((p.pk, p.first_job))
            job_counter[p.first_job] = job_counter.get(p.first_job, 0) + 1
            if not p.is_ready:
                not_ready.append(p.pk)
        if not_ready or len(players) < 3:
            return JsonResponse({'gameStatus': 0, 'notReady': not_ready})

        setting = json.loads(game.setting)
        for job, count in setting.items():
            need = count
            if count < job_counter.get(job, 0):

                for index, (p, j) in enumerate(want_job_player):
                    if j == job:
                        if need == 0:
                            no_people.append(p)

                        if random.randint(0, 1) == 1:
                            need -= 1
                            player_temp = Player.objects.get(pk=0)
                            player_temp.profession = j
                            player_temp.save()

            else:
                for index, (p, j) in enumerate(want_job_player):
                    if j == job:
                        player_temp = Player.objects.get(pk=p)
                        player_temp.profession = j
                        player_temp.save()
                        need -= 1
                for i in range(need):
                    p = no_people.pop(random.randint(0, len(no_people)-1))
                    player_temp = Player.objects.get(pk=p)
                    player_temp.profession = job
                    player_temp.save()
        game.state = GameStatusChoice.Execution
        game.gameStatus = 1
        game.save()

        data = {
            'gameStatus': 1,
            'notReady': [],

        }
        return JsonResponse(data)


def rooms(request):
    if request.method == "GET":
        games = Game.objects.all()

        return JsonResponse(games, safe=False)


def login(request):
    if request.method == "GET":

        name = request.GET.get("name")
        p = Player.objects.get_or_create(name_text=name)[0]
        p.is_ready = False
        p.game_id = ''
        p.save()
        icon_url = p.icon.url

        return JsonResponse({'id': p.pk, 'icon_url': icon_url, 'icon_path': p.icon.path})

        # p = Player.objects.all().filter(name_text=name).last()
        # if p is None:
        #     newP = Player()
        #     newP.name_text = name
        #     newP.save()
        #     request.session['id'] = newP.pk
        #     pk = newP.pk
        #     return JsonResponse({'newPid': pk})
        #
        # else:
        #     request.session['id'] = p.pk
        #     pk = p.pk
        #     return JsonResponse({'pid': pk})


def join_sakura(request):
    if request.method == "GET":
        player_id = request.GET.get('id')
        game = Game.objects.get_or_create(gameStatus=0)[0]
        request.session['game_id'] = game.pk
        player = Player.objects.get(pk=player_id)
        player.game_id = game.pk
        player.is_ready = False
        player.save()
        data = {
            'gameStatus': game.gameStatus,
            "gameId": game.pk
        }
        return JsonResponse(data)
