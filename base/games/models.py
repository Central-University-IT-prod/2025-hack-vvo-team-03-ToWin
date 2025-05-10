import datetime
import users.models

from math import ceil, log2

from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    place = models.CharField(max_length=3000)
    image = models.ImageField(upload_to='imgs')
    description = models.CharField(max_length=2500)
    select_archive = (
        (0, 'Неактивно'),
        (1, 'Идёт набор'),
        (2, 'Набор закрыт')
    )
    archive = models.IntegerField(default=1, choices=select_archive)
    select_type = (
        (0, 'Смешанные'),
        (1, 'Баскетбол'),
        (2, 'Футбол'),
        (3, 'Хоккей'),
        (4, 'Теннис'),
        (5, 'Волейбол'),
        (6, 'Пинг-понг'),
        (7, 'Регби'),
        (8, 'Киберспорт')
    )
    command = models.BooleanField(default=1)
    type_game = models.IntegerField(default=0, choices=select_type)
    count_player_now = models.IntegerField()
    count_player_max = models.IntegerField()
    now_rank = models.IntegerField()
    creator = models.ForeignKey(users.models.User, null=True, on_delete=models.SET_NULL, related_name='creator')
  
    #завершение матча
    # def complateStage(self):
    #     # self.checkAutoWin()
    #     if self.nowRank == 0: return
    #     for i in range(len(self.stages[self.nowRank])):
    #         if self.stages[self.nowRank][i] != None:
    #             self.stages[self.nowRank][i]._SetWinner()

    #     self.nowRank -= 1
    #     self.save()
            
    #переброс победителя на след этап
    #def _OnSetWinner(self, game):
        #rank = game.rank
        #ind = self.stages[rank].index(game)

        #if self.stages[rank-1][ind//2] == None:
            #self.stages[rank-1][ind//2] = Game(rank-1, self)

        # if ind % 2 == 0:
        #     self.stages[rank-1][ind//2]._team1 = game.winner
        # else:
        #     self.stages[rank-1][ind//2]._team2 = game.winner


    #def _initStages(self):
        #maxRankInd = ceil(log2(self.maxCount))-1
        #self.nowRank = maxRankInd
        #self.stages = [[Game(rank, self) for countGames in range(2**rank)] for rank in range(maxRankInd+1)]


    #def _isCanJoin(self):
        #if self.nowCount == self.maxCount: return False
        #if None in self.stages[-1]: return True
        #for i in range(len(self.stages[-1])):
            #if self.stages[-1][i]._team1 == None or self.stages[-1][i]._team2 == None: return True
        #return False


class Game(models.Model):
    player1 = models.ForeignKey(users.models.User, null=True, on_delete=models.SET_NULL, related_name='player1')
    player2 = models.ForeignKey(users.models.User, null=True, on_delete=models.SET_NULL, related_name='player2')
    count1 = models.IntegerField(default=0)
    count2 = models.IntegerField(default=0)
    winner = models.ForeignKey(users.models.User, null=True, on_delete=models.SET_NULL, related_name='winner')
    rank = models.IntegerField()
    competition = models.ForeignKey(Competition, null=True, on_delete=models.SET_NULL)
    place = models.CharField(max_length=3000)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    active = models.BooleanField(default=1)


    def _SetWinner(self):
        if self.player1 == None:
            self.winner = self.player2
        elif self.player2 == None:
            self.winner = self.player1 
        else:
            self.winner = self.player1 if self.count1 > self.count2 else self.player2
        self.active = False
        #self.competition._OnSetWinner(self)
        self.save()