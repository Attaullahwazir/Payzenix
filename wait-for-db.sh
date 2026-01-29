#!/bin/bash
# Wait for MySQL to be ready before starting Flask

echo "Waiting for MySQL to be ready..."

# Wait for MySQL on host 'db' port 3306
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt/$max_attempts: Checking MySQL connection..."
    
    # Try to connect to MySQL
    if timeout 5 bash -c "echo > /dev/tcp/db/3306" 2>/dev/null; then
        echo "✓ MySQL is ready on db:3306"
        break
    fi
    
    echo "  MySQL not ready yet, waiting..."
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "✗ MySQL failed to become ready after $max_attempts attempts"
    exit 1
fi

echo "Starting Flask application with gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class sync --timeout 120 --access-logfile - --error-logfile - wsgi:app
