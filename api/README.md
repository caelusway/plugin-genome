# 🧬 AlphaGenome REST API

A simple, production-ready REST API wrapper for Google DeepMind's AlphaGenome with comprehensive visualization capabilities.

## 🚀 Features

- **🔬 Genomic Predictions**: Interval and variant effect predictions
- **🎨 Visualization**: Publication-quality plots and charts
- **📚 Interactive Documentation**: Swagger UI with detailed biological context
- **🐳 Docker Ready**: Production deployment with Docker & Docker Compose
- **🔒 Production Security**: Nginx reverse proxy, rate limiting, health checks
- **🌐 CORS Support**: Cross-origin requests enabled
- **📊 Multiple Output Types**: RNA-seq, ATAC-seq, ChIP-seq, CAGE, DNase, HiC
- **🧪 Tissue-Specific**: UBERON ontology support for tissue-specific analysis

## 📋 Prerequisites

- **Docker** and **Docker Compose**
- **AlphaGenome API Key** from [DeepMind](https://deepmind.google.com/science/alphagenome)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd api
```

### 2. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env and add your API key
nano .env
```

Add your AlphaGenome API key:
```bash
ALPHA_GENOME_API_KEY=your_actual_api_key_here
```

### 3. Deploy with Docker

```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

The script will:
- ✅ Check Docker installation
- 🔧 Build the Docker image
- 🚀 Start the API server
- ⏳ Wait for health check
- 📋 Display access URLs

### 4. Access the API

- **🏥 Health Check**: http://localhost:8000/health
- **📚 Swagger UI**: http://localhost:8000/docs
- **📄 OpenAPI Spec**: http://localhost:8000/openapi.json

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose build && docker-compose up -d
```

## 🌐 Production Deployment

### With Nginx Reverse Proxy

```bash
# Start with production profile
docker-compose --profile production up -d
```

This includes:
- **🔒 Nginx reverse proxy** with security headers
- **⚡ Rate limiting** (10 requests/second)
- **📦 Gzip compression**
- **🛡️ Security headers** (XSS protection, content type validation)

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALPHA_GENOME_API_KEY` | **Required** - Your AlphaGenome API key | - |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `PYTHONUNBUFFERED` | Python output buffering | `1` |

## 📖 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check and status |
| `GET` | `/api/v1/outputs` | Available genomic output types |
| `GET` | `/api/v1/tissues` | Available tissue ontology terms |
| `POST` | `/api/v1/predict/interval` | Genomic interval predictions |
| `POST` | `/api/v1/predict/variant` | Variant effect predictions |

### Visualization Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/visualize/tracks` | Genomic track plots |
| `POST` | `/api/v1/visualize/variant` | Variant effect charts |
| `POST` | `/api/v1/visualize/summary` | Statistical summary plots |

## 🧪 Example Usage

### Predict Genomic Interval

```bash
curl -X POST "http://localhost:8000/api/v1/predict/interval" \
  -H "Content-Type: application/json" \
  -d '{
    "interval": {
      "chromosome": "chr22",
      "start": 35677410,
      "end": 36725986
    },
    "ontology_terms": ["UBERON:0001114"],
    "requested_outputs": ["RNA_SEQ", "ATAC_SEQ"]
  }'
```

### Visualize Results

```bash
curl -X POST "http://localhost:8000/api/v1/visualize/tracks" \
  -H "Content-Type: application/json" \
  -d '{
    "prediction_data": {
      "predictions": {
        "RNA_SEQ": {"shape": [1000], "mean": 0.5, "std": 0.2}
      }
    },
    "title": "CYP2B6 Gene Analysis"
  }'
```

## 🧬 Scientific Applications

### 🔬 Research Use Cases

- **Variant Effect Prediction**: Assess functional impact of genetic variants
- **Regulatory Analysis**: Identify enhancers, promoters, and regulatory elements
- **Tissue-Specific Studies**: Compare genomic activity across different tissues
- **Publication Visualization**: Generate high-quality plots for manuscripts

### 🏥 Clinical Applications

- **Pathogenicity Assessment**: Evaluate disease-causing potential of variants
- **Pharmacogenomics**: Predict drug response variations
- **Personalized Medicine**: Individual genetic risk assessment

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements_fastapi_fixed.txt

# Set environment variable
export ALPHA_GENOME_API_KEY=your_key_here

# Run server
python3 simple_server.py
```

### File Structure

```
api/
├── simple_server.py          # Main API server
├── load_env_helper.py        # Environment configuration
├── requirements_fastapi_fixed.txt  # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── nginx.conf              # Nginx reverse proxy config
├── deploy.sh               # Deployment script
├── env.example             # Environment template
└── README.md               # This file
```

## 🔧 Troubleshooting

### Common Issues

1. **API Key Not Working**
   ```bash
   # Check if API key is set
   grep ALPHA_GENOME_API_KEY .env
   
   # Test API key manually
   curl -H "Authorization: Bearer YOUR_KEY" https://api.alphagenome.com/health
   ```

2. **Docker Build Fails**
   ```bash
   # Clear Docker cache
   docker system prune -a
   
   # Rebuild from scratch
   docker-compose build --no-cache
   ```

3. **Health Check Fails**
   ```bash
   # Check logs
   docker-compose logs alphagenome-api
   
   # Check container status
   docker-compose ps
   ```

### Performance Tips

- **Memory**: Ensure at least 4GB RAM available for genomic predictions
- **Network**: Stable internet connection required for AlphaGenome API calls
- **Storage**: Consider volume mounts for persistent data in production

## 📚 Documentation

- **AlphaGenome Docs**: https://www.alphagenomedocs.com/
- **API Reference**: Available at `/docs` when server is running
- **OpenAPI Spec**: Available at `/openapi.json`

## 📄 License

This API wrapper is for **non-commercial use only**, following AlphaGenome's terms of service.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## 📞 Support

- **GitHub Issues**: For bugs and feature requests
- **AlphaGenome Support**: alphagenome@google.com
- **Documentation**: Check `/docs` endpoint for interactive API documentation

---

**🧬 Happy Genomic Analysis!** 🚀 