from django.db import models

from teams.models import Team

# Create your models here.
class BonusPoint(models.Model):
    amount = models.SmallIntegerField()
    reason = models.TextField()
    answer = models.CharField(max_length=100)

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
