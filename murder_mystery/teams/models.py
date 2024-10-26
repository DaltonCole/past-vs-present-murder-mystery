from django.db import models

from character_clues.models import CharacterClue
from characters.models import Character
from location_clues.models import LocationClue

# Create your models here.
class Team(models.Model):
    past_character = models.OneToOneField(
        Character,
        on_delete=models.CASCADE,
        related_name='past_character',
        null=True,
        blank=True,
    )
    future_character = models.OneToOneField(
        Character,
        on_delete=models.CASCADE,
        related_name='future_character',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Team({self.past_character.username.username if self.past_character else None}, {self.future_character.username.username if self.future_character else None})'

class TeamToClue(models.Model):
    team = models.ForeignKey(
            Team,
            on_delete=models.CASCADE,
            )
    order = models.SmallIntegerField()
    found = models.BooleanField(
            default=False,
            )
    location_hints = models.SmallIntegerField(
            default=0,
            )
    # Number of attempts this team has had at submitting the correct solution
    #   Tries will be point deductions
    tries = models.SmallIntegerField(
            default=0,
            )
    location_clue = models.ForeignKey(
           LocationClue,
           on_delete=models.CASCADE,
           blank=True,
           null=True,
            )
    character_clue = models.ForeignKey(
           CharacterClue,
           on_delete=models.CASCADE,
           blank=True,
           null=True,
            )
