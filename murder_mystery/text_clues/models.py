from django.db import models
from characters.models import Character

# Create your models here.
class OccupationFlavorText(models.Model):
    flavor_text = models.TextField()


class DescriptorFlavorText(models.Model):
    flavor_text = models.TextField()


class TextClue(models.Model):
    character_id = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
    )

    occupation_flavor_text = models.ForeignKey(
        OccupationFlavorText,
        on_delete=models.CASCADE,
        related_name='occupation',
    )
    descriptor1_flavor_text = models.ForeignKey(
        DescriptorFlavorText,
        on_delete=models.CASCADE,
        related_name='descriptor1',
    )
    descriptor2_flavor_text = models.ForeignKey(
        DescriptorFlavorText,
        on_delete=models.CASCADE,
        related_name='descriptor2',
    )
    descriptor3_flavor_text = models.ForeignKey(
        DescriptorFlavorText,
        on_delete=models.CASCADE,
        related_name='descriptor3',
    )
