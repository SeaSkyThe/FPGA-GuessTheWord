#!/usr/bin/env bash

set -o errexit
cd ..
pip install -r requirements.txt
cd GuessTheWord
python manage.py collectstatic --no-input
python manage.py migrate