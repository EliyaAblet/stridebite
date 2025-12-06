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

Tech stack

- Django 5.x (server-rendered UI + REST API using Django REST Framework)
- Django REST Framework (DRF) for JSON endpoints
- Relational database accessed only via Django ORM (no raw SQL)
- Deployed in a single Docker container on an AWS EC2 instance

Main assets

- User accounts and password hashes
- Meal and workout logs (time, duration, calories, notes)
- Authentication tokens for API access (DRF token auth)

Primary threats considered

- Unauthorized access to meal/workout data
- Account takeover via weak auth / session mis-handling
- Injection (XSS / script injection) in logged text fields
- CSRF against state-changing views
- Abuse of API endpoints (unauthenticated access, data leakage)
- Basic container or OS-level compromise

---

## 2. Application & Container Hardening

### 2.1. Environment-based configuration (Application-level hardening)

To avoid hard-coding secrets and environment-specific values in the codebase, the Django settings were updated to read critical configuration from environment variables:

- **`DJANGO_SECRET_KEY`**  
  - The Django `SECRET_KEY` is no longer stored in `settings.py`.  
  - It is read from the `DJANGO_SECRET_KEY` environment variable at runtime.  
  - This prevents accidental exposure of secrets in version control and makes key rotation easier.

- **`DJANGO_DEBUG`**  
  - The `DEBUG` flag is controlled by the `DJANGO_DEBUG` environment variable.  
  - In development, `DJANGO_DEBUG=True` can be set locally.  
  - In production (e.g., Docker/EC2), `DJANGO_DEBUG=False` is enforced so that detailed error pages are never exposed to end users.

- **`DJANGO_ALLOWED_HOSTS`**  
  - The `ALLOWED_HOSTS` setting is populated from the `DJANGO_ALLOWED_HOSTS` environment variable (comma-separated list).  
  - This allows different hostnames/IPs for development and production without changing code, and helps protect against Host header attacks.

- **Database configuration (`POSTGRES_*` variables)**  
  - Database connection details (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`) are read from environment variables instead of being hard-coded.  
  - This keeps credentials out of source control and allows different databases for local development vs. production.

Overall, using environment variables for sensitive and environment-specific settings reduces the risk of credential leakage, keeps the repository clean, and aligns with 12-factor app best practices.

---

### 2.2. Container Hardening (Dockerfile)

The Docker image for StrideBite was hardened to reduce the attack surface and follow container security best practices.

**Base image & dependencies**

- Uses a slim base image: `python:3.12-slim` to minimize the OS footprint and reduce the number of installed packages.
- Installs only the necessary system dependencies (`build-essential`, `libpq-dev`) with `--no-install-recommends` and then cleans up `apt` lists:
  - `rm -rf /var/lib/apt/lists/*` to reduce image size and remove cached package metadata.

**Python & pip hardening**

- `PYTHONDONTWRITEBYTECODE=1` prevents `.pyc` files from being written, keeping the container filesystem cleaner and less cluttered.
- `PYTHONUNBUFFERED=1` ensures logs are flushed directly to stdout/stderr for better observability.
- `PIP_NO_CACHE_DIR=1` and `pip install --no-cache-dir` are used to avoid storing pip caches inside the image.
- `PYTHONFAULTHANDLER=1` improves error diagnostics by enabling Python’s fault handler.

**Non-root user**

- A dedicated, non-privileged `app` user and group are created:
  - `addgroup --system app && adduser --system --ingroup app app`
- Application code is copied with `--chown=app:app` and the container switches to the non-root user:
  - `USER app`
- Running the Django application as a non-root user significantly reduces the impact of a potential compromise inside the container.

**Production WSGI server**

- The container does **not** use Django’s development server.  
- It runs `gunicorn` instead:

```bash
CMD ["gunicorn", "stridebite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
