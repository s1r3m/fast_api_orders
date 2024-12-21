#!/usr/bin/env bash
set -ex

# Run migrations.
sed -i 's/localhost:5432/db/' /migrations/alembic.ini
sleep 3  # Wait for DB to init
cd / && poetry run alembic -c /migrations/alembic.ini upgrade head

nginx
poetry run uvicorn main:app --workers 2 --host 0.0.0.0 --port 8000
