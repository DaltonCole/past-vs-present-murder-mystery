from django.db import models

# Create your models here.
class Character(models.Model):
    password = models.CharField(('password'), max_length=128)
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
    prefered_partner = models.CharField(max_length=32)
