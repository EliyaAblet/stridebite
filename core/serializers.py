from rest_framework import serializers
from .models import Meal, Workout, Sleep, WeighIn


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        # Let DRF include all fields; user will be read-only and set from request.user
        fields = "__all__"
        read_only_fields = ["id", "user"]


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = "__all__"
        read_only_fields = ["id", "user"]


class SleepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sleep
        fields = "__all__"
        read_only_fields = ["id", "user"]


class WeighInSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeighIn
        fields = "__all__"
        read_only_fields = ["id", "user"]
