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

urlpatterns = router.urls
