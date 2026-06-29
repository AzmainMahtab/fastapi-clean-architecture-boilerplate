#!/bin/bash
set -e

echo ">>> Waiting for PostgreSQL to be ready..."
until pg_isready -h "${POSTGRES_HOST:-postgres}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-app_user}" -q; do
  echo ">>> Postgres is unavailable - sleeping 1s"
  sleep 1
done
echo ">>> PostgreSQL is ready!"

# Run Alembic migrations if the directory exists
if [ -d "alembic" ]; then
  echo ">>> Running Alembic migrations..."
  alembic upgrade head
  echo ">>> Migrations complete!"
else
  echo ">>> Alembic directory not found, skipping migrations."
fi

# Switch execution based on environment variable
if [ "$ENVIRONMENT" = "local" ]; then
  echo ">>> Starting LOCAL server (Uvicorn with hot-reload)..."
  # Note: app.main:app means app/main.py structure
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
  echo ">>> Starting PRODUCTION server (Gunicorn + Uvicorn workers)..."
  # -w 4: 4 worker processes (tune to your CPU: 2 * cores + 1)
  # -k uvicorn.workers.UvicornWorker: ASGI worker class
  # --timeout 120: Prevents worker kills on slow startup/heavy queries
  exec gunicorn app.main:app \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
fi
