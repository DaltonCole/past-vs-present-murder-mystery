from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.home, name='home'),
    path('found_clues', views.found_clues, name='found-clues'),
    path('solution', views.solution, name='solution'),
    path('score', views.score, name='score'),
    path('bonus_points', views.bonus_points, name='bonus-points'),
    path('score_htmx', views.score_htmx, name='score-htmx'),
    path('found_clues_htmx', views.found_clues_htmx, name='found-clues-htmx'),
]
