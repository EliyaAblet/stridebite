from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from .api_views import (
    MealViewSet,
    WorkoutViewSet,
    SleepViewSet,
    WeighInViewSet,
)

router = DefaultRouter()
router.register("meals", MealViewSet, basename="api-meal")
router.register("workouts", WorkoutViewSet, basename="api-workout")
router.register("sleep", SleepViewSet, basename="api-sleep")
router.register("weighins", WeighInViewSet, basename="api-weighin")

urlpatterns = [
    # POST here with username/password to get a token
    path("auth/token/", obtain_auth_token, name="api-token-auth"),

    # all the viewsets (meals, workouts, sleep, weighins)
    path("", include(router.urls)),
]
