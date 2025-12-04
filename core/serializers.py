from rest_framework import serializers
from .models import Meal, Workout


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["id", "food_name", "protein", "calories", "logged_at"]


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["id", "workout_type", "duration", "logged_at"]
