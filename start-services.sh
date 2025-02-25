#!/bin/bash

echo "🚀 Installing global dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn requests sqlalchemy passlib bcrypt pydantic pyjwt asyncpg geoalchemy2 numpy python-jose pyproj pydantic[email]

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
if ! pg_isready -h localhost -p 5432 -U user1 > /dev/null 2>&1; then
    echo "⚠️ PostgreSQL is not running! Starting PostgreSQL..."
    brew services start postgresql
    sleep 5  # Give it time to start
else
    echo "✅ PostgreSQL is running."
fi

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
SERVICES=("auth-service" "location-service" "heatmap-service" "ml-service" "external-api-fetcher")
PORTS=(8001 8002 8003 8004 8005)

# Function to initialize database tables asynchronously
initialize_db() {
    SERVICE_DIR=$1
    echo "▶️ Ensuring database tables exist for $SERVICE_DIR..."
    python3 - <<EOF
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path("$SERVICE_DIR").resolve()))
try:
    from dependencies import Base, engine

    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database initialized for $SERVICE_DIR")

    asyncio.run(init_db())

except ImportError as e:
    print(f"⚠️ Could not initialize database for $SERVICE_DIR: {e}")
EOF
}

# Start each service
for i in "${!SERVICES[@]}"; do
    SERVICE_DIR="services/${SERVICES[$i]}"
    PORT="${PORTS[$i]}"

    if [[ ! -d "$SERVICE_DIR" ]]; then
        echo "❌ Error: Directory $SERVICE_DIR not found! Skipping..."
        continue
    fi

    # Initialize DB tables correctly for async engines
    if [[ "${SERVICES[$i]}" != "heatmap-service" ]]; then
        initialize_db "$SERVICE_DIR"
    fi

    echo "▶️ Starting $SERVICE_DIR on port $PORT..."
    (
      cd "$SERVICE_DIR" || exit
      uvicorn main:app --reload --host 0.0.0.0 --port "$PORT" &
    )
done

echo "✅ All services started!"
