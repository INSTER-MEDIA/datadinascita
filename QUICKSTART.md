# 🚀 Quick Start - Run Locally with Docker

Get DataDiNascita running on your local machine in **5 minutes**!

## Prerequisites

- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))
- Git installed

That's it! No need to install Python, Node.js, PostgreSQL, or anything else.

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/INSTER-MEDIA/datadinascita.git
cd datadinascita
```

Or if you already have it:

```bash
cd datadinascita
git checkout claude/tech-stack-audit-011CUN5x7ceDqhdXQgcngib5
```

---

## Step 2: Set Up Environment Files

```bash
# Copy environment templates
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

---

## Step 3: Generate Secret Key

**On macOS/Linux:**
```bash
# Generate and display SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))"
```

**On Windows (PowerShell):**
```powershell
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))"
```

**Copy the output** (looks like `SECRET_KEY=abc123...`) and paste it into `backend/.env`, replacing the existing `SECRET_KEY` line.

Your `backend/.env` should look like this:
```bash
DEBUG=True
SECRET_KEY=your-generated-secret-key-here-CHANGE-THIS
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://birthdays_user:birthdays_password@db:5432/birthdays_db
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## Step 4: Start All Services

```bash
docker-compose up -d
```

This will:
- ✅ Pull and start PostgreSQL database
- ✅ Build and start Django backend
- ✅ Build and start React frontend
- ✅ Set up networking between services

**First time?** This may take 2-5 minutes to download images and build.

---

## Step 5: Run Database Migrations

```bash
# Run migrations to create database tables
docker-compose exec backend python manage.py migrate
```

You should see output like:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying users.0001_initial... OK
  Applying birthdays.0001_initial... OK
  ...
```

---

## Step 6: Create Admin User

```bash
docker-compose exec backend python manage.py createsuperuser
```

Follow the prompts:
```
Email: admin@example.com
Username: admin
Password: ********
Password (again): ********
```

---

## Step 7: Access the Application

🎉 **You're ready!**

Open your browser and visit:

- **Frontend (React App)**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation (Swagger)**: http://localhost:8000/api/docs/
- **API Documentation (ReDoc)**: http://localhost:8000/api/redoc/

---

## 🧪 Test It Out

### 1. Create Your First Account

1. Go to http://localhost:5173
2. Click **"Sign up"**
3. Fill in the registration form
4. You'll be automatically logged in

### 2. Add Your First Contact

1. Click **"Contacts"** in the navigation
2. Click **"Add Contact"** button
3. Enter contact details with a birthday
4. Save!

### 3. Check the Dashboard

1. Go back to **"Dashboard"**
2. See your contact in the upcoming birthdays list

---

## 📋 Useful Commands

### View Logs

```bash
# View all logs
docker-compose logs -f

# View only backend logs
docker-compose logs -f backend

# View only frontend logs
docker-compose logs -f frontend

# View only database logs
docker-compose logs -f db
```

### Stop Everything

```bash
docker-compose down
```

### Stop and Remove All Data (Fresh Start)

```bash
docker-compose down -v
# This removes the database volume, so you'll start fresh
```

### Restart Services

```bash
# Restart everything
docker-compose restart

# Restart only backend
docker-compose restart backend

# Restart only frontend
docker-compose restart frontend
```

### Access Django Shell

```bash
docker-compose exec backend python manage.py shell
```

### Run Backend Tests

```bash
docker-compose exec backend pytest
```

### Access Database

```bash
docker-compose exec db psql -U birthdays_user -d birthdays_db
```

---

## 🔧 Troubleshooting

### Port Already in Use

**Error:** `Bind for 0.0.0.0:5173 failed: port is already allocated`

**Solution:** Another service is using the port. Either:

1. Stop the conflicting service
2. Or change the port in `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "5174:5173"  # Change 5173 to 5174
```

### Database Connection Error

**Error:** `connection to server at "db" (XXX.XXX.XXX.XXX), port 5432 failed`

**Solution:** Database might not be ready yet. Wait 10-15 seconds and try again:

```bash
docker-compose restart backend
```

### Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'django'`

**Solution:** Rebuild the backend container:

```bash
docker-compose build backend
docker-compose up -d backend
```

### Frontend Shows Blank Page

**Error:** White screen or "Cannot connect to API"

**Solution 1:** Check if backend is running:
```bash
curl http://localhost:8000/api/v1/birthdays/contacts/
# Should return: {"detail":"Authentication credentials were not provided."}
```

**Solution 2:** Check frontend environment:
```bash
# Ensure frontend/.env has:
VITE_API_URL=http://localhost:8000
```

### Permission Denied Errors

**Error:** `Permission denied` when running Docker commands

**Solution:** Add `sudo` before commands (Linux/Mac):
```bash
sudo docker-compose up -d
```

Or add your user to the docker group:
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### Can't Access http://localhost:5173

**Solution:**

1. Check if container is running:
```bash
docker-compose ps
```

2. Check frontend logs:
```bash
docker-compose logs frontend
```

3. Try rebuilding:
```bash
docker-compose build frontend
docker-compose up -d frontend
```

---

## 🛠️ Development Workflow

### Making Backend Changes

1. Edit files in `backend/`
2. Changes are automatically detected (hot reload)
3. If you add new dependencies to `requirements.txt`:
   ```bash
   docker-compose build backend
   docker-compose restart backend
   ```

### Making Frontend Changes

1. Edit files in `frontend/src/`
2. Changes are automatically reflected (Vite hot reload)
3. If you add new npm packages:
   ```bash
   docker-compose exec frontend npm install package-name
   # Or rebuild:
   docker-compose build frontend
   docker-compose restart frontend
   ```

### Creating New Database Migrations

```bash
# After changing models in backend/birthdays/models.py
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

---

## 📊 Sample Data

Want some test data to play with?

### Create Sample Contacts via Django Shell

```bash
docker-compose exec backend python manage.py shell
```

Then paste this:

```python
from django.contrib.auth import get_user_model
from birthdays.models import Contact, Event
from datetime import datetime, timedelta

# Get your user (replace with your email)
User = get_user_model()
user = User.objects.get(email='admin@example.com')

# Create some sample contacts
contacts = [
    {"name": "Alice Johnson", "birthday": datetime(1990, 1, 15).date(), "email": "alice@example.com"},
    {"name": "Bob Smith", "birthday": datetime(1985, 3, 22).date(), "email": "bob@example.com"},
    {"name": "Carol Davis", "birthday": datetime(1992, 6, 8).date(), "email": "carol@example.com"},
    {"name": "David Wilson", "birthday": datetime(1988, 9, 14).date(), "email": "david@example.com"},
    {"name": "Eve Martinez", "birthday": datetime(1995, 12, 3).date(), "email": "eve@example.com"},
]

for contact_data in contacts:
    Contact.objects.create(owner=user, **contact_data)

print(f"Created {len(contacts)} sample contacts!")

# Create some sample events
today = datetime.now().date()
next_week = today + timedelta(days=7)
next_month = today + timedelta(days=30)

events = [
    {"name": "Wedding Anniversary", "type": "anniversary", "date": next_week, "recurs_annually": True},
    {"name": "Company Holiday Party", "type": "holiday", "date": next_month, "recurs_annually": False},
]

for event_data in events:
    Event.objects.create(owner=user, **event_data)

print(f"Created {len(events)} sample events!")
exit()
```

---

## 🎯 What's Next?

Now that you have it running locally:

1. **Explore the API**: Visit http://localhost:8000/api/docs/
2. **Check the Admin Panel**: http://localhost:8000/admin
3. **Review the Code**: Look through `backend/` and `frontend/src/`
4. **Read the Documentation**: Check out `README.md` and `MIGRATION_GUIDE.md`
5. **Plan Deployment**: See deployment options in `MIGRATION_GUIDE.md`

---

## 🆘 Need Help?

- **Documentation**: Check `README.md`, `MIGRATION_GUIDE.md`, `TECH_STACK_AUDIT.md`
- **API Docs**: http://localhost:8000/api/docs/
- **Logs**: `docker-compose logs -f`
- **Issues**: Open an issue on GitHub

---

## 🎉 You're All Set!

You now have a fully functional modern birthday reminder application running locally.

**Happy Coding!** 🚀

---

*Generated with [Claude Code](https://claude.com/claude-code)*
