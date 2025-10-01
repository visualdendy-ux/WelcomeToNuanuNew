# ⚡ Quick Start Guide

Get your NUANU WiFi Login Portal running in 5 minutes!

## 🎯 Prerequisites

- Python 3.11+ installed
- Git installed
- Railway account (free)
- GitHub account

## 🚀 Local Setup (2 minutes)

### Step 1: Install Dependencies

```bash
cd d:\WELCOME-TO-NUANU-NEW
pip install -r requirements.txt
```

### Step 2: Run Server

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Test

Open browser:
- Login: http://localhost:8000/
- Admin: http://localhost:8000/admin (password: `Bali0361`)

## ☁️ Deploy to Railway (3 minutes)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `WELCOME-TO-NUANU-NEW`
4. Wait for deployment (auto-detects Python)

### Step 3: Add Environment Variables

In Railway dashboard → Variables → Add:

```
DB_USER=doadmin
DB_PASSWORD=your_database_password_here
DB_HOST=welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com
DB_PORT=25060
DB_NAME=welcome-to-nuanu-new
DASHBOARD_PASSWORD=Bali0361
```

### Step 4: Get Your URL

Railway → Settings → Networking → Generate Domain

Copy your URL: `https://your-app.railway.app`

## 🔧 MikroTik Setup (5 minutes)

### Step 1: Connect to MikroTik

- Open Winbox
- Connect to: `103.165.204.234`
- Login with admin credentials

### Step 2: Add Walled Garden

Go to **IP → Hotspot → Walled Garden** → Add:

```
dst-host: *.railway.app (action: allow)
dst-host: your-app.railway.app (action: allow)
dst-host: images.lifestyleasia.com (action: allow)
dst-host: nuanu.com (action: allow)
```

### Step 3: Create Hotspot User

Go to **IP → Hotspot → Users** → Add:

```
Name: user
Password: user
```

### Step 4: Configure Profile

Go to **IP → Hotspot → Server Profiles** → Your profile:

```
Login By: HTTP CHAP
HTTP Cookie Lifetime: 1d
```

## ✅ Test Complete Flow

1. Connect phone to WiFi
2. Browser opens → redirects to your Railway URL
3. Fill form:
   - Email: test@example.com
   - Questions: Test
   - Role: Solopreneur
4. Click Submit
5. Redirects to nuanu.com
6. Check admin dashboard: `https://your-app.railway.app/admin`
7. See test user in dashboard

## 🎉 Done!

Your WiFi login portal is now live!

## 📚 Next Steps

- Read [README-PYTHON.md](README-PYTHON.md) for full documentation
- See [MIKROTIK_SETUP.md](MIKROTIK_SETUP.md) for advanced MikroTik config
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment

## 🆘 Quick Troubleshooting

### Can't connect to database?

Check your `.env` file has correct credentials.

### Railway deployment failed?

1. Check Railway logs
2. Verify `requirements.txt` exists
3. Ensure all environment variables are set

### MikroTik not redirecting?

1. Check Walled Garden rules
2. Verify hotspot is running: `/ip hotspot print`
3. Test: `/ping your-app.railway.app`

### Admin dashboard not loading?

Password is: `Bali0361` (default)

## 📞 Need Help?

- Check full docs: [README-PYTHON.md](README-PYTHON.md)
- MikroTik guide: [MIKROTIK_SETUP.md](MIKROTIK_SETUP.md)
- Open GitHub issue

---

**Your Credentials:**

**Database:**
- Host: welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com
- Port: 25060
- Database: welcome-to-nuanu-new
- User: doadmin
- Password: [Get from DigitalOcean dashboard]

**MikroTik:**
- IP: 103.165.204.234
- Hotspot User: user / user

**Admin Dashboard:**
- Password: Bali0361
