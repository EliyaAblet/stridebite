# StrideBite — Daily Fitness & Meal Tracker

**StrideBite** is a simple, privacy-first web app that helps you log **workouts, meals, body metrics, sleep, and progress photos**—then turns them into **clean, motivating charts**. No ads, no clutter. Just your data, your rhythm.

## Why it matters
Most trackers are noisy or locked behind subscriptions. StrideBite keeps it **lightweight, local-first, and transparent**, making it easy to stay consistent and see what actually moves the needle—**protein, training volume, sleep, and recovery**—in one place.

---

## Features (Milestone 1 scope)
- Log **workouts** (run/strength/treadmill), **meals** (protein & calories), **weigh-ins**, **sleep**, and **progress photos**
- **Today Summary** with last-7-day trend mini-charts
- **Export** your data (CSV/JSON)
- Email/password auth (basic)

> Roadmap: goal alerts, macro breakdowns, wearables import, shareable progress links.

---

## Installation

### Option A — Docker (recommended)
```bash
git clone https://github.com/eliyaablet/stridebite.git
cd stridebite
docker compose up --build -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
# StrideBite — Project Scaffold
