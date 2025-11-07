# Task Tracker - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Start Services

```bash
docker-compose up -d
```

Wait ~30 seconds for services to start.

### Step 2: Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### Step 3: Open Application

Visit: **http://localhost:3000**

### Step 4: Create Account

1. Click "Sign up"
2. Fill in the registration form:
   - Email: your@email.com
   - Username: yourname
   - Password: SecurePass123! (must have uppercase, lowercase, number)
3. Click "Sign up"

### Step 5: Create Your First Project

1. Go to "Projects"
2. Click "Create Project"
3. Fill in:
   - Name: My First Project
   - Key: MFP (short identifier)
   - Description: Getting started with Task Tracker
4. Click "Create"

### Step 6: Start Using Kanban Board

1. Click on your project
2. Click "View Board"
3. Click "Create Task" to add your first task
4. Drag tasks between columns (Backlog → To Do → In Progress → Done)

## 🎯 Key Features

### Kanban Board
- **Drag & Drop** - Move tasks between columns
- **Visual Organization** - See all tasks at a glance
- **Color Coding** - Priority and type indicators

### Task Management
- **Priorities**: Low, Medium, High, Critical
- **Types**: Task, Bug, Feature, Improvement
- **Estimates**: Time tracking and story points
- **Details**: Full descriptions and metadata

### Project Organization
- **Multiple Projects** - Organize work by project
- **Team Collaboration** - Assign tasks to team members
- **Status Tracking** - Monitor progress

## 📱 Navigation

- **Dashboard** - Overview of all projects and tasks
- **Projects** - List and manage projects
- **Board** - Kanban view for task management
- **Task Details** - Full information about each task

## 🎨 Color Scheme

The app uses a clean color palette:
- **White** - Main background
- **Gray** - Text and borders
- **Green** (#10B981) - Success states, primary actions
- **Red** (#EF4444) - Errors, critical items

## 🔧 Common Tasks

### Create a Task
1. Go to project board
2. Click "Create Task"
3. Fill in title, description, priority, type
4. Click "Create"

### Move a Task
- **Drag & Drop** - Grab task card and drag to new column
- **Or** click task → change status dropdown

### Update a Task
1. Click on task card
2. View/edit details
3. Change status, add time, update description

### Create a Project
1. Go to Projects page
2. Click "Create Project"
3. Enter name, key, description
4. Start adding tasks

## 📊 API Access

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🆘 Need Help?

### Application Not Loading?

```bash
# Check services are running
docker-compose ps

# View logs
docker-compose logs -f
```

### Can't Create Account?

- Ensure password meets requirements (8+ chars, uppercase, lowercase, number)
- Check backend logs: `docker-compose logs backend`

### Database Issues?

```bash
# Re-run migrations
docker-compose exec backend alembic upgrade head

# Or reset everything
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## 🔐 Default Credentials

No default users - you must register your first account via the UI or API.

## 📦 What's Running?

After `docker-compose up`:

- **Frontend** (Vue.js) - Port 3000
- **Backend** (FastAPI) - Port 8000
- **PostgreSQL** - Port 5432
- **Redis** - Port 6379
- **Nginx** - Port 80

## ⚡ Next Steps

1. ✅ Create your first project
2. ✅ Add some tasks
3. ✅ Try drag & drop on the Kanban board
4. ✅ Explore task details
5. ✅ Check out the Dashboard

## 🎓 Learn More

- Full documentation: `README.md`
- Deployment guide: `DEPLOYMENT.md`
- API docs: http://localhost:8000/api/v1/docs

---

**Enjoy Task Tracking! 🎉**
