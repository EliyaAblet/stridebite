from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    # -------------------------
    # Public Landing Page
    # -------------------------
    path("", views.home, name="home"),

    # -------------------------
    # Authentication
    # -------------------------
    path(
        "login/",
        LoginView.as_view(template_name="login.html"),
        name="login",
    ),

    path("signup/", views.signup, name="signup"),

    # Custom logout that works with GET
    path("logout/", views.logout_view, name="logout"),

    # Forgot username
    path("forgot-username/", views.forgot_username, name="forgot_username"),

    # -------------------------
    # Dashboard
    # -------------------------
    path("dashboard/", views.dashboard, name="dashboard"),

    # -------------------------
    # Meals CRUD
    # -------------------------
    path("meals/", views.meal_list, name="meal_list"),
    path("meals/add/", views.meal_create, name="meal_create"),
    path("meals/<int:pk>/edit/", views.meal_update, name="meal_update"),
    path("meals/<int:pk>/delete/", views.meal_delete, name="meal_delete"),

    # -------------------------
    # Workouts CRUD
    # -------------------------
    path("workouts/", views.workout_list, name="workout_list"),
    path("workouts/add/", views.workout_create, name="workout_create"),
    path("workouts/<int:pk>/edit/", views.workout_update, name="workout_update"),
    path("workouts/<int:pk>/delete/", views.workout_delete, name="workout_delete"),

    # -------------------------
    # Password Reset Flow
    # -------------------------
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]


