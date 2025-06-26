# 🧬 Plugin Genome

A comprehensive genomic analysis platform featuring AlphaGenome API integration and visualization tools.

## 📁 Project Structure

```
plugin-genome/
├── api/                    # 🔬 AlphaGenome REST API
│   ├── simple_server.py    # Main API server
│   ├── load_env_helper.py  # Environment configuration
│   ├── requirements_*.txt  # Python dependencies
│   └── README.md          # API documentation
├── streamlit-demo/         # 🎨 Streamlit visualization demo
├── Dockerfile             # 🐳 API Docker build configuration
├── docker-compose.yml     # 🚀 Deployment orchestration
├── deploy-api.sh          # 📦 API deployment script
└── README.md              # This file
```

## 🚀 Quick API Deployment

Deploy only the AlphaGenome API from this repository:

### 1. Prerequisites

- **Docker** and **Docker Compose** installed
- **AlphaGenome API Key** from [DeepMind](https://deepmind.google.com/science/alphagenome)

### 2. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd plugin-genome

# Copy environment template
cp api/env.example .env

# Edit .env and add your API key
nano .env
```

Add your AlphaGenome API key:
```bash
ALPHA_GENOME_API_KEY=your_actual_api_key_here
```

### 3. Deploy API

```bash
# Make deployment script executable
chmod +x deploy-api.sh

# Deploy the API
./deploy-api.sh
```

### 4. Access API

- **🏥 Health Check**: http://localhost:8000/health
- **📚 Swagger UI**: http://localhost:8000/docs
- **📄 OpenAPI Spec**: http://localhost:8000/openapi.json

## 🐳 Docker Commands

```bash
# Start API
docker-compose up -d

# View logs
docker-compose logs -f alphagenome-api

# Stop API
docker-compose down

# Restart API
docker-compose restart

# Production with Nginx
docker-compose --profile production up -d
```

## 🧬 API Features

- **🔬 Genomic Predictions**: Interval and variant effect analysis
- **🎨 Visualization**: Publication-quality plots and charts
- **📚 Interactive Docs**: Comprehensive Swagger UI
- **🧪 Tissue-Specific**: UBERON ontology support
- **📊 Multiple Outputs**: RNA-seq, ATAC-seq, ChIP-seq, CAGE, DNase, HiC

## 📖 API Endpoints

### Core Predictions
- `GET /health` - Health check
- `GET /api/v1/outputs` - Available genomic output types
- `GET /api/v1/tissues` - Tissue ontology terms
- `POST /api/v1/predict/interval` - Genomic interval predictions
- `POST /api/v1/predict/variant` - Variant effect predictions

### Visualizations
- `POST /api/v1/visualize/tracks` - Genomic track plots
- `POST /api/v1/visualize/variant` - Variant effect charts
- `POST /api/v1/visualize/summary` - Statistical summaries

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

### Generate Visualization
```bash
curl -X POST "http://localhost:8000/api/v1/visualize/tracks" \
  -H "Content-Type: application/json" \
  -d '{
    "prediction_data": {
      "predictions": {
        "RNA_SEQ": {"shape": [1000], "mean": 0.5, "std": 0.2}
      }
    },
    "title": "Genomic Analysis Results"
  }'
```

## 🛠️ Development

### Local Development
```bash
# Install API dependencies
cd api
pip install -r requirements_fastapi_fixed.txt

# Set environment variable
export ALPHA_GENOME_API_KEY=your_key_here

# Run API server
python3 simple_server.py
```

### Streamlit Demo
```bash
# Run visualization demo
cd streamlit-demo
# Follow instructions in streamlit-demo/README.md
```

## 🌐 Production Deployment

### With Nginx Reverse Proxy
```bash
# Deploy with production profile
docker-compose --profile production up -d
```

Features:
- **🔒 Security headers** and rate limiting
- **📦 Gzip compression**
- **⚡ Load balancing** ready
- **🛡️ SSL termination** support

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALPHA_GENOME_API_KEY` | **Required** - AlphaGenome API key | - |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## 🧬 Scientific Applications

### 🔬 Research Use Cases
- **Variant Effect Prediction**: Functional impact assessment
- **Regulatory Analysis**: Enhancer and promoter identification
- **Multi-tissue Studies**: Comparative genomic analysis
- **Publication Visualization**: High-quality scientific plots

### 🏥 Clinical Applications
- **Pathogenicity Assessment**: Disease variant evaluation
- **Pharmacogenomics**: Drug response prediction
- **Personalized Medicine**: Individual risk assessment

## 🔧 Troubleshooting

### Common Issues

1. **API Key Problems**
   ```bash
   # Check API key in environment
   grep ALPHA_GENOME_API_KEY .env
   ```

2. **Docker Build Issues**
   ```bash
   # Clear Docker cache
   docker system prune -a
   docker-compose build --no-cache
   ```

3. **Health Check Failures**
   ```bash
   # Check container logs
   docker-compose logs alphagenome-api
   ```

## 📚 Documentation

- **API Documentation**: Available at `/docs` when running
- **AlphaGenome Docs**: https://www.alphagenomedocs.com/
- **API Reference**: Interactive Swagger UI

## 📄 License

This project is for **non-commercial use only**, following AlphaGenome's terms of service.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes in appropriate directory (`api/` or `streamlit-demo/`)
4. Test with Docker deployment
5. Submit a pull request

---

**🧬 Happy Genomic Analysis!** 🚀 