# StrideBite – Security Hardening Notes (Milestone 2)

This document summarizes the hardening steps taken for the **StrideBite** fitness tracker,
covering:

- Application-level controls (Django app & REST API)
- Authentication / authorization
- Input validation & sanitization
- Container-level and EC2 deployment hardening
- Known limitations & future work

---

## 1. Architecture & Threat Model (High Level)

**Tech stack**

- Django 5.x (server-rendered UI + REST API using Django REST Framework)
- Django REST Framework (DRF) for JSON endpoints
- Relational database accessed only via Django ORM (no raw SQL)
- Deployed in a single Docker container on an AWS EC2 instance

**Main assets**

- User accounts and password hashes
- Meal and workout logs (time, duration, calories, notes)
- Authentication tokens for API access (DRF token auth)

**Primary threats considered**

- Unauthorized access to meal/workout data
- Account takeover via weak auth / session mis-handling
- Injection (XSS / script injection) in logged text fields
- CSRF against state-changing views
- Abuse of API endpoints (unauthenticated access, data leakage)
- Basic container or OS-level compromise

---

## 2. Authentication & Authorization

### 2.1 Django authentication

- StrideBite uses **Django’s built-in authentication system**:
  - Passwords are hashed using Django’s default password hasher.
  - Login and logout are handled via Django’s `LoginView` and `LogoutView`.
- Only the following views are accessible to unauthenticated users:
  - Public landing page (`/`)
  - Login (`/login/`)
  - Signup (`/signup/`)
  - Password reset & forgot-username flow

All other views are protected with `@login_required` or DRF permissions.

### 2.2 Per-user data scoping

- All meal and workout queries are filtered by `user=request.user`.
- CRUD views use `get_object_or_404(..., user=request.user)` so that users **cannot access or edit another user’s data**, even by guessing IDs.

### 2.3 REST API (DRF) auth & permissions

In `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
