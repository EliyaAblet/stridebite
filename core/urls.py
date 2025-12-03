from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Meal CRUD
    path("meals/", views.meal_list, name="meal_list"),
    path("meals/add/", views.meal_create, name="meal_create"),
    path("meals/<int:pk>/edit/", views.meal_update, name="meal_update"),
    path("meals/<int:pk>/delete/", views.meal_delete, name="meal_delete"),

    # Workout CRUD
    path("workouts/", views.workout_list, name="workout_list"),
    path("workouts/add/", views.workout_create, name="workout_create"),
    path("workouts/<int:pk>/edit/", views.workout_update, name="workout_update"),
    path("workouts/<int:pk>/delete/", views.workout_delete, name="workout_delete"),
]
