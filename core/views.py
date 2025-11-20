from django.shortcuts import render, redirect
from .models import Meal, Workout


def home(request):
    """Simple dashboard placeholder."""
    recent_meals = Meal.objects.order_by("-id")[:5]
    recent_workouts = Workout.objects.order_by("-id")[:5]
    context = {
        "recent_meals": recent_meals,
        "recent_workouts": recent_workouts,
    }
    return render(request, "core/home.html", context)


def add_meal(request):
    if request.method == "POST":
        Meal.objects.create(
            food_name=request.POST.get("food_name", ""),
            protein=request.POST.get("protein") or 0,
            calories=request.POST.get("calories") or 0,
        )
        return redirect("home")

    return render(request, "core/add_meal.html")


def add_workout(request):
    if request.method == "POST":
        Workout.objects.create(
            workout_type=request.POST.get("workout_type", ""),
            duration=request.POST.get("duration") or 0,
            notes=request.POST.get("notes", ""),
        )
        return redirect("home")

    return render(request, "core/add_workout.html")
