#!/bin/bash

# Real-time Chat Application Setup Script
# This script automates the deployment and initial setup

set -e

echo "🚀 Starting Real-time Chat Application Setup..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Start the services
echo "📦 Starting all services with Docker Compose..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Wait for Ollama to be ready
echo "🤖 Waiting for Ollama to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "✅ Ollama is ready!"
        break
    fi
    
    attempt=$((attempt + 1))
    echo "⏳ Attempt $attempt/$max_attempts - Ollama not ready yet..."
    sleep 10
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Ollama failed to start within expected time"
    echo "📋 Check logs with: docker-compose logs ollama"
    exit 1
fi

# Pull the default LLM model
echo "📥 Pulling default LLM model (llama3.2)..."
docker exec ollama ollama pull llama3.2

# Optional: Pull additional models
read -p "🤔 Do you want to pull additional models? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 Pulling additional models..."
    docker exec ollama ollama pull mistral
    docker exec ollama ollama pull neural-chat
    echo "✅ Additional models downloaded!"
fi

# Check if all services are healthy
echo "🔍 Checking service health..."

# Check backend
if curl -f http://localhost:3001/health >/dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "⚠️ Backend health check failed"
fi

# Check frontend
if curl -f http://localhost:8501/_stcore/health >/dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "⚠️ Frontend health check failed"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Access your application:"
echo "   Frontend: http://localhost:8501"
echo "   Backend Health: http://localhost:3001/health"
echo "   Ollama API: http://localhost:11434/api/tags"
echo ""
echo "📖 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart: docker-compose restart"
echo ""
echo "🚀 Happy chatting with your local LLM!"