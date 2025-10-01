#!/bin/bash

# DigitalOcean Droplet Deployment Script
# Droplet: welcome-to-nuanu-new
# IP: 167.71.206.110

echo "🚀 Deploying to DigitalOcean Droplet..."

# Update system
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install Python 3.11 and pip
echo "🐍 Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3-pip nginx supervisor

# Install PostgreSQL client for database connection
sudo apt install -y postgresql-client libpq-dev

# Create app directory
echo "📁 Setting up application directory..."
sudo mkdir -p /var/www/nuanu-wifi-portal
sudo chown -R $USER:$USER /var/www/nuanu-wifi-portal
cd /var/www/nuanu-wifi-portal

# Clone or copy application
echo "📥 Copying application files..."
# Files will be copied via SCP or Git

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo "⚙️ Creating environment configuration..."
cat > .env << 'EOF'
# Server Configuration
PORT=8000
SECRET_KEY=super-secret-key-change-this-in-production

# PostgreSQL Database Configuration
DB_USER=doadmin
DB_PASSWORD=YOUR_DB_PASSWORD_HERE
DB_HOST=welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com
DB_PORT=25060
DB_NAME=welcome-to-nuanu-new

# Dashboard Password
DASHBOARD_PASSWORD=Bali0361

# Base URL
BASE_URL=http://167.71.206.110

# MikroTik Configuration
GATEWAY_IP=172.19.20.1
HOTSPOT_USER=user
HOTSPOT_PASS=user
DST_URL=https://nuanu.com/
EOF

echo "⚠️  IMPORTANT: Edit /var/www/nuanu-wifi-portal/.env and add your DB_PASSWORD!"

# Configure Supervisor (keeps app running)
echo "🔄 Configuring Supervisor..."
sudo tee /etc/supervisor/conf.d/nuanu-wifi-portal.conf > /dev/null << 'EOF'
[program:nuanu-wifi-portal]
directory=/var/www/nuanu-wifi-portal
command=/var/www/nuanu-wifi-portal/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/nuanu-wifi-portal.err.log
stdout_logfile=/var/log/nuanu-wifi-portal.out.log
environment=PATH="/var/www/nuanu-wifi-portal/venv/bin"
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/nuanu-wifi-portal > /dev/null << 'EOF'
server {
    listen 80;
    server_name 167.71.206.110;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/nuanu-wifi-portal/public/;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/nuanu-wifi-portal /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart services
echo "🔄 Starting services..."
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart nuanu-wifi-portal
sudo systemctl restart nginx

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your app is now running at: http://167.71.206.110"
echo "📊 Admin dashboard: http://167.71.206.110/admin"
echo ""
echo "⚠️  NEXT STEPS:"
echo "1. Edit /var/www/nuanu-wifi-portal/.env and add your DB_PASSWORD"
echo "2. Restart the app: sudo supervisorctl restart nuanu-wifi-portal"
echo "3. Check logs: sudo tail -f /var/log/nuanu-wifi-portal.out.log"
echo ""
echo "🔐 Optional: Set up SSL with Let's Encrypt:"
echo "   sudo apt install certbot python3-certbot-nginx"
echo "   sudo certbot --nginx -d yourdomain.com"
