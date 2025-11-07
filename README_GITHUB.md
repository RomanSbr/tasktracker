<div align="center">

# 📋 Task Tracker

[![CI](https://github.com/RomanSbr/tasktracker/workflows/CI/badge.svg)](https://github.com/RomanSbr/tasktracker/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Vue](https://img.shields.io/badge/vue-3.3+-4FC08D.svg)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.3+-3178C6.svg)](https://www.typescriptlang.org/)

**Modern task management system with Kanban board**

Built with FastAPI, Vue 3, PostgreSQL, and Docker

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Demo](#-demo)

![Task Tracker Demo](https://via.placeholder.com/800x400/10B981/FFFFFF?text=Task+Tracker+Kanban+Board)

</div>

---

## ✨ Features

- 🔐 **JWT Authentication** - Secure login with access & refresh tokens
- 📊 **Kanban Board** - Drag & drop tasks between columns
- 📋 **Project Management** - Organize tasks by projects
- 🎯 **Task Management** - Priorities, types, estimates, and history
- 💬 **Comments** - Discuss tasks with team members
- 📈 **Dashboard** - Overview with statistics and charts
- 🎨 **Modern UI** - Clean design with TailwindCSS
- 🐳 **Docker Ready** - One-command deployment
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- 🚀 **Fast** - Async backend with optimized queries

## 🎯 Tech Stack

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

### Frontend
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)

### Infrastructure
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose 2.0+
- OR: Python 3.11+ and Node.js 18+

### One-Command Start

```bash
git clone https://github.com/RomanSbr/tasktracker.git
cd tasktracker
docker-compose up -d && docker-compose exec backend alembic upgrade head
```

Open **http://localhost:3000** 🎉

### Using Makefile

```bash
make up        # Start all services
make migrate   # Run database migrations
make logs      # View logs
make down      # Stop services
make clean     # Remove all data
```

## 📖 Documentation

- [📚 Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [🚀 Deployment Guide](DEPLOYMENT.md) - Production deployment
- [📋 Project Overview](PROJECT_OVERVIEW.md) - Full feature list
- [🔧 API Documentation](http://localhost:8000/api/v1/docs) - Interactive API docs

## 🎨 Screenshots

### Kanban Board
![Kanban Board](https://via.placeholder.com/800x500/10B981/FFFFFF?text=Kanban+Board+with+Drag+%26+Drop)

### Dashboard
![Dashboard](https://via.placeholder.com/800x500/10B981/FFFFFF?text=Dashboard+with+Analytics)

### Task Detail
![Task Detail](https://via.placeholder.com/800x500/10B981/FFFFFF?text=Task+Detail+View)

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Nginx (Reverse Proxy)          │
├──────────────┬──────────────────────────┤
│   Frontend   │        Backend           │
│   (Vue 3)    │       (FastAPI)          │
└──────────────┴──────────────────────────┘
                      ↓
        ┌─────────────┴─────────────┐
        │                           │
   PostgreSQL                    Redis
   (Database)                   (Cache)
```

## 📋 Features in Detail

### Kanban Board
- ✅ 6 status columns (Backlog → Done)
- ✅ Drag & drop between columns
- ✅ Visual priority indicators
- ✅ Task counters per column
- ✅ Quick filters

### Task Management
- ✅ 4 priority levels (Low to Critical)
- ✅ 4 task types (Task, Bug, Feature, Improvement)
- ✅ Time tracking (estimated/logged)
- ✅ Story points
- ✅ Due dates
- ✅ Tags support
- ✅ Complete history tracking

### User Management
- ✅ Registration & Login
- ✅ JWT with refresh tokens
- ✅ Password strength validation
- ✅ Profile management

## 🛠️ Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Database Migrations

```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head
```

## 🧪 Testing

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test
```

## 🎨 Color Palette

- **White**: #FFFFFF - Clean backgrounds
- **Gray**: #6B7280, #9CA3AF, #E5E7EB - Text and borders
- **Green**: #10B981, #059669 - Success, primary actions
- **Red**: #EF4444, #DC2626 - Errors, critical items

## 📊 Project Statistics

- **3,300+** lines of code
- **60+** source files
- **8** database tables
- **18+** API endpoints
- **7** UI pages
- **100%** Docker ready

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Vue.js](https://vuejs.org/) - Progressive JavaScript framework
- [TailwindCSS](https://tailwindcss.com/) - Utility-first CSS framework
- [PostgreSQL](https://www.postgresql.org/) - Powerful open-source database

## 📧 Contact

Roman Sbr - [@RomanSbr](https://github.com/RomanSbr)

Project Link: [https://github.com/RomanSbr/tasktracker](https://github.com/RomanSbr/tasktracker)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ using FastAPI and Vue 3

</div>
