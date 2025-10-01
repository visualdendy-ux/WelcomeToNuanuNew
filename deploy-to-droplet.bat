@echo off
echo ========================================
echo  Deploy to DigitalOcean Droplet
echo  IP: 167.71.206.110
echo ========================================
echo.

echo This script will:
echo 1. Upload your code to the droplet
echo 2. Run the deployment script
echo.

set /p CONTINUE="Continue? (y/n): "
if /i not "%CONTINUE%"=="y" exit /b

echo.
echo Step 1: Uploading files to droplet...
echo.

REM Using SCP to upload files (requires SSH client)
scp -r . root@167.71.206.110:/tmp/WELCOME-TO-NUANU-NEW

if errorlevel 1 (
    echo.
    echo ERROR: Failed to upload files!
    echo Make sure you have SSH access to the droplet.
    echo.
    pause
    exit /b 1
)

echo.
echo Step 2: Running deployment script on droplet...
echo.

REM Connect and run deployment
ssh root@167.71.206.110 "cd /tmp/WELCOME-TO-NUANU-NEW && chmod +x deploy.sh && sudo ./deploy.sh"

if errorlevel 1 (
    echo.
    echo ERROR: Deployment failed!
    echo Check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Deployment Complete!
echo ========================================
echo.
echo Your app is now running at:
echo   http://167.71.206.110
echo.
echo Admin dashboard:
echo   http://167.71.206.110/admin
echo.
echo IMPORTANT: You need to set your database password!
echo.
echo Run this command on the droplet:
echo   ssh root@167.71.206.110
echo   sudo nano /var/www/nuanu-wifi-portal/.env
echo   (Edit DB_PASSWORD line)
echo   sudo supervisorctl restart nuanu-wifi-portal
echo.
pause
