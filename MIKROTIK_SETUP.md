# 🔧 MikroTik Configuration Guide

Complete guide for configuring MikroTik router (IP: 103.165.204.234) for NUANU WiFi Login Portal.

---

## Prerequisites

- **MikroTik Winbox** installed on your computer
- **Router IP**: 103.165.204.234
- **Admin credentials** for MikroTik
- **Railway URL**: Your deployed app URL from Railway

---

## Part 1: Connect to MikroTik

### Using Winbox

1. Download Winbox from https://mikrotik.com/download
2. Open Winbox
3. Enter:
   - **Connect To**: 103.165.204.234
   - **Login**: admin (or your username)
   - **Password**: (your password)
4. Click **Connect**

### Using SSH (Alternative)

```bash
ssh admin@103.165.204.234
```

---

## Part 2: Basic Hotspot Setup (If Not Already Configured)

### Check if Hotspot is Already Running

```
/ip hotspot print
```

If you see a hotspot server, skip to Part 3.

### Create New Hotspot (If Needed)

1. Go to **IP → Hotspot**
2. Click **Hotspot Setup**
3. Follow wizard:
   - **Hotspot Interface**: Select your WiFi interface (e.g., wlan1)
   - **Local Address**: 192.168.88.1/24 (or your network)
   - **Address Pool**: 192.168.88.10-192.168.88.254
   - **Certificate**: none
   - **SMTP Server**: 0.0.0.0
   - **DNS Servers**: 8.8.8.8
   - **DNS Name**: nuanu.wifi
   - **Local Hotspot User**: user
   - **Password**: user

---

## Part 3: Configure Walled Garden

Walled Garden allows access to specific websites without authentication.

### Using Winbox GUI

1. Go to **IP → Hotspot → Walled Garden**
2. Click **"+"** to add each rule:

#### Rule 1: Railway App
```
Dst. Host: *.railway.app
Action: allow
```

#### Rule 2: Your Specific Domain
```
Dst. Host: your-app-name.up.railway.app
Action: allow
```
*(Replace with your actual Railway domain)*

#### Rule 3: Background Image
```
Dst. Host: images.lifestyleasia.com
Action: allow
```

#### Rule 4: Redirect Destination
```
Dst. Host: nuanu.com
Action: allow
```

#### Rule 5: Wildcard for NUANU
```
Dst. Host: *.nuanu.com
Action: allow
```

### Using Terminal

```
/ip hotspot walled-garden
add dst-host=*.railway.app action=allow
add dst-host=your-app-name.up.railway.app action=allow
add dst-host=images.lifestyleasia.com action=allow
add dst-host=nuanu.com action=allow
add dst-host=*.nuanu.com action=allow
```

### Verify Walled Garden Rules

```
/ip hotspot walled-garden print
```

---

## Part 4: Configure Walled Garden IP (Important!)

Sometimes domain-based walled garden doesn't work. Add IP addresses:

### Find Railway App IP

On your computer:
```bash
nslookup your-app-name.up.railway.app
```

Note the IP address (e.g., 34.123.45.67)

### Add IP to Walled Garden

```
/ip hotspot walled-garden ip
add dst-address=34.123.45.67 action=allow
```

---

## Part 5: Configure Hotspot Server Profile

### Using Winbox

1. Go to **IP → Hotspot → Server Profiles**
2. Double-click your profile (usually "hsprof1")

#### General Tab
- **Name**: hsprof1
- **Hotspot Address**: (leave default)
- **DNS Name**: nuanu.wifi

#### Login Tab
- **Login By**: `HTTP CHAP`
- **HTTP Cookie Lifetime**: `1d`
- **HTTP PAP**: ☑ (checked)
- **HTTPS**: ☐ (unchecked, unless you have certificate)

#### RADIUS Tab
- Leave default (unless using RADIUS)

#### Trial Tab
- **Trial Uptime**: 0s (no trial)
- **Trial User Profile**: default

### Using Terminal

```
/ip hotspot profile
set [find name="hsprof1"] login-by=http-chap,http-pap http-cookie-lifetime=1d
```

---

## Part 6: Create Hotspot Users

### Create Default User

1. Go to **IP → Hotspot → Users**
2. Click **"+"**
3. Fill in:
   - **Name**: user
   - **Password**: user
   - **Profile**: default
   - **Limit Uptime**: (leave empty for unlimited)
4. Click **OK**

### Using Terminal

```
/ip hotspot user
add name=user password=user profile=default
```

### Create Multiple Users (Optional)

```
/ip hotspot user
add name=guest password=guest123 profile=default limit-uptime=2h
add name=premium password=premium123 profile=default limit-uptime=1d
```

---

## Part 7: Customize Login Page Redirect

### Method A: External Hosted Login (Recommended)

#### Create Redirect HTML

1. Create a file named `login.html` with this content:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=https://your-app-name.up.railway.app/">
    <title>Redirecting...</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .loader {
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div style="text-align: center;">
        <div class="loader"></div>
        <h2>Redirecting to login...</h2>
        <p>Please wait...</p>
    </div>
</body>
</html>
```

2. Replace `your-app-name.up.railway.app` with your actual Railway URL

#### Upload to MikroTik

1. Open **Winbox** → **Files**
2. Drag and drop `login.html` to the file list
3. Wait for upload to complete
4. In terminal, move to hotspot directory:

```
/file
print
# Note the file number
move [find name="login.html"] destination=hotspot/login.html
```

### Method B: Direct API Integration

Upload your actual `public/login.html` to MikroTik:

1. Edit `public/login.html` line 213:
```javascript
const API_BASE = "https://your-app-name.up.railway.app";
```

2. Upload to MikroTik `/hotspot/` directory
3. Ensure Walled Garden allows API access

---

## Part 8: Configure DNS

### Set DNS Servers

```
/ip dns
set servers=8.8.8.8,8.8.4.4 allow-remote-requests=yes
```

### Verify DNS

```
/ip dns print
```

---

## Part 9: Firewall Configuration

### Allow Hotspot Traffic

```
/ip firewall filter
add chain=input action=accept protocol=tcp dst-port=80 comment="Allow HTTP for Hotspot"
add chain=input action=accept protocol=tcp dst-port=443 comment="Allow HTTPS for Hotspot"
add chain=input action=accept protocol=udp dst-port=53 comment="Allow DNS"
```

### NAT Configuration

```
/ip firewall nat
add chain=srcnat action=masquerade out-interface=ether1 comment="Hotspot NAT"
```

*(Replace ether1 with your WAN interface)*

---

## Part 10: Testing

### Test 1: Check Hotspot Status

```
/ip hotspot print
```

Should show:
- **Name**: hotspot1
- **Interface**: wlan1 (or your interface)
- **Address Pool**: your pool
- **Profile**: hsprof1

### Test 2: Check Active Users

```
/ip hotspot active print
```

### Test 3: Manual Login Test

1. Connect device to WiFi
2. Open browser
3. Should redirect to login page
4. Fill form and submit
5. Should connect and redirect to nuanu.com

### Test 4: Check Logs

```
/log print where topics~"hotspot"
```

Look for:
- User login events
- Authentication success/failure
- Redirect events

---

## Part 11: Advanced Configuration

### Set Session Timeout

```
/ip hotspot profile
set [find name="hsprof1"] session-timeout=1d idle-timeout=5m
```

### Set Bandwidth Limits

```
/ip hotspot user profile
add name="basic" rate-limit="2M/2M" shared-users=1
add name="premium" rate-limit="10M/10M" shared-users=3

/ip hotspot user
set [find name="user"] profile=basic
```

### Enable HTTPS (Requires Certificate)

```
/ip hotspot profile
set [find name="hsprof1"] use-radius=yes ssl-certificate=your-cert
```

### Custom Error Pages

Create `error.html` and upload to `/hotspot/` directory.

### MAC Address Bypass

Allow specific devices without login:

```
/ip hotspot ip-binding
add address=192.168.88.100 type=bypassed mac-address=AA:BB:CC:DD:EE:FF
```

---

## Part 12: Monitoring & Maintenance

### View Active Sessions

```
/ip hotspot active print
```

### Disconnect User

```
/ip hotspot active remove [find user="user"]
```

### View User Statistics

```
/ip hotspot user print stats
```

### Clear All Sessions

```
/ip hotspot active remove [find]
```

### Backup Configuration

```
/export file=hotspot-backup
```

Download from **Files** in Winbox.

### Monitor Bandwidth

```
/interface monitor-traffic wlan1
```

---

## Part 13: Troubleshooting

### Issue: Login Page Not Showing

**Check:**
1. Hotspot is running: `/ip hotspot print`
2. Interface is correct: `/interface print`
3. DNS is working: `/ip dns print`

**Solution:**
```
/ip hotspot
set [find] disabled=no
```

### Issue: Can't Access External Login Page

**Check:**
1. Walled Garden rules: `/ip hotspot walled-garden print`
2. DNS resolution: `/ping your-app-name.up.railway.app`

**Solution:**
Add IP-based walled garden rule (see Part 4)

### Issue: Users Can't Authenticate

**Check:**
1. User exists: `/ip hotspot user print`
2. Profile is correct: `/ip hotspot profile print`

**Solution:**
```
/ip hotspot user
set [find name="user"] password=user
```

### Issue: Redirect Not Working

**Check:**
1. HTTP CHAP enabled: `/ip hotspot profile print`
2. Cookie lifetime: Should be > 0

**Solution:**
```
/ip hotspot profile
set [find name="hsprof1"] login-by=http-chap http-cookie-lifetime=1d
```

### Issue: Slow Performance

**Check:**
1. CPU usage: `/system resource print`
2. Active users: `/ip hotspot active print count-only`

**Solution:**
- Limit concurrent users
- Increase bandwidth
- Upgrade router hardware

---

## Part 14: Security Best Practices

### 1. Change Default Credentials

```
/user
set admin password=NewStrongPassword123!
```

### 2. Disable Unused Services

```
/ip service
disable telnet,ftp,www
```

### 3. Enable Firewall

```
/ip firewall filter
add chain=input action=drop in-interface=wlan1 comment="Drop all other input from WiFi"
```

### 4. Regular Backups

Schedule automatic backups:

```
/system scheduler
add name=daily-backup on-event="/system backup save name=backup" start-time=03:00:00 interval=1d
```

### 5. Monitor Logs

```
/log
add topics=hotspot,info action=memory
```

---

## Part 15: Quick Reference Commands

### Restart Hotspot

```
/ip hotspot
set [find] disabled=yes
set [find] disabled=no
```

### Clear User Sessions

```
/ip hotspot active remove [find]
```

### View Configuration

```
/ip hotspot export
```

### Reset Hotspot (Careful!)

```
/ip hotspot remove [find]
```

### Check Version

```
/system package print
```

### Reboot Router

```
/system reboot
```

---

## 📞 Support Resources

- **MikroTik Wiki**: https://wiki.mikrotik.com/wiki/Hotspot
- **MikroTik Forum**: https://forum.mikrotik.com
- **Video Tutorials**: https://www.youtube.com/mikrotik

---

## ✅ Configuration Checklist

- [ ] Connected to MikroTik via Winbox
- [ ] Hotspot server created/verified
- [ ] Walled Garden rules added
- [ ] Walled Garden IPs added
- [ ] Server profile configured
- [ ] Hotspot user created (user/user)
- [ ] Login page uploaded
- [ ] DNS configured
- [ ] Firewall rules set
- [ ] NAT configured
- [ ] Tested login from device
- [ ] Verified data saves to database
- [ ] Checked logs for errors
- [ ] Backup configuration saved

---

**Your MikroTik is now configured! 🎉**

Connect to your WiFi and test the complete flow:
1. Connect to WiFi
2. Browser opens login page
3. Fill form
4. Submit
5. Redirect to nuanu.com
6. Check admin dashboard for data
