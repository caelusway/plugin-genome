FROM python:3.11-slim

# AlphaGenome API Docker Image for Production
# 
# Production Deployment:
# 1. Set BASE_URL environment variable to your actual server URL:
#    docker run -e BASE_URL=https://api.yourdomain.com -p 8000:8000 your-image
# 
# 2. For HTTPS deployment, use a reverse proxy (nginx, traefik, etc.)
# 
# 3. Environment Variables:
#    - BASE_URL: Full URL for OpenAPI spec (e.g., https://api.yourdomain.com)
#    - HOST: Bind address (default: 0.0.0.0)
#    - PORT: Port number (default: 8000)
#    - ALPHA_GENOME_API_KEY: Your AlphaGenome API key

# Set working directory
WORKDIR /app

# Install system dependencies for AlphaGenome and visualization
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY api/requirements_fastapi_fixed.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy API application code
COPY api/simple_server.py .
COPY api/load_env_helper.py .
COPY api/README.md .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000
# For production, set BASE_URL to your actual server URL
# Example: ENV BASE_URL=https://api.yourdomain.com
ENV BASE_URL="https://plugin-genome-production.up.railway.app"

# Expose port
EXPOSE 8000

# Health check using environment variables
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://127.0.0.1:${PORT}/health || exit 1

# Start the simple server
CMD ["python3", "simple_server.py"] 