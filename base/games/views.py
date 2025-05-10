import datetime, users.models
from math import log2

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . import forms, models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from .models import Competition
from main.views import check_user_in_game


def create_games_for_competition(comp: models.Competition):
    for i in range(comp.now_rank, -1, -1):
        for j in range(comp.count_player_max//2**(comp.now_rank-i+1)):
            g = models.Game(competition=comp, rank=i)
            g.save()


@login_required
def create(request):
    template_name = 'create.html'
    context = {}
    if request.user.role == 1:
        if request.method == 'POST':
            form = forms.CreateCompetitionForm(request.POST)
            if form.is_valid():
                comp = form.save(commit=False)
                comp.now_rank = int(-1 * log2(comp.count_player_max) // 1 * -1)
                comp.datetime = datetime.datetime.combine(datetime.datetime.date(form.cleaned_data['datetime']), form.cleaned_data['time'])
                comp.count_player_now = 0
                comp.save()
                create_games_for_competition(comp)
                
        elif request.method == 'GET':
            form = forms.CreateCompetitionForm()
            context['form'] = form

            return render(request, template_name=template_name, context=context)
        
    return redirect('index')


@login_required
def join(request, comp_id: int):
    if request.user.role == 0:
        try:
            comp = get_object_or_404(models.Competition, id=comp_id)
            if request.user.command == comp.command:
                games_with_user = models.Game.objects.filter(competition=comp, player1=request.user)
                if not games_with_user:
                    games_with_user = models.Game.objects.filter(competition=comp, player2=request.user)
                    if not games_with_user:
                        if comp.archive == 1:
                            try:
                                free_games_with_one = get_list_or_404(models.Game, competition=comp, rank=comp.now_rank, player2=None)
                                print(free_games_with_one)
                                for g in free_games_with_one:
                                    
                                    if g.player1 != None:
                                        g.player2 = request.user
                                        g.save()
                                        comp.count_player_now += 1
                                        comp.save()
                                        break
                                else:
                                    free_games_empty = get_list_or_404(models.Game, competition=comp, rank=comp.now_rank, player1=None, player2=None)
                                    free_games_empty[0].player1 = request.user
                                    free_games_empty[0].save()
                                    comp.count_player_now += 1
                                    comp.save()
                            except:
                                pass
                            #free_games_empty = get_list_or_404(models.Game, competition=comp, rank=comp.now_rank, player1=None, player2=None)
                            #free_games_empty[0].player1 = request.user
                            #free_games_empty[0].save()
        except:
            pass
    return redirect('index')
            

@login_required
def leave(request, comp_id: int):
    if request.user.role == 0:
        try:
            comp = get_object_or_404(models.Competition, id=comp_id)
            try:
                game_now = get_object_or_404(models.Game, competition=comp, player2=request.user)
                game_now.player2 = None
                game_now.save()
                comp.count_player_now -= 1
                comp.save()
            except:
                game_now = get_object_or_404(models.Game, competition=comp, player1=request.user)
                game_now.player1 = game_now.player2
                game_now.player2 = None
                game_now.save()
                comp.count_player_now -= 1
                comp.save()
        except:  
            pass
    return redirect('index')
        

def comp(request, comp_id: int):
    template_name = 'competition.html'
    context = {}
    try:
        comp = get_object_or_404(models.Competition, id=comp_id)
        
        context['comp'] = comp
        context['games'] = []
        for i in range(int(-1 * log2(comp.count_player_max) // 1 * -1), 0, -1):
            games  = get_list_or_404(models.Game, rank=i, competition=comp)
            context['games'].append(games)

        return render(request, template_name, context=context)
    except:
        return redirect('index')
    #return render(request, template_name, context=context)


def mygames(request):
    context = {}
    template_name = 'mygames.html'
    context['competitions'] = []
    competitions = models.Competition.objects.all().order_by('-count_player_now')
    for c in competitions:
        if check_user_in_game(request.user, c):
            context['competitions'].append(c)
    
    
    return render(request=request, template_name=template_name, context=context)


def select_winners(request, comp_id: id):
    try: 
        comp = get_object_or_404(models.Competition, id=comp_id)
        games = get_list_or_404(models.Game, competition=comp, rank=comp.now_rank)
        for g in games:
            g._SetWinner()
        games_high = models.Game.objects.filter(competition=comp_id, rank=comp.now_rank-1)
        g = games_high[0]
        g.player1 = games[0].winner
        g.save()
        
        g.player2 = games[1].winner
        g.save()
        last_index = 1
        for g in range(1, len(games_high)):
            gh = games_high[g]
            gh.player1 = games[last_index+1].winner
            gh.player2 = games[last_index+2].winner
            gh.save()
            last_index += 2
        comp.now_rank -= 1
        comp.save()
        return redirect('mygames')
    except Exception as e:
        print(e)
    return redirect('index')

@api_view(['GET'])
@permission_classes([AllowAny])
def apimethod(request):
    return Response({
        "swagger": "2.0", 
        "title": "Music API Documentation",
        "2": 200
    })

class CompetitionListCreateAPIView(APIView):
    def get(self, request):
        competitions = Competition.objects.all()
        data = []
        for comp in competitions:
            data.append({
                "id": comp.id,
                "name": comp.name,
                "type_game": comp.type_game,
                "count_player_max": comp.count_player_max,
                "count_player_now": comp.count_player_now,
                "now_rank": comp.now_rank,
                "datetime": comp.datetime,
            })
        return Response(data)

def edit_game(request, game_id: int, count1:int, count2:int):
    game = get_object_or_404(models.Game, id=game_id)
    print(game.id, game.player1, game.player2)

    if game.player1 != None and game.player2 != None:
        print('oo')
        game.count1 = count1
        game.count2 = count2
        game.save()
    return redirect('mygames')
