# DataDiNascita - Birthday Reminder Application

**Never forget a birthday again!**

A modern, full-stack birthday and event tracking application built with Django 5.1, Django REST Framework, React 18, and TypeScript.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.1-green)
![React](https://img.shields.io/badge/react-18.3-blue)
![TypeScript](https://img.shields.io/badge/typescript-5.4-blue)

---

## Features

✨ **Core Features**
- 👥 Contact management with birthdays
- 📅 Custom events (anniversaries, holidays, etc.)
- 🔔 Upcoming birthday notifications
- 📊 Dashboard with statistics
- 📤 CSV import/export
- 🔍 Search and filter contacts
- 🎂 Age calculation and tracking

🔒 **Security**
- JWT authentication
- Secure password hashing (Argon2)
- CORS protection
- Rate limiting
- HTTPS enforcement (production)

🚀 **Modern Stack**
- RESTful API with Django REST Framework
- React + TypeScript SPA
- Responsive design with Tailwind CSS
- PostgreSQL database
- Docker support
- Automated testing
- CI/CD pipeline

---

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/INSTER-MEDIA/datadinascita.git
cd datadinascita

# Set up environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Generate a secret key and add to backend/.env
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))"

# Start all services
docker-compose up -d

# Create superuser
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# Admin: http://localhost:8000/admin
# API Docs: http://localhost:8000/api/docs/
```

### Manual Setup

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed setup instructions.

---

## Project Structure

```
datadinascita/
├── backend/                    # Django backend
│   ├── config/                 # Django settings & URLs
│   ├── birthdays/              # Main app (models, views, serializers)
│   ├── users/                  # User authentication app
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend Docker image
│   └── pytest.ini              # Test configuration
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── lib/                # API client & utilities
│   │   ├── stores/             # Zustand state management
│   │   └── types/              # TypeScript types
│   ├── package.json            # npm dependencies
│   ├── Dockerfile              # Frontend Docker image
│   └── vite.config.ts          # Vite configuration
├── .github/workflows/          # CI/CD pipelines
├── docker-compose.yml          # Docker Compose configuration
├── TECH_STACK_AUDIT.md        # Technology audit report
├── MIGRATION_GUIDE.md         # Migration documentation
└── README.md                   # This file
```

---

## Technology Stack

### Backend
- **Framework**: Django 5.1
- **API**: Django REST Framework 3.14
- **Database**: PostgreSQL 16
- **Authentication**: JWT (Simple JWT)
- **Password Hashing**: Argon2
- **API Docs**: drf-spectacular (OpenAPI/Swagger)
- **Testing**: pytest, pytest-django
- **Code Quality**: ruff, black, isort

### Frontend
- **Framework**: React 18
- **Language**: TypeScript 5
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3
- **State Management**: Zustand
- **Data Fetching**: React Query (TanStack Query)
- **Routing**: React Router 6
- **Forms**: React Hook Form + Zod
- **Icons**: Lucide React

### DevOps
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment**: Google Cloud Run, Vercel
- **Monitoring**: Sentry
- **Database**: Cloud SQL, Neon, Supabase

---

## API Documentation

Full API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Quick Examples

**Register a new user:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Create a contact:**
```bash
curl -X POST http://localhost:8000/api/v1/birthdays/contacts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "John Doe",
    "birthday": "1990-05-15",
    "email": "john@example.com"
  }'
```

---

## Development

### Backend Development

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
pytest

# Run linting
ruff check .
black --check .
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm run test

# Build for production
npm run build

# Run linting
npm run lint
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests with coverage
pytest --cov

# Run specific test file
pytest birthdays/tests.py

# Run with verbose output
pytest -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run tests in watch mode
npm run test -- --watch

# Run tests with UI
npm run test:ui
```

---

## Deployment

### Option 1: Google Cloud Run

```bash
# Backend
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/datadinascita-backend
gcloud run deploy datadinascita-backend \
  --image gcr.io/PROJECT_ID/datadinascita-backend \
  --platform managed \
  --region us-central1

# Frontend
cd frontend
npm run build
# Deploy dist/ to Cloud Storage + Cloud CDN or use Cloud Run
```

### Option 2: Railway (Easiest)

1. Push code to GitHub
2. Visit https://railway.app
3. Click "New Project" → "Deploy from GitHub repo"
4. Add PostgreSQL service
5. Set environment variables
6. Deploy!

### Option 3: Vercel (Frontend) + Cloud Run (Backend)

```bash
# Frontend to Vercel
cd frontend
vercel

# Backend to Cloud Run (see Option 1)
```

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed deployment instructions.

---

## Environment Variables

### Backend

```bash
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,.run.app
DATABASE_URL=postgresql://user:password@host:5432/dbname
CORS_ALLOWED_ORIGINS=https://yourdomain.com
SENTRY_DSN=your-sentry-dsn  # Optional
```

### Frontend

```bash
VITE_API_URL=http://localhost:8000  # Development
# VITE_API_URL=https://api.yourdomain.com  # Production
```

---

## Migration from Legacy Version

This project is a complete modernization of the original Google App Engine (Python 2.7) application.

**Key Changes:**
- ✅ Python 2.7 → Python 3.12
- ✅ Django 0.96 → Django 5.1
- ✅ GAE Datastore → PostgreSQL
- ✅ Server-side templates → React SPA
- ✅ No modern tooling → Full CI/CD pipeline

For migration instructions, see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) and [TECH_STACK_AUDIT.md](TECH_STACK_AUDIT.md).

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- **Backend**: Follow PEP 8, use `black` and `ruff`
- **Frontend**: Follow ESLint rules, use Prettier
- **Commits**: Use conventional commits (e.g., `feat:`, `fix:`, `docs:`)

---

## License

Copyright © 2010-2025 [INSTER-MEDIA](http://inster-media.com/)

---

## Support

- 📧 Email: support@inster-media.com
- 🐛 Issues: [GitHub Issues](https://github.com/INSTER-MEDIA/datadinascita/issues)
- 📖 Docs: [API Documentation](http://localhost:8000/api/docs/)

---

## Roadmap

- [ ] Email notifications for upcoming birthdays
- [ ] SMS notifications (Twilio integration)
- [ ] Push notifications (PWA)
- [ ] Mobile apps (React Native)
- [ ] Social media integration
- [ ] Calendar export (iCal)
- [ ] Recurring events
- [ ] Gift ideas tracking
- [ ] Multi-language support

---

## Acknowledgments

- Original template by [Designs By Darren](http://www.designsbydarren.com)
- Icons by [Lucide](https://lucide.dev/)
- Built with [Django](https://www.djangoproject.com/) and [React](https://react.dev/)

---

**Made with ❤️ by INSTER-MEDIA**
