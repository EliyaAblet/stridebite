from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# For convenience
USER_MODEL = settings.AUTH_USER_MODEL


class Meal(models.Model):
    """
    A single meal with protein and calories.
    Linked to a user so each person sees only their own data.
    """

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="meals",
        null=True,
        blank=True,  # keep optional for now so migrations are easier
    )
    food_name = models.CharField(max_length=100)
    protein = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Protein in grams",
    )
    calories = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Calories for this meal",
    )
    logged_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.food_name} ({self.protein}g protein, {self.calories} kcal)"


class Workout(models.Model):
    """
    A logged workout (run, strength, treadmill, etc.).
    """

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workouts",
        null=True,
        blank=True,
    )
    workout_type = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Duration in minutes",
    )
    notes = models.TextField(blank=True)
    logged_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.workout_type} ({self.duration} min)"


class WeighIn(models.Model):
    """
    Daily bodyweight entry.
    """

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weigh_ins",
        null=True,
        blank=True,
    )
    date = models.DateField(default=timezone.localdate)
    weight_lbs = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(50),
            MaxValueValidator(400),
        ],
        help_text="Bodyweight in pounds",
    )
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.date} – {self.weight_lbs} lbs"


class Sleep(models.Model):
    """
    Daily sleep entry (hours slept).
    """

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sleeps",
        null=True,
        blank=True,
    )
    date = models.DateField(default=timezone.localdate)
    hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(24),
        ],
        help_text="Total hours slept",
    )
    sleep_quality = models.PositiveSmallIntegerField(
        default=3,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        help_text="1 = very poor, 5 = excellent",
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.date} – {self.hours}h (quality {self.sleep_quality})"


class ProgressPhoto(models.Model):
    """
    Progress photo for visual tracking.
    """

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress_photos",
        null=True,
        blank=True,
    )
    date = models.DateField(default=timezone.localdate)
    image = models.ImageField(upload_to="progress_photos/")
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date", "-uploaded_at"]

    def __str__(self) -> str:
        return f"Photo on {self.date} ({self.user})"
