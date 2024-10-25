from django.db import models

from teams.models import Team

# Create your models here.
class BonusPoint(models.Model):
    amount = models.SmallIntegerField()
    reason = models.TextField()
    answer = models.CharField(max_length=100)
    # TODO: Add some bonus points that can be collected multiple times
    # TODO: Label unique bonus points in bonus point view
    # TODO: Add second get for non unique bonus points?

    def __str__(self):
        return f'({self.amount}) {self.reason}'


class TeamToBonusPoint(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    bonus_point = models.ForeignKey(
        BonusPoint,
        on_delete=models.CASCADE,
    )
