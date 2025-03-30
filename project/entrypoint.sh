#!/bin/sh
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Checking if database 'locker_dev' exists..."
DB_EXISTS=$(PGPASSWORD=postgres psql -h db -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'locker_dev';" | tr -d '[:space:]')

if [ "$DB_EXISTS" = "1" ]; then
  echo "The DB already exists"
else
  echo "Creating database: 'locker_dev'..."
  PGPASSWORD=postgres psql -h db -U postgres -c "CREATE DATABASE locker_dev;"
  echo "BD created"
fi

exec "$@"
