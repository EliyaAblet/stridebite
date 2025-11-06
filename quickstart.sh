#!/usr/bin/env bash
set -e

project="stridebite"
app="core"

if [ ! -f "manage.py" ]; then
  django-admin startproject $project .
  python manage.py startapp $app
  echo "from django.contrib import admin
from django.urls import path
urlpatterns = [path('admin/', admin.site.urls)]" > $project/urls.py
fi

echo "Bootstrap complete."
#!/bin/bash
echo 'Quickstart running'
