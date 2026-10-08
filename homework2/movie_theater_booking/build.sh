#!/usr/bin/env bash
# Render build command. Runs on every deploy, on a fresh copy of the code.
set -o errexit  # stop at the first failing step, so a broken deploy fails loudly

pip install -r requirements.txt
python manage.py collectstatic --no-input   # admin CSS/JS into staticfiles/ for whitenoise
python manage.py migrate
python manage.py seed_demo                  # movies + seats; demo user if DEMO_PASSWORD is set
