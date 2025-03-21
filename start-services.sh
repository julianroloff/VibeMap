#!/bin/bash

echo "🚀 Installing global dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn requests sqlalchemy passlib bcrypt pydantic pyjwt asyncpg geoalchemy2 numpy python-jose pyproj pydantic[email] httpx pydantic-settings

echo "🔍 Checking if Homebrew is installed..."
if ! command -v brew &>/dev/null; then
    echo "⚠️ Homebrew not found! Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew is installed."
fi

echo "🔍 Checking if PostgreSQL is installed..."
if ! command -v psql &>/dev/null; then
    echo "⚠️ PostgreSQL not found! Installing..."
    brew install postgresql
fi

echo "🔍 Checking if PostgreSQL is running..."
if ! pg_isready -q; then
    echo "⚠️ PostgreSQL is not running! Starting PostgreSQL..."
    brew services start postgresql
else
    echo "✅ PostgreSQL is running."
fi

# Ensure PostgreSQL user exists
echo "🔍 Checking if user 'user1' exists..."
USER_EXISTS=$(psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='user1'")
if [[ -z "$USER_EXISTS" ]]; then
    echo "⚠️ User 'user1' not found! Creating user..."
    psql -U postgres -c "CREATE USER user1 WITH PASSWORD 'test'; ALTER ROLE user1 CREATEDB;"
else
    echo "✅ User 'user1' exists."
fi

# Ensure databases exist
DBS=("users" "location_db" "apilocation_db")
for DB in "${DBS[@]}"; do
    echo "🔍 Checking if database '$DB' exists..."
    DB_EXISTS=$(psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB'")
    if [[ -z "$DB_EXISTS" ]]; then
        echo "⚠️ Database '$DB' not found! Creating it..."
        psql -U postgres -c "CREATE DATABASE $DB OWNER user1;"
    else
        echo "✅ Database '$DB' exists."
    fi
done

echo "🔍 Checking for running services and stopping them first..."
for port in {8001..8005}; do
    pid=$(lsof -ti :$port)
    if [ ! -z "$pid" ]; then
        echo "🔴 Killing process on port $port (PID: $pid)..."
        kill -9 $pid
    fi
done

echo "🚀 Starting all services..."

# Define service directories and ports
SERVICES=("auth-service" "location-service" "ml-service" "external-api-fetcher")
PORTS=(8001 8002 8004 8005)

# Start each service
for i in "${!SERVICES[@]}"; do
    SERVICE_DIR="services/${SERVICES[$i]}"
    PORT="${PORTS[$i]}"

    if [[ ! -d "$SERVICE_DIR" ]]; then
        echo "❌ Error: Directory $SERVICE_DIR not found! Skipping..."
        continue
    fi

    echo "▶️ Starting $SERVICE_DIR on port $PORT..."
    (
      cd "$SERVICE_DIR" || exit
      uvicorn main:app --reload --host 0.0.0.0 --port "$PORT" &
    )
done

echo "✅ All services started!"
