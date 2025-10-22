# Migration Guide: Legacy to Modern Stack

This guide walks you through migrating from the legacy Google App Engine Python 2.7 application to the modern Django 5.1 + React stack.

## Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose installed
- Git installed

### 1. Clone and Set Up

```bash
cd /path/to/datadinascita

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Generate a new SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
# Add the generated key to backend/.env
```

### 2. Start with Docker Compose

```bash
# Start all services (database, backend, frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# Backend will be available at: http://localhost:8000
# Frontend will be available at: http://localhost:5173
# API docs at: http://localhost:8000/api/docs/
```

### 3. Create Superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/

---

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and set SECRET_KEY, DATABASE_URL, etc.

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Start development server
npm run dev
```

---

## Data Migration from GAE Datastore

### Step 1: Export Data from GAE

```bash
# Using Google Cloud Console or gcloud CLI
gcloud datastore export gs://YOUR_BUCKET/datastore-export \
  --kinds=Person,Event,Contact

# Download the export
gsutil -m cp -r gs://YOUR_BUCKET/datastore-export ./gae-export
```

### Step 2: Convert and Import

We've created a migration script to help:

```bash
cd backend

# Run the migration script
python manage.py import_from_gae --export-dir=../gae-export

# Or manually import using Django shell
python manage.py shell
```

```python
# In Django shell
from birthdays.models import Contact
from datetime import datetime

# Example: Import a contact
Contact.objects.create(
    name="John Doe",
    birthday=datetime(1990, 5, 15).date(),
    email="john@example.com",
    owner=request.user  # You'll need to get the user first
)
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest birthdays/tests.py

# Run specific test
pytest birthdays/tests.py::TestContactAPI::test_create_contact
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with UI
npm run test:ui
```

---

## Deployment

### Deploy to Cloud Run (Backend)

```bash
cd backend

# Build and push Docker image
gcloud builds submit --tag gcr.io/PROJECT_ID/datadinascita-backend

# Deploy to Cloud Run
gcloud run deploy datadinascita-backend \
  --image gcr.io/PROJECT_ID/datadinascita-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DEBUG=False \
  --set-secrets DATABASE_URL=database-url:latest,SECRET_KEY=django-secret-key:latest

# Or use the cloudrun.yml configuration
gcloud run services replace cloudrun.yml
```

### Deploy to Vercel (Frontend)

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard:
# VITE_API_URL=https://your-backend-url.run.app
```

### Deploy to Railway (Full Stack)

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Add PostgreSQL service
5. Configure environment variables
6. Deploy!

---

## Environment Variables Reference

### Backend (.env)

```bash
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,.run.app

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://yourfrontend.vercel.app

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000  # Development
# VITE_API_URL=https://your-backend.run.app  # Production
```

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - Register new user
- `POST /api/v1/auth/login/` - Login (get JWT tokens)
- `POST /api/v1/auth/logout/` - Logout
- `POST /api/v1/auth/token/refresh/` - Refresh access token
- `GET /api/v1/auth/profile/` - Get user profile
- `PATCH /api/v1/auth/profile/` - Update profile

### Contacts
- `GET /api/v1/birthdays/contacts/` - List contacts
- `POST /api/v1/birthdays/contacts/` - Create contact
- `GET /api/v1/birthdays/contacts/{id}/` - Get contact
- `PATCH /api/v1/birthdays/contacts/{id}/` - Update contact
- `DELETE /api/v1/birthdays/contacts/{id}/` - Delete contact
- `GET /api/v1/birthdays/contacts/upcoming_birthdays/` - Upcoming birthdays
- `POST /api/v1/birthdays/contacts/import_csv/` - Import CSV
- `GET /api/v1/birthdays/contacts/export_csv/` - Export CSV
- `DELETE /api/v1/birthdays/contacts/delete_all/` - Delete all contacts

### Events
- `GET /api/v1/birthdays/events/` - List events
- `POST /api/v1/birthdays/events/` - Create event
- `GET /api/v1/birthdays/events/{id}/` - Get event
- `PATCH /api/v1/birthdays/events/{id}/` - Update event
- `DELETE /api/v1/birthdays/events/{id}/` - Delete event
- `GET /api/v1/birthdays/events/upcoming_events/` - Upcoming events

---

## Troubleshooting

### Backend Issues

**Database connection errors:**
```bash
# Check DATABASE_URL is correct
echo $DATABASE_URL

# Test database connection
python manage.py dbshell
```

**Migration errors:**
```bash
# Reset migrations (DANGER: loses data)
python manage.py migrate birthdays zero
python manage.py migrate

# Or create fresh database
python manage.py flush
python manage.py migrate
```

### Frontend Issues

**CORS errors:**
- Ensure `CORS_ALLOWED_ORIGINS` in backend/.env includes your frontend URL
- Check that backend is running and accessible

**Build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## Next Steps

1. ✅ Complete data migration from GAE
2. ✅ Set up production database (Cloud SQL/Neon)
3. ✅ Configure custom domain
4. ✅ Set up email notifications
5. ✅ Enable error tracking (Sentry)
6. ✅ Set up backups
7. ✅ Configure monitoring

## Support

For questions or issues:
- Check the [Tech Stack Audit](TECH_STACK_AUDIT.md)
- Review API docs at `/api/docs/`
- Open an issue on GitHub
