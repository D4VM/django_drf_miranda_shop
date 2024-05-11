#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Start Django server
cd src/
screen -dmS django-server python manage.py runserver 0.0.0.0:8000
