from django.db import models
from characters.models import Character
from video_clues.models import VideoClue
from text_clues.models import TextClue

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
            default=False,
            )
    # Number of attempts this team has had at submitting the correct solution
    #   Tries will be point deductions
    tries = models.SmallIntegerField(
            default=0,
            )
    video_clue = models.ForeignKey(
           VideoClue,
           on_delete=models.CASCADE,
           blank=True,
           null=True,
            )
    text_clue = models.ForeignKey(
           TextClue,
           on_delete=models.CASCADE,
           blank=True,
           null=True,
            )
