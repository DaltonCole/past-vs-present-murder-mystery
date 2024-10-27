from django.urls import path

from pages.views import (
    bonus_points,
    found_clues,
    found_clues_htmx,
    home,
    score,
    score_htmx,
    solution,
)
# Individual imports because database initialization gets confused by CharacterClueForm otherwise

app_name = 'pages'
urlpatterns = [
    path('', home, name='home'),
    path('clue', home, name='clue'),
    path('found_clues', found_clues, name='found-clues'),
    path('solution', solution, name='solution'),
    path('score', score, name='score'),
    path('bonus_points', bonus_points, name='bonus-points'),
    path('score_htmx', score_htmx, name='score-htmx'),
    path('found_clues_htmx', found_clues_htmx, name='found-clues-htmx'),
]
