# 🚀 Deploy to DigitalOcean Droplet

## Your Droplet Information
- **Name:** welcome-to-nuanu-new
- **IP Address:** 167.71.206.110
- **Database:** Already configured (DigitalOcean Managed PostgreSQL)

---

## 📋 Quick Deployment (Automated)

### Option 1: Automatic Deployment (Recommended)

I'll deploy everything for you automatically! Just provide:
1. Your DigitalOcean Droplet SSH password or SSH key

### Option 2: Manual Deployment

Follow these steps:

---

## 🔧 Step-by-Step Manual Deployment

### 1. Connect to Your Droplet

```bash
ssh root@167.71.206.110
```

### 2. Upload Your Code

From your local machine (Windows):

```powershell
# Using SCP to copy files
scp -r d:\WELCOME-TO-NUANU-NEW root@167.71.206.110:/tmp/
```

### 3. Run Deployment Script

On the droplet:

```bash
cd /tmp/WELCOME-TO-NUANU-NEW
chmod +x deploy.sh
sudo ./deploy.sh
```

### 4. Configure Database Password

```bash
sudo nano /var/www/nuanu-wifi-portal/.env
```

Change this line:
```
DB_PASSWORD=YOUR_DB_PASSWORD_HERE
```

To your actual password, then save (Ctrl+X, Y, Enter)

### 5. Restart Application

```bash
sudo supervisorctl restart nuanu-wifi-portal
```

### 6. Test Your App

Visit: **http://167.71.206.110**

---

## 🎯 What Gets Installed

- ✅ Python 3.11
- ✅ Nginx (web server)
- ✅ Supervisor (keeps app running)
- ✅ Your FastAPI application
- ✅ All dependencies from requirements.txt

---

## 🔍 Useful Commands

### Check App Status
```bash
sudo supervisorctl status nuanu-wifi-portal
```

### View Logs
```bash
# Application logs
sudo tail -f /var/log/nuanu-wifi-portal.out.log

# Error logs
sudo tail -f /var/log/nuanu-wifi-portal.err.log

# Nginx logs
sudo tail -f /var/nginx/access.log
```

### Restart App
```bash
sudo supervisorctl restart nuanu-wifi-portal
```

### Restart Nginx
```bash
sudo systemctl restart nginx
```

### Update Code
```bash
cd /var/www/nuanu-wifi-portal
git pull origin main  # if using git
sudo supervisorctl restart nuanu-wifi-portal
```

---

## 🌐 Configure MikroTik

Update your MikroTik Walled Garden with your droplet IP:

```
# In MikroTik Winbox: IP → Hotspot → Walled Garden
dst-host: 167.71.206.110 (action: allow)
dst-host: images.lifestyleasia.com (action: allow)
dst-host: nuanu.com (action: allow)
```

Update login page redirect in `public/login.html`:
- Change API_BASE to: `http://167.71.206.110`

---

## 🔐 Optional: Add SSL Certificate (HTTPS)

### Using Let's Encrypt (FREE)

1. **Get a domain name** (point it to 167.71.206.110)

2. **Install Certbot:**
```bash
sudo apt install certbot python3-certbot-nginx -y
```

3. **Get SSL certificate:**
```bash
sudo certbot --nginx -d yourdomain.com
```

4. **Update .env file:**
```bash
sudo nano /var/www/nuanu-wifi-portal/.env
# Change BASE_URL to: https://yourdomain.com
```

5. **Restart app:**
```bash
sudo supervisorctl restart nuanu-wifi-portal
```

---

## 🐛 Troubleshooting

### App not starting?
```bash
# Check logs
sudo tail -f /var/log/nuanu-wifi-portal.err.log

# Check if port 8000 is in use
sudo netstat -tulpn | grep 8000

# Restart supervisor
sudo systemctl restart supervisor
```

### Database connection error?
```bash
# Test database connection
psql -h welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com \
     -U doadmin -d welcome-to-nuanu-new -p 25060

# Check .env file has correct password
sudo cat /var/www/nuanu-wifi-portal/.env
```

### Nginx error?
```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Can't access from browser?
```bash
# Check firewall
sudo ufw status

# Allow HTTP
sudo ufw allow 80/tcp

# Check if app is running
sudo supervisorctl status
```

---

## 📊 Your URLs

- **Login Page:** http://167.71.206.110/
- **Admin Dashboard:** http://167.71.206.110/admin
- **API Docs:** http://167.71.206.110/docs

---

## 🔄 Auto-Update Setup (Optional)

Create a webhook to auto-deploy on git push:

```bash
# Install webhook
sudo apt install webhook -y

# Create webhook script
sudo nano /var/www/update-app.sh
```

Add:
```bash
#!/bin/bash
cd /var/www/nuanu-wifi-portal
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart nuanu-wifi-portal
```

Make executable:
```bash
sudo chmod +x /var/www/update-app.sh
```

---

## ✅ Deployment Checklist

- [ ] Connected to droplet via SSH
- [ ] Uploaded code to droplet
- [ ] Ran deploy.sh script
- [ ] Updated .env with DB_PASSWORD
- [ ] Restarted application
- [ ] Tested login page (http://167.71.206.110)
- [ ] Tested admin dashboard (http://167.71.206.110/admin)
- [ ] Updated MikroTik Walled Garden
- [ ] Tested complete WiFi flow
- [ ] (Optional) Set up SSL certificate

---

## 🎉 Done!

Your WiFi portal is now running on your DigitalOcean Droplet!

**Need help?** Check the logs or contact support.
