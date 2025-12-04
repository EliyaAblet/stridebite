from rest_framework import generics
from .models import Meal, Workout
from .serializers import MealSerializer, WorkoutSerializer


# -------- Meals API --------

class MealListCreateAPIView(generics.ListCreateAPIView):
    queryset = Meal.objects.all().order_by("-logged_at")
    serializer_class = MealSerializer


class MealRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


# -------- Workouts API --------

class WorkoutListCreateAPIView(generics.ListCreateAPIView):
    queryset = Workout.objects.all().order_by("-logged_at")
    serializer_class = WorkoutSerializer


class WorkoutRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
