#!/bin/bash

echo "🚀 Updating package lists and installing system dependencies..."
sudo apt update && sudo apt install -y python3-pip python3-venv lsof curl postgresql postgresql-contrib

echo "🚀 Installing global Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install fastapi uvicorn requests sqlalchemy passlib bcrypt pydantic pyjwt asyncpg geoalchemy2 numpy python-jose pyproj pydantic[email]

echo "🔍 Checking if PostgreSQL is installed..."
if ! command -v psql &>/dev/null; then
    echo "⚠️ PostgreSQL not found! Installing..."
    sudo apt install -y postgresql postgresql-contrib
fi

echo "🔍 Checking if PostgreSQL is running..."
if ! systemctl is-active --quiet postgresql; then
    echo "⚠️ PostgreSQL is not running! Starting PostgreSQL..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
else
    echo "✅ PostgreSQL is running."
fi

echo "🔍 Checking for running services and stopping them first..."
for port in {8001..8005}; do
    pid=$(sudo lsof -ti :$port)
    if [ ! -z "$pid" ]; then
        echo "🔴 Killing process on port $port (PID: $pid)..."
        sudo kill -9 $pid
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
      python3 -m uvicorn main:app --reload --host 0.0.0.0 --port "$PORT" &
    )
done

echo "✅ All services started!"
