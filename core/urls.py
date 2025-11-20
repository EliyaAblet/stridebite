from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-meal/", views.add_meal, name="add_meal"),
    path("add-workout/", views.add_workout, name="add_workout"),
]
