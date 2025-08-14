@echo off
echo 🚀 Video Quality Checker - Deployment Helper
echo =============================================
echo.

echo This script will help you deploy your application to Vercel and Render
echo.

echo [Step 1] Backend Deployment on Render
echo 1. Go to https://dashboard.render.com/
echo 2. Click 'New +' → 'Web Service'
echo 3. Connect GitHub repo: jerald6111/Video-Quality-Checker
echo 4. Configure:
echo    - Name: video-quality-checker-api
echo    - Root Directory: backend
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: python app_production.py
echo    - Environment Variables:
echo      PORT=5000
echo      FLASK_ENV=production
echo.

pause

echo.
echo [Step 2] Frontend Deployment on Vercel
echo 1. Go to https://vercel.com/dashboard
echo 2. Click 'New Project'
echo 3. Import repo: jerald6111/Video-Quality-Checker
echo 4. Configure:
echo    - Framework: Create React App
echo    - Root Directory: frontend
echo    - Build Command: npm run build
echo    - Output Directory: build
echo.

set /p RENDER_URL="Enter your Render backend URL (e.g., https://your-app.onrender.com): "

if not "%RENDER_URL%"=="" (
    echo.
    echo Add this environment variable in Vercel:
    echo REACT_APP_API_URL=%RENDER_URL%
    echo.
)

echo [Step 3] Update CORS Configuration
echo After deploying to Vercel, you'll get a URL like: https://your-app.vercel.app
echo Add this URL to the CORS configuration in backend/app_production.py
echo.

set /p commit_choice="Would you like to commit the new deployment files? (y/n): "

if /i "%commit_choice%"=="y" (
    git add .
    git commit -m "Add deployment configuration for Vercel and Render - Added production Flask app with enhanced mock responses - Created Vercel configuration for frontend deployment - Added comprehensive deployment documentation - Updated CORS settings for production"
    
    echo Committed deployment files!
    
    set /p push_choice="Push to GitHub? (y/n): "
    
    if /i "%push_choice%"=="y" (
        git push origin main
        echo Pushed to GitHub!
    )
)

echo.
echo 🎉 Deployment setup complete!
echo.
echo Next steps:
echo 1. Deploy backend on Render using the instructions above
echo 2. Deploy frontend on Vercel using the instructions above
echo 3. Update CORS settings with your actual Vercel URL
echo 4. Test both services
echo.
echo Documentation:
echo - Full deployment guide: DEPLOYMENT.md
echo - Development setup: DEVELOPMENT.md
echo.
echo Happy deploying! 🚀
pause
