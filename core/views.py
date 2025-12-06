from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Meal, Workout
from .forms import MealForm, WorkoutForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        """
        Clears any leftover messages (like logout message)
        before showing the login success message.
        """
        # Clear all old messages stored in the session
        list(messages.get_messages(self.request))

        messages.success(self.request, "Welcome back! You are now logged in.")
        return super().form_valid(form)



# --------------------------
#        PUBLIC HOME
# --------------------------
def home(request):
    """
    Always show the public landing page.
    """
    return render(request, "landing.html")


# --------------------------
#        DASHBOARD
# --------------------------
@login_required
def dashboard(request):
    meals_qs = Meal.objects.filter(user=request.user).order_by("-logged_at")
    workouts_qs = Workout.objects.filter(user=request.user).order_by("-logged_at")

    context = {
        "meal_count": meals_qs.count(),
        "workout_count": workouts_qs.count(),
        "recent_meals": meals_qs[:5],
        "recent_workouts": workouts_qs[:5],
    }
    return render(request, "home.html", context)


# --------------------------
#        MEALS CRUD
# --------------------------
@login_required
def meal_list(request):
    meals = Meal.objects.filter(user=request.user).order_by("-logged_at")
    return render(request, "meal_list.html", {"meals": meals})


@login_required
def meal_create(request):
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect("meal_list")
    else:
        form = MealForm()
    return render(request, "meal_form.html", {"form": form})


@login_required
def meal_update(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)

    if request.method == "POST":
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect("meal_list")
    else:
        form = MealForm(instance=meal)

    return render(request, "meal_form.html", {"form": form, "meal": meal})


@login_required
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)

    if request.method == "POST":
        meal.delete()
        return redirect("meal_list")

    return render(request, "meal_confirm_delete.html", {"meal": meal})


# --------------------------
#       WORKOUT CRUD
# --------------------------
@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user).order_by("-logged_at")
    return render(request, "workout_list.html", {"workouts": workouts})


@login_required
def workout_create(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect("workout_list")
    else:
        form = WorkoutForm()

    return render(request, "workout_form.html", {"form": form})


@login_required
def workout_update(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workout_list")
    else:
        form = WorkoutForm(instance=workout)

    return render(request, "workout_form.html", {"form": form, "workout": workout})


@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)

    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")

    return render(request, "workout_confirm_delete.html", {"workout": workout})


# --------------------------
#           LOGOUT
# --------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")

def forgot_username(request):
    """
    Simple demo view:
    - User enters email
    - We look up the account and show the username using messages.
    (For production you'd send this via email instead.)
    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        user = User.objects.filter(email__iexact=email).first()

        if user:
            messages.success(
                request,
                f"Your username for StrideBite is: {user.username}",
            )
        else:
            messages.error(
                request,
                "We couldn't find an account with that email address."
            )

    return render(request, "forgot_username.html")

def signup(request):
    """
    Simple sign-up:
    - Shows Django's UserCreationForm
    - On success, creates the user and redirects to login with a success message.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your account has been created. You can now log in to StrideBite."
            )
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})
