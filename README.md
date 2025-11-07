# Task Tracker

Modern task management system built with FastAPI, Vue 3, and PostgreSQL.

## Features

- 🔐 JWT Authentication & Authorization
- 📋 Project & Task Management
- 👥 Team Collaboration
- 💬 Real-time Comments & Notifications
- 📊 Analytics & Dashboards
- 🎯 Kanban Board with Drag & Drop
- 🔍 Advanced Search & Filtering
- ⚡ Real-time Updates via WebSocket

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (Async)
- **Cache**: Redis
- **Migration**: Alembic
- **Validation**: Pydantic

### Frontend
- **Framework**: Vue 3 + TypeScript
- **State**: Pinia
- **Router**: Vue Router
- **Styling**: TailwindCSS
- **Build**: Vite

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for detailed 5-minute setup guide.

### Prerequisites
- Docker & Docker Compose 2.0+
- OR: Python 3.11+ and Node.js 18+ (for local development)

### One-Command Start

```bash
docker-compose up -d && docker-compose exec backend alembic upgrade head
```

Then visit **http://localhost:3000**

### Using Makefile

```bash
make up        # Start all services
make migrate   # Run database migrations
make logs      # View logs
make down      # Stop services
```

### Access Points
- **Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs
- **Via Nginx**: http://localhost

### Local Development (without Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
tasktracker/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Config, security
│   │   ├── crud/        # Database operations
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utilities
│   ├── alembic/         # Database migrations
│   └── tests/           # Tests
├── frontend/            # Vue 3 application
│   ├── src/
│   │   ├── api/        # API clients
│   │   ├── components/ # Vue components
│   │   ├── pages/      # Page components
│   │   ├── router/     # Vue Router
│   │   ├── stores/     # Pinia stores
│   │   └── styles/     # Global styles
│   └── tests/          # Tests
└── docker-compose.yml  # Docker services

```

## Color Palette

- White: #FFFFFF
- Gray: #6B7280, #9CA3AF, #E5E7EB
- Red: #EF4444, #DC2626
- Green: #10B981, #059669

## Documentation

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide
- **API Docs**: http://localhost:8000/api/v1/docs - Interactive API documentation

## Available Scripts

Located in `scripts/` directory:

- `init-db.sh` - Initialize database with migrations
- `create-admin.sh` - Create admin user interactively
- `backup.sh` - Backup database
- `restore.sh` - Restore from backup

## Development Commands

### Backend
```bash
# Run tests
docker-compose exec backend pytest

# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Run migrations
docker-compose exec backend alembic upgrade head

# Downgrade migration
docker-compose exec backend alembic downgrade -1
```

### Frontend
```bash
# Install dependencies
cd frontend && npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

## Features Implemented

✅ User Authentication (JWT)
✅ Project Management
✅ Task Management with Kanban Board
✅ Drag & Drop Interface
✅ Task Priorities & Types
✅ Task History Tracking
✅ Comments System
✅ Dashboard with Statistics
✅ Responsive Design
✅ Docker Deployment
✅ Database Migrations
✅ API Documentation

## Tech Highlights

- **Async Everything** - FastAPI + SQLAlchemy async for high performance
- **Type Safety** - TypeScript frontend + Pydantic backend
- **Modern UI** - TailwindCSS with custom color palette (White, Gray, Green, Red)
- **Real-time Ready** - WebSocket support for live updates
- **Production Ready** - Docker Compose with Nginx reverse proxy
- **Developer Friendly** - Hot reload, migrations, comprehensive docs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- Documentation: See [QUICKSTART.md](QUICKSTART.md) and [DEPLOYMENT.md](DEPLOYMENT.md)
- Issues: GitHub Issues
- API Reference: http://localhost:8000/api/v1/docs

---

**Built with ❤️ using FastAPI and Vue 3**
