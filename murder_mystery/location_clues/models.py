from django.db import models

from story_clues.models import StoryClue

# Create your models here.
class Location(models.Model):
    location = models.CharField(max_length=32)
    where = models.TextField()
    location_hint1 = models.TextField()
    location_hint2 = models.TextField()
    location_hint3 = models.TextField()

class LocationClue(models.Model):
    story_clue = models.ForeignKey(
            StoryClue,
            on_delete=models.CASCADE,
            )
    location = models.ForeignKey(
            Location,
            on_delete=models.CASCADE,
            )
