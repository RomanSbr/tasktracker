# Task Tracker - Deployment Guide

## Quick Start with Docker Compose

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd tasktracker
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env and set your values (SECRET_KEY, database passwords, etc.)
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Wait for services to be ready** (check logs)
```bash
docker-compose logs -f
```

5. **Run database migrations**
```bash
docker-compose exec backend alembic upgrade head
```

6. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- Main App: http://localhost (via Nginx)

### Create First User

Register via the UI at http://localhost:3000/register or use the API:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "SecurePass123!",
    "first_name": "Admin",
    "last_name": "User"
  }'
```

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql+asyncpg://tasktracker:tasktracker_password_2024@localhost:5432/tasktracker
export SECRET_KEY=your-secret-key-min-32-chars

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm install
cp .env.example .env

# Start dev server
npm run dev
```

Visit http://localhost:5173

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U tasktracker -d tasktracker

# Common queries
\dt  # List tables
\d users  # Describe users table
SELECT * FROM users;
```

### Redis Access

```bash
# Connect to Redis
docker-compose exec redis redis-cli -a redis_password_2024

# Common commands
KEYS *
GET key_name
FLUSHALL  # Clear all data
```

## Production Deployment

### Security Checklist

- [ ] Change all default passwords in `.env`
- [ ] Set strong `SECRET_KEY` (min 32 chars)
- [ ] Enable HTTPS (use Let's Encrypt or your SSL certificates)
- [ ] Set proper CORS origins
- [ ] Configure firewall rules
- [ ] Enable database backups
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure Sentry for error tracking
- [ ] Review and set proper file upload limits
- [ ] Enable rate limiting

### Environment Variables

```bash
# Required
SECRET_KEY=your-very-secure-secret-key-at-least-32-characters-long
POSTGRES_PASSWORD=your-secure-database-password
REDIS_PASSWORD=your-secure-redis-password

# Optional
SENTRY_DSN=your-sentry-dsn
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### SSL/HTTPS Setup

Update `nginx/nginx.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    # ... rest of config
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Database Backups

```bash
# Backup
docker-compose exec postgres pg_dump -U tasktracker tasktracker > backup_$(date +%Y%m%d).sql

# Restore
docker-compose exec -T postgres psql -U tasktracker tasktracker < backup_20240101.sql
```

## Troubleshooting

### Backend not starting

```bash
# Check logs
docker-compose logs backend

# Check database connection
docker-compose exec backend python -c "from app.db.session import engine; import asyncio; asyncio.run(engine.connect())"
```

### Frontend not loading

```bash
# Check logs
docker-compose logs frontend

# Rebuild frontend
docker-compose up -d --build frontend
```

### Database migration issues

```bash
# Check current revision
docker-compose exec backend alembic current

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Downgrade one revision
docker-compose exec backend alembic downgrade -1
```

### Reset Everything

```bash
# Stop and remove all containers, volumes
docker-compose down -v

# Remove all data
rm -rf postgres_data redis_data

# Start fresh
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## Monitoring

### Check Service Health

```bash
# Backend health
curl http://localhost:8000/health

# Check all services
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Performance Metrics

Access Prometheus at http://localhost:9090 (if configured)
Access Grafana at http://localhost:3001 (if configured)

## Scaling

### Horizontal Scaling

```bash
# Scale backend to 3 instances
docker-compose up -d --scale backend=3

# Scale frontend to 2 instances
docker-compose up -d --scale frontend=2
```

### Database Optimization

```sql
-- Add indexes for better performance
CREATE INDEX CONCURRENTLY idx_tasks_project_status ON tasks(project_id, status);
CREATE INDEX CONCURRENTLY idx_tasks_assignee_status ON tasks(assignee_id, status);

-- Analyze tables
ANALYZE tasks;
ANALYZE users;
ANALYZE projects;
```

## Maintenance

### Update Dependencies

```bash
# Backend
cd backend
pip install -U -r requirements.txt

# Frontend
cd frontend
npm update
```

### Clear Cache

```bash
# Redis
docker-compose exec redis redis-cli -a redis_password_2024 FLUSHALL

# Docker build cache
docker system prune -a
```

## Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Documentation: /docs
