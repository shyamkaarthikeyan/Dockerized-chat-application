@echo off
REM Real-time Chat Application Setup Script for Windows
REM This script automates the deployment and initial setup

echo 🚀 Starting Real-time Chat Application Setup...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are available

REM Start the services
echo 📦 Starting all services with Docker Compose...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Wait for Ollama to be ready
echo 🤖 Waiting for Ollama to be ready...
set max_attempts=30
set attempt=0

:wait_loop
set /a attempt+=1
curl -f http://localhost:11434/api/tags >nul 2>&1
if not errorlevel 1 (
    echo ✅ Ollama is ready!
    goto ollama_ready
)

if %attempt% geq %max_attempts% (
    echo ❌ Ollama failed to start within expected time
    echo 📋 Check logs with: docker-compose logs ollama
    pause
    exit /b 1
)

echo ⏳ Attempt %attempt%/%max_attempts% - Ollama not ready yet...
timeout /t 10 /nobreak >nul
goto wait_loop

:ollama_ready
REM Pull the default LLM model
echo 📥 Pulling default LLM model (llama3.2)...
docker exec ollama ollama pull llama3.2

REM Optional: Pull additional models
set /p choice="🤔 Do you want to pull additional models? (y/n): "
if /i "%choice%"=="y" (
    echo 📥 Pulling additional models...
    docker exec ollama ollama pull mistral
    docker exec ollama ollama pull neural-chat
    echo ✅ Additional models downloaded!
)

REM Check if all services are healthy
echo 🔍 Checking service health...

REM Check backend
curl -f http://localhost:3001/health >nul 2>&1
if not errorlevel 1 (
    echo ✅ Backend is healthy
) else (
    echo ⚠️ Backend health check failed
)

REM Check frontend
curl -f http://localhost:8501/_stcore/health >nul 2>&1
if not errorlevel 1 (
    echo ✅ Frontend is healthy
) else (
    echo ⚠️ Frontend health check failed
)

echo.
echo 🎉 Setup complete!
echo.
echo 📋 Access your application:
echo    Frontend: http://localhost:8501
echo    Backend Health: http://localhost:3001/health
echo    Ollama API: http://localhost:11434/api/tags
echo.
echo 📖 Useful commands:
echo    View logs: docker-compose logs -f
echo    Stop services: docker-compose down
echo    Restart: docker-compose restart
echo.
echo 🚀 Happy chatting with your local LLM!
pause