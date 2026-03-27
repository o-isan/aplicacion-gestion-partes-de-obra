#!/bin/bash

set -e

echo "Waiting for PostgreSQL..."
while ! python -c "import socket; s = socket.socket(); s.settimeout(2); s.connect(('$POSTGRES_HOST', ${POSTGRES_PORT:-5432})); s.close()" 2>/dev/null; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "PostgreSQL is up!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
