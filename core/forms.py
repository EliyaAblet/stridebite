# core/forms.py
from django import forms
from .models import Meal, Workout


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["food_name", "protein", "calories", "logged_at"]
        widgets = {
            "logged_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }

    def clean_food_name(self):
        # Strip whitespace and rely on model's no_html_validator
        name = self.cleaned_data["food_name"].strip()
        return name

    def clean(self):
        cleaned = super().clean()
        protein = cleaned.get("protein")
        calories = cleaned.get("calories")

        # Extra server-side sanity check
        if protein is not None and calories is not None:
            # You can tweak this heuristic, just an example
            if protein > calories:
                self.add_error(
                    "protein",
                    "Protein (g) should not be greater than calories (kcal).",
                )
        return cleaned


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["workout_type", "duration", "calories", "logged_at", "notes"]
        widgets = {
            "logged_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_notes(self):
        notes = self.cleaned_data.get("notes", "") or ""
        # Trim whitespace; HTML is blocked by model validator
        return notes.strip()

    def clean(self):
        cleaned = super().clean()
        duration = cleaned.get("duration")
        calories = cleaned.get("calories")

        if duration is not None and duration > 600:
            self.add_error("duration", "Workouts longer than 600 minutes are not allowed.")

        # Little sanity check: if calories is wildly high, flag it
        if calories is not None and calories > 5000:
            self.add_error("calories", "Calories burned seems unrealistically high (>5000).")

        return cleaned
