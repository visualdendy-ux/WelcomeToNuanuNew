# ✅ Deployment Checklist

Use this checklist to ensure everything is properly configured before going live.

---

## 📋 Pre-Deployment Checklist

### Local Testing

- [ ] Python 3.11+ installed
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created with correct credentials
- [ ] Server runs locally: `uvicorn app:app --reload --port 8000`
- [ ] Login page loads: http://localhost:8000/
- [ ] Admin dashboard loads: http://localhost:8000/admin
- [ ] Test form submission works
- [ ] Data appears in admin dashboard
- [ ] Database connection successful
- [ ] No errors in console

### Code Review

- [ ] `app.py` has correct database credentials
- [ ] `public/login.html` exists
- [ ] `public/admin.html` exists
- [ ] `requirements.txt` is complete
- [ ] `Procfile` configured for Python
- [ ] `railway.json` configured correctly
- [ ] `.env.example` has all variables
- [ ] `.gitignore` includes `.env` and sensitive files

### Database

- [ ] PostgreSQL database accessible
- [ ] Database credentials correct:
  - Host: `welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com`
  - Port: `25060`
  - Database: `welcome-to-nuanu-new`
  - User: `doadmin`
  - Password: [Get from DigitalOcean dashboard]
- [ ] SSL connection enabled
- [ ] Table `wifi_users` will be created automatically on first run

---

## 🚀 Railway Deployment Checklist

### GitHub Setup

- [ ] Code pushed to GitHub
- [ ] Repository is accessible
- [ ] All files committed
- [ ] `.env` NOT committed (should be in .gitignore)

### Railway Configuration

- [ ] Railway account created
- [ ] New project created from GitHub repo
- [ ] Repository connected
- [ ] Python runtime detected
- [ ] Build successful

### Environment Variables

Add these in Railway dashboard → Variables:

- [ ] `DB_USER` = `doadmin`
- [ ] `DB_PASSWORD` = [Your database password from DigitalOcean]
- [ ] `DB_HOST` = `welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com`
- [ ] `DB_PORT` = `25060`
- [ ] `DB_NAME` = `welcome-to-nuanu-new`
- [ ] `DASHBOARD_PASSWORD` = `Bali0361` (or your custom password)
- [ ] `SECRET_KEY` = (generate a random secret key)
- [ ] `BASE_URL` = (your Railway URL, e.g., https://your-app.railway.app)

### Deployment

- [ ] Deployment successful
- [ ] No build errors
- [ ] Logs show "Application startup complete"
- [ ] Domain generated
- [ ] HTTPS enabled (automatic)

### Testing Deployed App

- [ ] Login page loads: `https://your-app.railway.app/`
- [ ] Admin dashboard loads: `https://your-app.railway.app/admin`
- [ ] Can login to admin with password
- [ ] Test form submission
- [ ] Data saves to database
- [ ] Data appears in admin dashboard
- [ ] Statistics display correctly
- [ ] Export CSV works
- [ ] Delete user works

---

## 🔧 MikroTik Configuration Checklist

### Connection

- [ ] Winbox installed
- [ ] Connected to MikroTik: `103.165.204.234`
- [ ] Admin access confirmed
- [ ] Hotspot service running

### Walled Garden Configuration

Add these rules in **IP → Hotspot → Walled Garden**:

- [ ] `dst-host: *.railway.app` (action: allow)
- [ ] `dst-host: your-app-name.up.railway.app` (action: allow)
- [ ] `dst-host: images.lifestyleasia.com` (action: allow)
- [ ] `dst-host: nuanu.com` (action: allow)
- [ ] `dst-host: *.nuanu.com` (action: allow)

### Walled Garden IP (Optional but Recommended)

- [ ] Found Railway app IP: `nslookup your-app.railway.app`
- [ ] Added IP to Walled Garden IP list

### Hotspot Profile

**IP → Hotspot → Server Profiles** → Your profile:

- [ ] Login By: `HTTP CHAP` enabled
- [ ] HTTP Cookie Lifetime: `1d`
- [ ] HTML Directory: `hotspot`

### Hotspot User

**IP → Hotspot → Users**:

- [ ] User created: `user` / `user`
- [ ] Profile: `default` (or your profile)
- [ ] User is active

### DNS Configuration

- [ ] DNS servers configured: `8.8.8.8`, `8.8.4.4`
- [ ] Allow remote requests: enabled
- [ ] DNS resolution working: `/ping your-app.railway.app`

### Firewall Rules

- [ ] HTTP (port 80) allowed
- [ ] HTTPS (port 443) allowed
- [ ] DNS (port 53) allowed
- [ ] NAT configured for hotspot

---

## 🧪 End-to-End Testing Checklist

### Test from Mobile Device

- [ ] Connect to WiFi hotspot
- [ ] Browser automatically opens
- [ ] Redirects to Railway login page
- [ ] Login page displays correctly
- [ ] All form fields visible
- [ ] Can type in email field
- [ ] Can type in questions field
- [ ] Can select role from dropdown

### Test Form Submission

- [ ] Fill in email: `test@example.com`
- [ ] Fill in questions: `Test question`
- [ ] Select role: `Solopreneur`
- [ ] Click Submit button
- [ ] Button shows "Saving your information..."
- [ ] Success message appears
- [ ] Redirects to nuanu.com
- [ ] Internet access granted

### Verify Data Collection

- [ ] Open admin dashboard: `https://your-app.railway.app/admin`
- [ ] Enter password: `Bali0361`
- [ ] Dashboard loads successfully
- [ ] Test user appears in table
- [ ] Email is correct
- [ ] Questions are correct
- [ ] Role is correct
- [ ] IP address is captured
- [ ] Timestamp is correct

### Test Admin Features

- [ ] Total users count is correct
- [ ] Last 24 hours count updates
- [ ] Role statistics display
- [ ] Role distribution chart shows
- [ ] Search functionality works
- [ ] Can filter by email
- [ ] Can filter by role
- [ ] Export CSV downloads
- [ ] CSV contains correct data
- [ ] Delete user works
- [ ] User removed from list

### Test Multiple Users

- [ ] Submit form with different emails
- [ ] Submit form with different roles
- [ ] All users appear in dashboard
- [ ] Statistics update correctly
- [ ] Role distribution updates

---

## 🔐 Security Checklist

### Credentials

- [ ] `.env` file NOT in Git
- [ ] Database password secure
- [ ] Dashboard password changed from default
- [ ] SECRET_KEY is random and secure
- [ ] No credentials in code comments
- [ ] No credentials in logs

### Access Control

- [ ] Admin dashboard password protected
- [ ] Only authorized users have MikroTik access
- [ ] Railway account secured with 2FA
- [ ] GitHub repository private (recommended)
- [ ] Database firewall configured

### SSL/TLS

- [ ] Railway app uses HTTPS
- [ ] Database connection uses SSL
- [ ] No mixed content warnings
- [ ] Certificate valid

---

## 📊 Monitoring Checklist

### Railway Monitoring

- [ ] Check deployment logs: `railway logs`
- [ ] Monitor CPU usage
- [ ] Monitor memory usage
- [ ] Check for errors in logs
- [ ] Set up alerts (optional)

### Database Monitoring

- [ ] Check database size
- [ ] Monitor connection count
- [ ] Check for slow queries
- [ ] Verify backups enabled

### MikroTik Monitoring

- [ ] Check active hotspot users: `/ip hotspot active print`
- [ ] Monitor bandwidth usage
- [ ] Check logs: `/log print where topics~"hotspot"`
- [ ] Verify no authentication errors

---

## 🐛 Troubleshooting Checklist

### If Login Page Doesn't Load

- [ ] Check Railway deployment status
- [ ] Verify domain is generated
- [ ] Check Railway logs for errors
- [ ] Test URL directly in browser
- [ ] Check DNS resolution

### If Data Doesn't Save

- [ ] Check Railway logs for database errors
- [ ] Verify database credentials
- [ ] Test database connection
- [ ] Check network connectivity
- [ ] Verify table exists

### If MikroTik Doesn't Redirect

- [ ] Verify Walled Garden rules
- [ ] Check hotspot is running
- [ ] Test DNS resolution on MikroTik
- [ ] Check firewall rules
- [ ] Verify hotspot user exists

### If Admin Dashboard Doesn't Load

- [ ] Check password is correct
- [ ] Verify `/admin` route works
- [ ] Check browser console for errors
- [ ] Test API endpoints directly
- [ ] Check Railway logs

---

## 📝 Post-Deployment Tasks

### Documentation

- [ ] Document Railway URL
- [ ] Save admin password securely
- [ ] Document any custom configurations
- [ ] Create backup of configuration
- [ ] Share access with team (if applicable)

### Backup

- [ ] Backup database
- [ ] Export initial data
- [ ] Save MikroTik configuration
- [ ] Backup Railway environment variables

### Monitoring Setup

- [ ] Set up uptime monitoring (optional)
- [ ] Configure error alerts (optional)
- [ ] Set up database backup schedule
- [ ] Document maintenance procedures

---

## ✅ Final Verification

### Complete Flow Test

1. [ ] User connects to WiFi
2. [ ] Browser opens automatically
3. [ ] Redirects to login page
4. [ ] User fills form
5. [ ] Data saves to database
6. [ ] User gets internet access
7. [ ] Data visible in admin dashboard
8. [ ] All statistics correct

### Performance Test

- [ ] Page loads in < 3 seconds
- [ ] Form submission in < 2 seconds
- [ ] Admin dashboard loads in < 3 seconds
- [ ] No timeout errors
- [ ] Handles multiple concurrent users

### User Experience Test

- [ ] Mobile responsive
- [ ] Desktop responsive
- [ ] Tablet responsive
- [ ] All buttons work
- [ ] All links work
- [ ] No broken images
- [ ] Professional appearance

---

## 🎉 Go Live!

Once all items are checked:

- [ ] **FINAL TEST**: Complete end-to-end flow
- [ ] **BACKUP**: Save all configurations
- [ ] **MONITOR**: Watch logs for first hour
- [ ] **DOCUMENT**: Note Railway URL and credentials
- [ ] **CELEBRATE**: Your WiFi portal is live! 🚀

---

## 📞 Emergency Contacts

**If something goes wrong:**

1. Check Railway logs: `railway logs`
2. Check MikroTik logs: `/log print`
3. Test database connection
4. Review this checklist
5. Check documentation files

**Support Resources:**
- [README-PYTHON.md](README-PYTHON.md)
- [QUICK_START.md](QUICK_START.md)
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [MIKROTIK_SETUP.md](MIKROTIK_SETUP.md)

---

**Deployment Date:** _____________

**Deployed By:** _____________

**Railway URL:** _____________

**Notes:** _____________
