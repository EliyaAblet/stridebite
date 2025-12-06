# core/admin.py

from django.contrib import admin
from .models import Meal, Workout, Sleep, WeighIn


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "logged_at", "food_name", "protein", "calories")
    list_filter = ("user", "logged_at")
    search_fields = ("food_name", "user__username")


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "logged_at", "workout_type", "duration", "calories")
    list_filter = ("user", "workout_type", "logged_at")
    search_fields = ("workout_type", "notes", "user__username")


@admin.register(Sleep)
class SleepAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "logged_at", "hours")
    list_filter = ("user", "logged_at")
    search_fields = ("user__username",)


@admin.register(WeighIn)
class WeighInAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "logged_at", "weight_kg")
    list_filter = ("user", "logged_at")
    search_fields = ("user__username",)
