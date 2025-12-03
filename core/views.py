from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Meal, Workout
from .forms import MealForm, WorkoutForm


def home(request):
    """Dashboard: quick stats + recent items."""
    meals = Meal.objects.order_by("-logged_at")
    workouts = Workout.objects.order_by("-logged_at")

    context = {
        "meal_count": meals.count(),
        "workout_count": workouts.count(),
        "recent_meals": meals[:5],
        "recent_workouts": workouts[:5],
    }
    return render(request, "home.html", context)


# ========= MEAL CRUD =========

def meal_list(request):
    meals = Meal.objects.order_by("-logged_at")
    return render(request, "meal_list.html", {"meals": meals})


def meal_create(request):
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("meal_list")
    else:
        form = MealForm(initial={"logged_at": timezone.now()})

    return render(request, "meal_form.html", {"form": form, "mode": "create"})


def meal_update(request, pk):
    meal = get_object_or_404(Meal, pk=pk)

    if request.method == "POST":
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect("meal_list")
    else:
        form = MealForm(instance=meal)

    context = {"form": form, "mode": "edit", "meal": meal}
    return render(request, "meal_form.html", context)


def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk)

    if request.method == "POST":
        meal.delete()
        return redirect("meal_list")

    return render(request, "meal_confirm_delete.html", {"meal": meal})


# ========= WORKOUT CRUD =========

def workout_list(request):
    workouts = Workout.objects.order_by("-logged_at")
    return render(request, "workout_list.html", {"workouts": workouts})


def workout_create(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("workout_list")
    else:
        form = WorkoutForm(initial={"logged_at": timezone.now()})

    return render(request, "workout_form.html", {"form": form, "mode": "create"})


def workout_update(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workout_list")
    else:
        form = WorkoutForm(instance=workout)

    context = {"form": form, "mode": "edit", "workout": workout}
    return render(request, "workout_form.html", context)


def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")

    return render(request, "workout_confirm_delete.html", {"workout": workout})
