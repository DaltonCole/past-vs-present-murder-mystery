from django.db import models
from teams.models import Team

# Create your models here.
class Solution(models.Model):
    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
    )

    # When the solution was first submitted
    first_finished = models.DateTimeField(auto_now_add=True)
    # Last time the solution was submitted
    finished = models.DateTimeField(auto_now=True)

    solution = models.TextField()
