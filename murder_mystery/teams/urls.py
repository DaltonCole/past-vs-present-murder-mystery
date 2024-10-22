from django.urls import path

from . import views

app_name = 'team'
urlpatterns = [
    path('clue_hint/', views.clue_hint, name='clue-hint')
]
