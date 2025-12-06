# Dockerfile for StrideBite (hardened)
FROM python:3.12-slim AS base

# --- Security / runtime sanity envs ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONFAULTHANDLER=1 \
    DJANGO_ENV=production

# Set working directory
WORKDIR /app

# --- OS-level deps (only what we need) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Python dependencies ---
COPY requirements.txt .

# Upgrade pip and install deps without cache
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# --- Non-root user for app runtime ---
RUN addgroup --system app && adduser --system --ingroup app app

# Copy project files as non-root and fix ownership
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Expose app port
EXPOSE 8000

# Optional: container healthcheck using Django's checks
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python manage.py check --deploy || exit 1

# --- Start gunicorn instead of Django dev server ---
# If your project module is not "stridebite", change it below.
CMD ["gunicorn", "stridebite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
