#!/bin/sh
source .venv/bin/activate
python -u -m flask --app main run --host=0.0.0.0 --port=${PORT:-8080}
