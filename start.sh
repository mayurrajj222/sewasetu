#!/bin/bash
set -e

echo "Starting PostgreSQL..."
service postgresql start

echo "Configuring PostgreSQL user and database..."
su - postgres -c "psql -c \"CREATE USER sewasetu WITH SUPERUSER PASSWORD 'sewasetu123';\"" 2>/dev/null || true
su - postgres -c "psql -c \"CREATE DATABASE sewasetu OWNER sewasetu;\"" 2>/dev/null || true
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE sewasetu TO sewasetu;\"" 2>/dev/null || true

# Check if tables already exist
TABLE_COUNT=$(su - postgres -c "psql -d sewasetu -t -c \"SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';\"" 2>/dev/null | tr -d ' ' || echo "0")

if [ "$TABLE_COUNT" -eq "0" ] || [ -z "$TABLE_COUNT" ]; then
    echo "Loading schema.sql..."
    su - postgres -c "psql -d sewasetu -f /app/schema.sql"
    if [ -f "/seed/seed.sql" ]; then
        echo "Loading seed.sql (100,000 citizens)..."
        su - postgres -c "psql -d sewasetu -f /seed/seed.sql"
    fi
fi

echo "Starting SMS gateway on port 8025..."
python3 /smsgw/app.py &

echo "Starting cron service..."
cron 2>/dev/null || true

export DB_HOST="127.0.0.1"
export DB_PORT="5432"
export DB_NAME="sewasetu"
export DB_USER="sewasetu"
export DB_PASS="sewasetu123"
export SMS_GATEWAY_URL="http://127.0.0.1:8025"

APP_PORT="${PORT:-8000}"
echo "Starting Sewa Setu application on port $APP_PORT..."
exec gunicorn --bind "0.0.0.0:$APP_PORT" --workers 4 --threads 4 --timeout 60 --chdir /app app:app
