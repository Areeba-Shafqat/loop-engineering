@echo off
REM Update Frontend with Railway Backend URL
REM Usage: connect-backend.bat <your-railway-backend-url>

if "%1"=="" (
    echo ==================================================
    echo   ERROR: Please provide the Railway backend URL
    echo ==================================================
    echo.
    echo Usage: connect-backend.bat https://your-backend-url.railway.app
    echo.
    echo To get your backend URL:
    echo 1. Open: https://railway.com/project/ad7cbc23-7fc4-4159-b3ff-147d8330e01b
    echo 2. Click on 'loop-engineering' service
    echo 3. Go to Settings -^> Networking
    echo 4. Click 'Generate Domain' if not generated
    echo 5. Copy the public URL and run this script again
    echo.
    pause
    exit /b 1
)

set BACKEND_URL=%1

echo ==================================================
echo   Connecting Frontend to Backend
echo ==================================================
echo.
echo Backend URL: %BACKEND_URL%
echo Frontend: https://frontend-fawn-six-17.vercel.app
echo.
echo Updating Vercel environment variable...
echo.

cd frontend

REM Remove old environment variable
vercel env rm VITE_API_URL production -y 2>nul

REM Add new environment variable
echo %BACKEND_URL%/api | vercel env add VITE_API_URL production

echo.
echo Redeploying frontend...
vercel --prod

echo.
echo ==================================================
echo   Deployment Complete!
echo ==================================================
echo.
echo Frontend: https://frontend-fawn-six-17.vercel.app
echo Backend:  %BACKEND_URL%
echo.
echo Test your deployment at:
echo https://frontend-fawn-six-17.vercel.app
echo.
pause
