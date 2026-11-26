#!/bin/sh

echo "Waiting for database..."

until python -c "
import os
import psycopg2

conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port=os.environ['DB_PORT'],
    dbname=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD']
)
conn.close()
"
do
    echo "Database is not ready. Retrying in 2 seconds..."
    sleep 2
done

echo "Database connection successful!"

echo "Creating database tables..."
python -m app.create_tables

echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000