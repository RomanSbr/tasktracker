#!/bin/bash
set -e

echo "🔧 Initializing Task Tracker Database..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
until docker-compose exec -T postgres pg_isready -U tasktracker; do
  sleep 1
done

echo "✅ PostgreSQL is ready!"

# Run migrations
echo "📦 Running database migrations..."
docker-compose exec -T backend alembic upgrade head

echo "✨ Database initialized successfully!"
echo ""
echo "🚀 You can now access:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/v1/docs"
