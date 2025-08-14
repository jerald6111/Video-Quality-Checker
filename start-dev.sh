#!/bin/bash

# Development startup script

echo "🚀 Starting Video Quality Checker Development Environment"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if ports are available
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "❌ Port 5000 is already in use. Please stop any services using this port."
    exit 1
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "❌ Port 3000 is already in use. Please stop any services using this port."
    exit 1
fi

echo "📦 Building and starting services..."

# Start with Docker Compose
docker-compose up --build

echo "✅ Services are running!"
echo "🌐 Frontend: http://localhost"
echo "🔧 Backend API: http://localhost:5000"
echo "📚 Health Check: http://localhost:5000/api/health"
