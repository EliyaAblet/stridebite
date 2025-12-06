from rest_framework import serializers
from .models import Meal, Workout, Sleep, WeighIn


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["id", "user", "food_name", "protein", "calories", "logged_at"]
        read_only_fields = ["id", "user"]


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["id", "user", "workout_type", "duration", "calories", "logged_at"]
        read_only_fields = ["id", "user"]


class SleepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sleep
        fields = ["id", "user", "date", "hours", "sleep_quality", "logged_at"]
        read_only_fields = ["id", "user"]


class WeighInSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeighIn
        fields = ["id", "user", "weight_kg", "logged_at"]
        read_only_fields = ["id", "user"]
