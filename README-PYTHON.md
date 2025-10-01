# 🚀 NUANU WiFi Login Portal (Python FastAPI)

Complete WiFi hotspot login system with user data collection and admin dashboard for MikroTik routers.

## ✨ Features

- **Modern Login Portal**: Beautiful, responsive login page
- **Data Collection**: Captures email, questions, and user role
- **Admin Dashboard**: Real-time statistics and user management  
- **Python FastAPI Backend**: Fast, modern, async Python framework
- **PostgreSQL Database**: Secure data storage on DigitalOcean
- **MikroTik Integration**: Seamless hotspot authentication
- **Export Functionality**: CSV, XLSX, PDF export options

## 📋 Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL (DigitalOcean)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Deployment**: Railway
- **Router**: MikroTik with Hotspot

## 🛠️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/WELCOME-TO-NUANU-NEW.git
cd WELCOME-TO-NUANU-NEW
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
DB_USER=doadmin
DB_PASSWORD=your_database_password_here
DB_HOST=welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com
DB_PORT=25060
DB_NAME=welcome-to-nuanu-new
DASHBOARD_PASSWORD=Bali0361
```

### 5. Run Locally

```bash
# Using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or using the batch file (Windows)
start.bat
```

Visit:
- **Login**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin

## 🗄️ Database Schema

### Table: `wifi_users`

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| email | VARCHAR(255) | User email |
| questions | TEXT | User questions/feedback |
| role | VARCHAR(100) | User role (Solopreneur, etc.) |
| ip_address | VARCHAR(50) | User IP address |
| created_at | TIMESTAMP | Registration timestamp |

## 🔌 API Endpoints

### POST `/api/save-user`
Save user registration data

**Request:**
```json
{
  "email": "user@example.com",
  "questions": "Optional question",
  "role": "Solopreneur"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User data saved successfully",
  "data": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### GET `/api/users`
Get all users (for admin dashboard)

**Response:**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "questions": "Question text",
      "role": "Solopreneur",
      "ip_address": "192.168.1.100",
      "created_at": "2025-10-01T12:00:00"
    }
  ]
}
```

### GET `/api/stats`
Get user statistics

**Response:**
```json
{
  "success": true,
  "stats": {
    "total": 100,
    "last24hours": 15,
    "byRole": [
      {"role": "Solopreneur", "count": 30},
      {"role": "Student", "count": 25}
    ]
  }
}
```

### DELETE `/api/users/{user_id}`
Delete a user

**Response:**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

## 🚂 Deploy to Railway

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial commit: Python FastAPI WiFi portal"
git push origin main
```

### 2. Deploy on Railway

1. Go to [Railway.app](https://railway.app)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-detects Python and uses `requirements.txt`

### 3. Add Environment Variables

In Railway dashboard → **Variables**:

```
DB_USER=doadmin
DB_PASSWORD=your_database_password_here
DB_HOST=welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com
DB_PORT=25060
DB_NAME=welcome-to-nuanu-new
DASHBOARD_PASSWORD=Bali0361
SECRET_KEY=your-secret-key-here
BASE_URL=https://your-app.railway.app
```

### 4. Generate Domain

Railway → **Settings** → **Networking** → **Generate Domain**

Your app will be at: `https://your-app-name.up.railway.app`

## 🔧 MikroTik Configuration

### Quick Setup

1. **Open Winbox** → Connect to `103.165.204.234`

2. **Add Walled Garden Rules**

Go to **IP → Hotspot → Walled Garden**:

```
dst-host: *.railway.app (allow)
dst-host: your-app-name.up.railway.app (allow)
dst-host: images.lifestyleasia.com (allow)
dst-host: nuanu.com (allow)
```

3. **Configure Server Profile**

**IP → Hotspot → Server Profiles** → Your profile:
- Login By: `HTTP CHAP`
- HTTP Cookie Lifetime: `1d`

4. **Create Hotspot User**

**IP → Hotspot → Users**:
- Name: `user`
- Password: `user`

5. **Upload Login Page** (Optional)

Copy `public/login.html` to MikroTik `/hotspot/` directory

See [MIKROTIK_SETUP.md](MIKROTIK_SETUP.md) for detailed instructions.

## 📊 Admin Dashboard

Access at: `https://your-app.railway.app/admin`

**Features:**
- View all registered users
- Real-time statistics
- Search and filter
- Export to CSV/XLSX/PDF
- Delete users
- Role distribution charts

**Default Password:** `Bali0361` (change in `.env`)

## 🧪 Testing

### Test Login Flow

1. Connect to WiFi hotspot
2. Browser redirects to login page
3. Fill form:
   - Email: test@example.com
   - Questions: Test question
   - Role: Select role
4. Click Submit
5. Redirects to nuanu.com
6. Check admin dashboard for data

### Test API Locally

```bash
# Save user
curl -X POST http://localhost:8000/api/save-user \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","questions":"Test","role":"Solopreneur"}'

# Get users
curl http://localhost:8000/api/users

# Get stats
curl http://localhost:8000/api/stats
```

## 📦 Project Structure

```
WELCOME-TO-NUANU-NEW/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway deployment config
├── railway.json              # Railway settings
├── .env.example              # Environment variables template
├── start.bat                 # Windows start script
├── public/
│   ├── login.html           # Login page
│   └── admin.html           # Admin dashboard
├── login-rev-check.html     # Original login (for reference)
├── README-PYTHON.md         # This file
├── DEPLOYMENT_GUIDE.md      # Detailed deployment guide
└── MIKROTIK_SETUP.md        # MikroTik configuration guide
```

## 🔐 Security

- ✅ Environment variables for sensitive data
- ✅ CORS configured
- ✅ SSL/TLS on Railway (automatic)
- ✅ PostgreSQL SSL connection
- ✅ Password-protected admin dashboard
- ✅ Input validation
- ⚠️ Change `DASHBOARD_PASSWORD` in production
- ⚠️ Change `SECRET_KEY` in production

## 🐛 Troubleshooting

### Database Connection Error

**Error:** `could not connect to server`

**Solution:**
1. Check `.env` credentials
2. Verify DigitalOcean database is running
3. Check firewall allows connections
4. Test connection:
   ```bash
   psql -h welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com \
        -U doadmin -d welcome-to-nuanu-new -p 25060
   ```

### Import Error: No module named 'fastapi'

**Solution:**
```bash
pip install -r requirements.txt
```

### Port Already in Use

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
uvicorn app:app --port 8001
```

### Railway Deployment Failed

**Solution:**
1. Check Railway logs
2. Verify `requirements.txt` is correct
3. Ensure `Procfile` exists
4. Check environment variables are set

### MikroTik Not Redirecting

**Solution:**
1. Verify Walled Garden rules
2. Check hotspot is running: `/ip hotspot print`
3. Test DNS: `/ping your-app.railway.app`
4. Add IP-based walled garden rule

## 📝 Development

### Add New API Endpoint

```python
# In app.py
@app.get("/api/my-endpoint")
async def my_endpoint(request: Request):
    return JSONResponse({"message": "Hello"})
```

### Modify Database Schema

```python
# In init_db() function
cur.execute("""
    ALTER TABLE wifi_users 
    ADD COLUMN new_field VARCHAR(100)
""")
```

### Add New Form Field

1. Update `public/login.html` HTML
2. Update JavaScript to capture field
3. Update `/api/save-user` endpoint in `app.py`
4. Update database schema

## 🔄 Updates & Maintenance

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

### Backup Database

```bash
pg_dump -h welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com \
        -U doadmin -d welcome-to-nuanu-new -p 25060 > backup.sql
```

### Monitor Logs

```bash
# Railway CLI
railway logs

# Or in Railway dashboard
```

## 📞 Support

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Railway Docs**: https://docs.railway.app
- **MikroTik Wiki**: https://wiki.mikrotik.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

## 📄 License

MIT License - Free to use for your projects

---

**Made with ❤️ for NUANU**

**Database Credentials:**
- Host: `welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com`
- Port: `25060`
- Database: `welcome-to-nuanu-new`
- User: `doadmin`
- Password: [Get from DigitalOcean dashboard]

**MikroTik IP:** `103.165.204.234`
