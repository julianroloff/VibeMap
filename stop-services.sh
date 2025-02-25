#!/bin/bash

echo "🛑 Stopping all running services..."

# Define service ports
PORTS=(8001 8002 8003 8004 8005)

# Stop each service running on the defined ports
for PORT in "${PORTS[@]}"; do
    PID=$(lsof -ti :$PORT)
    if [ ! -z "$PID" ]; then
        echo "🔴 Stopping service on port $PORT (PID: $PID)..."
        kill $PID
        sleep 2  # Wait for graceful shutdown
        if ps -p $PID > /dev/null; then
            echo "⚠️ Service on port $PORT did not stop, forcing shutdown..."
            kill -9 $PID
        fi
    else
        echo "✅ No service running on port $PORT."
    fi
done

echo "✅ All services stopped!"
