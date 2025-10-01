# 🚀 Complete Deployment Guide

## Step-by-Step Instructions for GitHub + Railway + MikroTik Setup

---

## Part 1: Prepare Your Code

### 1. Install Dependencies Locally (Test First)

```bash
cd d:\WELCOME-TO-NUANU-NEW
npm install
```

### 2. Test Locally

```bash
npm start
```

Open browser:
- Login: http://localhost:3000/
- Admin: http://localhost:3000/admin

Test the login form and verify database connection works.

---

## Part 2: Push to GitHub

### 1. Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: WiFi login portal with admin dashboard"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `WELCOME-TO-NUANU-NEW`
3. Make it **Private** (recommended for security)
4. Don't initialize with README (you already have one)
5. Click "Create repository"

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/WELCOME-TO-NUANU-NEW.git
git branch -M main
git push -u origin main
```

---

## Part 3: Deploy to Railway

### 1. Sign Up / Login to Railway

1. Go to https://railway.app
2. Sign in with GitHub
3. Authorize Railway to access your repositories

### 2. Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **"WELCOME-TO-NUANU-NEW"**
### 3. Add Environment Variables

1. Click on your deployed service
2. Go to **"Variables"** tab
3. Add environment variables in Railway dashboard:
   - `DB_USER` (your database user)
   - `DB_PASSWORD` (your database password)
   - `DB_HOST` (your database host)
   - `DB_PORT` (25060)
   - `DB_NAME` (your database name)
   - `NODE_ENV` (production)
4. Click **"Deploy"** to redeploy with new variables

### 4. Get Your Public URL

1. Go to **"Settings"** tab
2. Scroll to **"Networking"**
3. Click **"Generate Domain"**
4. Copy your URL (e.g., `https://welcome-to-nuanu-new-production.up.railway.app`)

### 5. Test Your Deployment

Visit your URLs:
- Login: `https://your-app.railway.app/`
- Admin: `https://your-app.railway.app/admin`

---

## Part 4: Configure MikroTik Router

### Prerequisites
- MikroTik Winbox installed
- Router IP: **103.165.204.234**
- Admin credentials for MikroTik

### Method A: External Hosted Login (Recommended)

This method uses your Railway-hosted login page.

#### Step 1: Configure Walled Garden

1. Open **Winbox** → Connect to **103.165.204.234**
2. Go to **IP → Hotspot → Walled Garden**
3. Click **"+"** to add new rules:

```
Rule 1:
- Dst. Host: your-app.railway.app
- Action: allow

Rule 2:
- Dst. Host: *.railway.app
- Action: allow

Rule 3:
- Dst. Host: images.lifestyleasia.com
- Action: allow

Rule 4:
- Dst. Host: nuanu.com
- Action: allow

Rule 5:
- Dst. Host: *.nuanu.com
- Action: allow
```

#### Step 2: Configure Hotspot Server Profile

1. Go to **IP → Hotspot → Server Profiles**
2. Double-click your profile (usually "hsprof1")
3. **Login** tab:
   - Login By: `HTTP CHAP`
   - HTTP Cookie Lifetime: `1d`
4. **RADIUS** tab (if using RADIUS, skip if not):
   - Leave as default or configure as needed

#### Step 3: Set Custom Login URL

1. Still in **Server Profiles** → **Login** tab
2. **HTML Directory**: `hotspot`
3. **Login Page**: Leave blank or set to your Railway URL

**OR** use Terminal:

```
/ip hotspot profile
set [find name="hsprof1"] html-directory=hotspot login-by=http-chap
```

#### Step 4: Create Hotspot User

1. Go to **IP → Hotspot → Users**
2. Click **"+"** to add user:
   - Name: `user`
   - Password: `user`
   - Profile: `default` (or your profile)
3. Click **OK**

#### Step 5: Redirect to External Login

**Option A: Using Walled Garden IP**

1. Go to **IP → Hotspot → Walled Garden IP List**
2. Add your Railway app's IP address

**Option B: Modify Login Page**

Upload a simple redirect HTML to MikroTik:

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url=https://your-app.railway.app/">
</head>
<body>
    <p>Redirecting to login...</p>
</body>
</html>
```

1. Save as `login.html`
2. In Winbox, go to **Files**
3. Drag and drop `login.html` to `/hotspot/` directory

### Method B: Upload Login Page to MikroTik (Alternative)

This method hosts the login page directly on MikroTik.

#### Step 1: Prepare Login Page for MikroTik

1. Copy `public/login.html` 
2. Edit line 213 to use your Railway API:

```javascript
const API_BASE = "https://your-app.railway.app";
```

3. Save the file

#### Step 2: Upload to MikroTik

1. Open **Winbox** → **Files**
2. Navigate to `/hotspot/` folder
3. Upload modified `login.html`
4. Rename to `login.html` (overwrite existing)

#### Step 3: Configure Walled Garden for API Access

Add Walled Garden rules (same as Method A, Step 1)

---

## Part 5: Testing the Complete System

### 1. Test WiFi Connection

1. Connect to your WiFi hotspot
2. Open browser (should auto-redirect to login)
3. Fill in the form:
   - Email: test@example.com
   - Questions: Test question
   - Role: Select any role
4. Click **Submit**
5. Should redirect to nuanu.com

### 2. Verify Data in Admin Dashboard

1. Go to `https://your-app.railway.app/admin`
2. Check if test user appears
3. Verify all data is captured correctly

### 3. Test from Mobile Device

1. Connect phone to WiFi
2. Open browser
3. Complete login process
4. Verify mobile responsiveness

---

## Part 6: MikroTik Advanced Configuration

### Monitor Active Users

```
/ip hotspot active print
```

### View Hotspot Logs

```
/log print where topics~"hotspot"
```

### Set User Limits

```
/ip hotspot user
set [find name="user"] limit-uptime=1d limit-bytes-total=1G
```

### Create Multiple User Profiles

```
/ip hotspot user profile
add name="premium" rate-limit="10M/10M" shared-users=3
add name="basic" rate-limit="2M/2M" shared-users=1
```

### Customize Session Timeout

```
/ip hotspot profile
set [find name="hsprof1"] session-timeout=1d idle-timeout=5m
```

---

## Part 7: Security Best Practices

### 1. Secure Admin Dashboard

Add basic authentication to `server.js`:

```javascript
// Add before admin route
const adminAuth = (req, res, next) => {
  const auth = req.headers.authorization;
  if (auth === 'Basic ' + Buffer.from('admin:your-password').toString('base64')) {
    next();
  } else {
    res.setHeader('WWW-Authenticate', 'Basic realm="Admin Area"');
    res.status(401).send('Authentication required');
  }
};

app.get('/admin', adminAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'admin.html'));
});
```

### 2. Enable HTTPS on MikroTik

```
/ip hotspot profile
set [find name="hsprof1"] use-radius=yes
```

### 3. Backup Database Regularly

In Railway dashboard:
1. Go to your PostgreSQL database
2. Enable automated backups
3. Download manual backup: `pg_dump` command

### 4. Monitor Railway Logs

```bash
railway logs
```

Or in Railway dashboard → **Deployments** → **View Logs**

---

## Part 8: Troubleshooting

### Issue: Users Can't Access Login Page

**Solution:**
1. Check Walled Garden rules include your Railway domain
2. Verify DNS is working: `ping your-app.railway.app`
3. Check MikroTik firewall rules

### Issue: Data Not Saving to Database

**Solution:**
1. Check Railway logs for errors
2. Verify environment variables are correct
3. Test database connection:
   ```bash
   psql -h welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com -U doadmin -d welcome-to-nuanu-new -p 25060
   ```

### Issue: Login Redirects Not Working

**Solution:**
1. Check MikroTik hotspot user exists
2. Verify `$(link-login-only)` variable in login.html
3. Test manual login:
   ```
   http://103.165.204.234/login?username=user&password=user
   ```

### Issue: Admin Dashboard Not Loading

**Solution:**
1. Check Railway deployment status
2. Verify `/admin` route in server.js
3. Check browser console for errors

### Issue: CORS Errors

**Solution:**
Already handled in `server.js` with `cors()` middleware. If issues persist:

```javascript
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'DELETE'],
  credentials: true
}));
```

---

## Part 9: Maintenance

### Update Code

```bash
# Make changes locally
git add .
git commit -m "Description of changes"
git push origin main
```

Railway will auto-deploy on push.

### Database Maintenance

```sql
-- View table size
SELECT pg_size_pretty(pg_total_relation_size('wifi_users'));

-- Clean old records (older than 90 days)
DELETE FROM wifi_users WHERE created_at < NOW() - INTERVAL '90 days';

-- Vacuum database
VACUUM ANALYZE wifi_users;
```

### Monitor Performance

Railway dashboard shows:
- CPU usage
- Memory usage
- Request count
- Response times

---

## Part 10: Scaling

### Increase Railway Resources

1. Go to Railway dashboard
2. Click your service → **Settings**
3. Upgrade plan if needed

### Add Redis Caching (Optional)

```bash
npm install redis
```

Update `server.js` to cache frequent queries.

### Load Balancing (Advanced)

Deploy multiple instances on Railway and use Railway's built-in load balancing.

---

## 📞 Support Contacts

- **Railway Support**: https://railway.app/help
- **DigitalOcean Support**: https://www.digitalocean.com/support
- **MikroTik Forum**: https://forum.mikrotik.com

---

## ✅ Deployment Checklist

- [ ] Code tested locally
- [ ] Pushed to GitHub
- [ ] Deployed to Railway
- [ ] Environment variables configured
- [ ] Database connection verified
- [ ] Railway domain generated
- [ ] MikroTik Walled Garden configured
- [ ] Hotspot user created
- [ ] Login page accessible
- [ ] Admin dashboard accessible
- [ ] Test user registration
- [ ] Verify data in database
- [ ] Test from mobile device
- [ ] Monitor logs for errors

---

**Congratulations! Your NUANU WiFi Login Portal is now live! 🎉**
