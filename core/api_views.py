# core/api_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Meal, Workout, Sleep, WeighIn
from .serializers import (
    MealSerializer,
    WorkoutSerializer,
    SleepSerializer,
    WeighInSerializer,
)
from .permissions import IsAppUser


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated, IsAppUser]

    def get_queryset(self):
        # Each user sees only their own meals
        return Meal.objects.filter(user=self.request.user).order_by("-logged_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated, IsAppUser]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by("-logged_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SleepViewSet(viewsets.ModelViewSet):
    serializer_class = SleepSerializer
    permission_classes = [IsAuthenticated, IsAppUser]

    def get_queryset(self):
        return Sleep.objects.filter(user=self.request.user).order_by("-logged_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WeighInViewSet(viewsets.ModelViewSet):
    serializer_class = WeighInSerializer
    permission_classes = [IsAuthenticated, IsAppUser]

    def get_queryset(self):
        return WeighIn.objects.filter(user=self.request.user).order_by("-logged_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

