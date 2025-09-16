@echo off
REM Complete Setup Script for Windows
REM Frontend-Backend Integration and GitHub Pages Deployment

echo 🚀 AUTONOMOUS NAVIGATION SYSTEM - COMPLETE DEPLOYMENT
echo =====================================================

REM Step 1: Backend Instructions
echo.
echo 📡 STEP 1: Start Backend on Raspberry Pi
echo ----------------------------------------
echo Please open a new terminal/command prompt and run:
echo ssh srihari@192.168.0.101
echo cd ~/autonomy_system
echo source venv/bin/activate  
echo python3 api.py
echo.
echo ⚠️  Keep that terminal open - the backend must stay running!
echo.
pause

REM Step 2: Test Backend
echo.
echo 🧪 STEP 2: Testing Backend Connection
echo ------------------------------------
python test_backend.py
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Backend test failed. Make sure backend is running on RPi.
    pause
    exit /b 1
)

REM Step 3: Build Frontend
echo.
echo 🔨 STEP 3: Building Frontend
echo ----------------------------
call npm run build:prod
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Frontend build failed.
    pause
    exit /b 1
)

REM Step 4: Test Frontend
echo.
echo 🖥️  STEP 4: Testing Frontend Locally
echo -----------------------------------
echo Starting local preview...
echo Open http://localhost:4173 in your browser
echo Check if everything works, then close this window to continue
start /wait npm run preview

REM Step 5: GitHub Setup
echo.
echo 🌐 STEP 5: GitHub Pages Deployment
echo ----------------------------------
echo Before deploying, make sure you have:
echo ✅ Created a GitHub repository named 'sentinel-view-system'
echo ✅ Pushed your code to GitHub
echo ✅ Enabled GitHub Pages in repository settings
echo.
set /p deploy="Deploy to GitHub Pages now? (y/n): "
if /i "%deploy%"=="y" (
    echo Deploying...
    call npm run deploy
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ Successfully deployed to GitHub Pages!
        echo 🌍 Your site will be available at:
        echo https://sikandar-irfan.github.io/sentinel-view-system/
    ) else (
        echo ❌ Deployment failed. Check the error messages above.
    )
) else (
    echo ⏭️  Skipping deployment. You can deploy later with: npm run deploy
)

echo.
echo 🎉 SETUP COMPLETE!
echo ==================
echo 📋 Summary:
echo ✅ Backend integration configured
echo ✅ Frontend built and tested  
echo ✅ GitHub Pages deployment ready
echo.
echo 🔗 Access your dashboard:
echo 🏠 Local: http://localhost:4173
echo 🌐 GitHub Pages: https://sikandar-irfan.github.io/sentinel-view-system/
echo.
echo 💡 Important: Keep your Raspberry Pi backend running for live data!
echo.
pause