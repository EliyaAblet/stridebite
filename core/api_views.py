from rest_framework import viewsets, permissions
from .models import Meal, Workout, Sleep, WeighIn
from .serializers import (
    MealSerializer,
    WorkoutSerializer,
    SleepSerializer,
    WeighInSerializer,
)


class UserOwnedModelViewSet(viewsets.ModelViewSet):
    """
    Base class that:
    - requires authentication
    - only returns the current user's rows
    - automatically sets user on create
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealViewSet(UserOwnedModelViewSet):
    queryset = Meal.objects.all().order_by("-logged_at")
    serializer_class = MealSerializer


class WorkoutViewSet(UserOwnedModelViewSet):
    queryset = Workout.objects.all().order_by("-logged_at")
    serializer_class = WorkoutSerializer


class SleepViewSet(UserOwnedModelViewSet):
    queryset = Sleep.objects.all().order_by("-logged_at")
    serializer_class = SleepSerializer


class WeighInViewSet(UserOwnedModelViewSet):
    queryset = WeighIn.objects.all().order_by("-logged_at")
    serializer_class = WeighInSerializer
