from django.db import models

# Create your models here.
class VideoClue(models.Model):
    video_url = models.URLField()
    location_hint1 = models.TextField()
    location_hint2 = models.TextField()
    location_hint3 = models.TextField()
