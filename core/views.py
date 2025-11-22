from django.shortcuts import render, redirect
from .models import Meal, Workout


def home(request):
    meals_count = Meal.objects.count()
    workouts_count = Workout.objects.count()

    # just show a few recent entries so the page feels alive
    latest_meals = Meal.objects.order_by("-id")[:5]
    latest_workouts = Workout.objects.order_by("-id")[:5]

    context = {
        "meals_count": meals_count,
        "workouts_count": workouts_count,
        "latest_meals": latest_meals,
        "latest_workouts": latest_workouts,
    }
    return render(request, "home.html", context)


def add_meal(request):
    if request.method == "POST":
        Meal.objects.create(
            food_name=request.POST["food_name"],
            protein=request.POST["protein"],
            calories=request.POST["calories"],
        )
        return redirect("home")
    return render(request, "add_meal.html")


def add_workout(request):
    if request.method == "POST":
        Workout.objects.create(
            workout_type=request.POST["workout_type"],
            duration=request.POST["duration"],
            notes=request.POST.get("notes", ""),
        )
        return redirect("home")
    return render(request, "add_workout.html")

