#!/bin/bash

# AlphaGenome API Deployment Script (Root Level)
# This script deploys only the API from the plugin-genome repository

set -e

echo "🧬 AlphaGenome API Deployment (from plugin-genome)"
echo "================================================="

# Check if we're in the right directory
if [ ! -d "api" ]; then
    echo "❌ Error: api/ directory not found. Please run this script from the plugin-genome root directory."
    exit 1
fi

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
    if [ -f api/env.example ]; then
        cp api/env.example .env
        echo "📝 Created .env file from api/env.example"
        echo "⚠️  Please edit .env file and add your ALPHA_GENOME_API_KEY"
        echo "💡 Get your API key from: https://deepmind.google.com/science/alphagenome"
        exit 1
    else
        echo "❌ No api/env.example file found. Please create .env manually."
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
echo "📁 Building API from api/ directory..."

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
echo "🎉 API Deployment successful!"
echo "📁 Source: plugin-genome/api/"
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
echo "📁 Project structure:"
echo "  plugin-genome/          # Root repository"
echo "  ├── api/               # API source code"
echo "  ├── streamlit-demo/    # Streamlit demo (not deployed)"
echo "  ├── Dockerfile         # API Docker build"
echo "  ├── docker-compose.yml # Deployment config"
echo "  └── .env              # Environment variables"
echo ""
echo "🧬 Happy genomic analysis!" 