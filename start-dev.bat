@echo off
echo 🚀 Starting Video Quality Checker Development Environment

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

echo 📦 Building and starting services...

REM Start with Docker Compose
docker-compose up --build

echo ✅ Services are running!
echo 🌐 Frontend: http://localhost
echo 🔧 Backend API: http://localhost:5000
echo 📚 Health Check: http://localhost:5000/api/health
pause
