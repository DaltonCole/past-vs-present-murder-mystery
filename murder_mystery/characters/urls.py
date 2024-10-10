from django.urls import path

from . import views

app_name = 'characters'
urlpatterns = [
    path('creation/', views.creation, name='creation')
]
