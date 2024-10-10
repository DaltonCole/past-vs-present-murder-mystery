from django.urls import path

from . import views

app_name = 'admin-pages'
urlpatterns = [
    path('console', views.console, name='console'),
]
