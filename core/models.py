# core/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

User = get_user_model()

# Simple validator to block HTML tags (and by extension script tags)
no_html_validator = RegexValidator(
    regex=r'^[^<>]*$',
    message="HTML tags are not allowed in this field.",
)


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")

    # Text field with no-HTML validator
    food_name = models.CharField(
        max_length=200,
        validators=[no_html_validator],
    )

    # Protein in grams, ex: 0–300g
    protein = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(300),
        ],
        help_text="Protein in grams (0–300).",
    )

    # Calories in kcal, ex: 0–5000
    calories = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5000),
        ],
        help_text="Calories in kcal (0–5000).",
    )

    # When this meal was logged
    logged_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.food_name} ({self.calories} kcal)"


class Workout(models.Model):
    WORKOUT_TYPES = [
        ("run", "Run"),
        ("strength", "Strength"),
        ("treadmill", "Treadmill"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")

    workout_type = models.CharField(
        max_length=50,
        choices=WORKOUT_TYPES,
        validators=[no_html_validator],
    )

    # Duration in minutes, ex: 1–600
    duration = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(600),
        ],
        help_text="Duration in minutes (1–600).",
    )

    # Optional calories burned
    calories = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5000),
        ],
        help_text="Estimated calories burned (0–5000).",
    )

    logged_at = models.DateTimeField(default=timezone.now)

    # Optional notes – also blocked from containing HTML tags
    notes = models.TextField(
        blank=True,
        validators=[no_html_validator],
        help_text="Optional notes about this workout (no HTML).",
    )

    def __str__(self) -> str:
        return f"{self.workout_type} for {self.duration} min"


class Sleep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sleeps")

    # Hours slept, ex: 0–24
    hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(24),
        ],
        help_text="Hours slept (0–24).",
    )

    logged_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.hours}h sleep"


class WeighIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weighins")

    # Weight in kg, ex: 30–400
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(30),
            MaxValueValidator(400),
        ],
        help_text="Body weight in kg (30–400).",
    )

    logged_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.weight_kg} kg"

