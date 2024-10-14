from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Character(models.Model):
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    real_name = models.CharField(max_length=32)
    character_name = models.CharField(max_length=32)

    PAST_OR_FUTURE_CHOICES = [('p', 'Past'), ('f', 'Future')]
    past_or_future = models.CharField(
        choices=PAST_OR_FUTURE_CHOICES,
        default='f',
        max_length=16,
    )

    occupation = models.CharField(max_length=32)
    descriptor1 = models.CharField(max_length=32)
    descriptor2 = models.CharField(max_length=32)
    descriptor3 = models.CharField(max_length=32)
    solo = models.BooleanField()
    preferred_partner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='I_choose_you_to_be_my_partner',
    )
