from django.db import models
from characters.models import Character

# Create your models here.
class FlavorText(models.Model):
    flavor_text = models.TextField()


class TextClue(models.Model):
    flavor_text = models.ForeignKey(
        FlavorText,
        on_delete=models.CASCADE,
    )
    character_id = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
    )
