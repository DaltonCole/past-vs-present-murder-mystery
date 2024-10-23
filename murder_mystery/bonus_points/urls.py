from django.urls import path

from . import views

app_name = 'bonus-points'
urlpatterns = [
    path('submission', views.bonus_point_submission, name='submission'),
    path('remaining', views.bonus_points_remaining, name='remaining'),
]
