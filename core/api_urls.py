from django.urls import path
from . import api_views

urlpatterns = [
    # Meals
    path("meals/", api_views.MealListCreateAPIView.as_view(), name="api_meals"),
    path("meals/<int:pk>/", api_views.MealRetrieveUpdateDestroyAPIView.as_view(), name="api_meal_detail"),

    # Workouts
    path("workouts/", api_views.WorkoutListCreateAPIView.as_view(), name="api_workouts"),
    path("workouts/<int:pk>/", api_views.WorkoutRetrieveUpdateDestroyAPIView.as_view(), name="api_workout_detail"),
]
