#!/usr/bin/env bash

PROJECT=flask_project

# create virtualenv if it doesn't exist
if [ ! -d /$PROJECT/venv ]; then
    python -m venv /$PROJECT/venv
    /$PROJECT/venv/bin/pip install -U pip
fi

. /$PROJECT/venv/bin/activate
cd /$PROJECT

$1
