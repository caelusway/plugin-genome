#!/bin/bash

# AlphaGenome API Deployment Script
# This script helps deploy the AlphaGenome API using Docker

set -e

echo "🧬 AlphaGenome API Deployment Script"
echo "===================================="

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

# Check for environment file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "📝 Created .env file from env.example"
        echo "⚠️  Please edit .env file and add your ALPHA_GENOME_API_KEY"
        echo "💡 Get your API key from: https://deepmind.google.com/science/alphagenome"
        exit 1
    else
        echo "❌ No env.example file found. Please create .env manually."
        exit 1
    fi
fi

# Check if API key is set
if ! grep -q "ALPHA_GENOME_API_KEY=.*[^[:space:]]" .env; then
    echo "❌ ALPHA_GENOME_API_KEY is not set in .env file"
    echo "💡 Please edit .env file and add your AlphaGenome API key"
    exit 1
fi

echo "✅ Environment configuration looks good"

# Build and start the services
echo "🔧 Building Docker image..."
docker-compose build

echo "🚀 Starting AlphaGenome API..."
docker-compose up -d

# Wait for health check
echo "⏳ Waiting for API to be ready..."
sleep 10

# Check health
for i in {1..12}; do
    if curl -f http://localhost:8000/health &> /dev/null; then
        echo "✅ API is healthy and ready!"
        break
    fi
    if [ $i -eq 12 ]; then
        echo "❌ API failed to start properly"
        echo "📋 Checking logs..."
        docker-compose logs alphagenome-api
        exit 1
    fi
    echo "⏳ Still waiting... ($i/12)"
    sleep 5
done

echo ""
echo "🎉 Deployment successful!"
echo "📋 API Health: http://localhost:8000/health"
echo "📚 Swagger UI: http://localhost:8000/docs"
echo "📄 OpenAPI Spec: http://localhost:8000/openapi.json"
echo ""
echo "🔧 Useful commands:"
echo "  View logs:    docker-compose logs -f"
echo "  Stop API:     docker-compose down"
echo "  Restart API:  docker-compose restart"
echo "  Update API:   docker-compose pull && docker-compose up -d"
echo ""
echo "🧬 Happy genomic analysis!" 