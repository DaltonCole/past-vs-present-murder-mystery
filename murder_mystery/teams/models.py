from django.db import models
from characters.models import Character

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
