# 🐳 Docker Setup for Legacy Academy Tracking System

This document explains how to run the Legacy Academy Tracking System using Docker for local development and testing.

## 📋 Prerequisites

- Docker installed on your machine
- Docker Compose installed
- Git (to clone the repository)

## 🚀 Quick Start

### 1. Development Setup

Run the full development environment with PostgreSQL:

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f web
```

The application will be available at:
- **Django App**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Admin Panel**: http://localhost:8000/admin/

### 2. With Metabase Analytics

To include Metabase for analytics and reporting:

```bash
# Start with Metabase profile
docker-compose --profile metabase up --build

# Access Metabase at http://localhost:3000
```

## 🗄️ Database Commands

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Load sample data
docker-compose exec web python manage.py loaddata fixtures/sample_data.json

# Access PostgreSQL shell
docker-compose exec db psql -U legacy_user -d legacy_academy_db

# Backup database
docker-compose exec db pg_dump -U legacy_user legacy_academy_db > backup.sql

# Restore database
docker-compose exec -T db psql -U legacy_user legacy_academy_db < backup.sql
```

## 🔧 Development Commands

```bash
# Install new Python packages
docker-compose exec web pip install package_name
# Then rebuild: docker-compose up --build

# Run Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check for issues
docker-compose exec web python manage.py check
```

## 📊 Metabase Setup

When using Metabase for the first time:

1. Go to http://localhost:3000
2. Set up admin account
3. Add PostgreSQL database connection:
   - **Host**: `db`
   - **Port**: `5432`
   - **Database**: `legacy_academy_db`
   - **Username**: `legacy_user`
   - **Password**: `secure_password123`

## 🛠️ Troubleshooting

### Common Issues

**1. Port already in use:**
```bash
# Stop existing containers
docker-compose down

# Check running containers
docker ps

# Kill specific port process
sudo lsof -ti:8000 | xargs kill -9
```

**2. Database connection issues:**
```bash
# Restart database service
docker-compose restart db

# Check database health
docker-compose exec db pg_isready -U legacy_user
```

**3. Permission errors:**
```bash
# Fix volume permissions
docker-compose exec web chown -R app:app /app
```

**4. Build issues:**
```bash
# Clean rebuild
docker-compose down --volumes
docker-compose build --no-cache
docker-compose up
```

### Reset Everything

```bash
# Stop and remove all containers, volumes, and networks
docker-compose down --volumes --remove-orphans

# Remove images
docker-compose down --rmi all

# Start fresh
docker-compose up --build
```

## 🏗️ Project Structure in Docker

```
/app/
├── attendance_system/     # Django project settings
├── schools/              # School management app
├── students/             # Student management app
├── attendance/           # Attendance tracking app
├── visits/               # Home visit management app
├── reports/              # Reports and analytics app
├── templates/            # HTML templates
├── static/               # Static files
├── media/                # User uploads
├── staticfiles/          # Collected static files
└── manage.py             # Django management script
```

## 🌐 Environment Variables

The Docker setup uses `.env.docker` for development variables:

```bash
# View current environment
docker-compose exec web env | grep DJANGO

# Override environment variables
DEBUG=False docker-compose up
```

## 📈 Performance Tips

1. **Use bind mounts for development** (already configured)
2. **Use volumes for data persistence** (PostgreSQL data)
3. **Multi-stage builds** for production (see Dockerfile.prod)
4. **Health checks** for reliable startups

## 🚀 Production Deployment

For production deployment, use:

```bash
# Production build
docker-compose -f docker-compose.prod.yml up --build

# With SSL and nginx
docker-compose -f docker-compose.prod.yml --profile production up
```

## 🔍 Monitoring

```bash
# View container stats
docker stats

# View container logs
docker-compose logs -f web
docker-compose logs -f db

# Execute into running container
docker-compose exec web bash
docker-compose exec db bash
```

## 🔒 Security Notes

- Default passwords are for development only
- Change all credentials for production
- Use Docker secrets for sensitive data in production
- Regular security updates for base images

---

## Next Steps

After successful Docker setup:
1. Access the application at http://localhost:8000
2. Create superuser account
3. Set up school and user data
4. Configure Metabase for analytics
5. Start developing attendance tracking features