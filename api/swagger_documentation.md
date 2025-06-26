# 🧬 AlphaGenome REST API - Swagger Documentation Guide

This document provides comprehensive information about the AlphaGenome REST API's Swagger/OpenAPI documentation, based on Google DeepMind's official AlphaGenome documentation.

## 📚 API Overview

The AlphaGenome REST API provides programmatic access to Google DeepMind's AlphaGenome model through clean REST endpoints. The API includes comprehensive Swagger/OpenAPI documentation with:

- **Interactive Documentation**: Auto-generated docs at `/docs` (Swagger UI)
- **Alternative Documentation**: ReDoc interface at `/redoc`
- **OpenAPI Schema**: Machine-readable schema at `/openapi.json`

## 🎯 Key Features of Our Swagger Documentation

### 1. **Comprehensive Descriptions**
Every endpoint includes detailed descriptions explaining:
- Purpose and functionality
- Use cases and applications  
- Performance considerations
- Clinical applications (for variant analysis)

### 2. **Rich Examples**
All request/response models include:
- Realistic example data
- Multiple use case scenarios
- Expected response formats
- Error response examples

### 3. **Detailed Parameter Documentation**
Each parameter includes:
- Data type and validation rules
- Example values
- Required vs optional status
- Biological context and meaning

### 4. **Organized Tag Structure**
Endpoints are grouped into logical categories:
- **Health**: Server status and monitoring
- **Configuration**: Supported outputs and tissues
- **Predictions**: Core genomic predictions
- **Variant Analysis**: Genetic variant effects
- **Async Jobs**: Long-running operations

## 🔬 AlphaGenome Model Information

### Supported Output Types

Our Swagger docs detail all supported genomic predictions:

#### Expression & Transcription
- **RNA_SEQ**: Gene expression levels from RNA sequencing
  - Resolution: Single base-pair
  - Use case: Transcriptional activity analysis
- **CAGE**: Cap analysis gene expression (promoter activity)
  - Resolution: Single base-pair  
  - Use case: Transcription initiation sites

#### Chromatin Accessibility
- **ATAC_SEQ**: Assay for transposase-accessible chromatin
  - Resolution: Single base-pair
  - Use case: Open chromatin regions
- **DNASE_SEQ**: DNase hypersensitivity sites
  - Resolution: Single base-pair
  - Use case: Regulatory element identification

#### Chromatin Modifications
- **CHIP_SEQ**: Chromatin immunoprecipitation sequencing
  - Resolution: Single base-pair
  - Use case: Protein-DNA interactions
- **HISTONE_MARKS**: Histone modification patterns
  - Resolution: Single base-pair
  - Use case: Epigenetic state analysis

### Supported Sequence Lengths

The API documentation details optimal sequence lengths:

- **2KB**: Promoter regions and small regulatory elements
- **16KB**: Gene loci with proximal regulatory elements  
- **100KB**: Large regulatory domains and gene clusters
- **500KB**: Topologically associating domains (TADs)
- **1MB**: Large chromosomal segments

### Tissue Ontology Terms

Comprehensive tissue coverage with UBERON terms:

#### Major Categories
- **Digestive System**: Colon, liver, esophagus
- **Respiratory System**: Lung tissues
- **Cardiovascular System**: Heart and blood vessels
- **Nervous System**: Brain and neural tissues
- **Urinary System**: Kidney and related organs
- **Immune System**: Lymph nodes and immune organs
- **Reproductive System**: Prostate, breast, reproductive organs

## 📋 Endpoint Documentation Details

### Health Endpoints

#### `GET /health`
- **Purpose**: Comprehensive server health check
- **Returns**: Server status, AlphaGenome initialization, capabilities
- **Use Cases**: Monitoring, capability discovery, troubleshooting

### Configuration Endpoints

#### `GET /api/v1/outputs`
- **Purpose**: Get all supported output types and sequence lengths
- **Enhanced Info**: Detailed descriptions, resolutions, use cases
- **Response**: Structured data with biological context

#### `GET /api/v1/tissues`
- **Purpose**: Get tissue ontology terms for predictions
- **Organization**: Grouped by biological system
- **Metadata**: Names, categories, descriptions

### Prediction Endpoints

#### `POST /api/v1/predict/interval`
- **Purpose**: Multimodal genomic predictions for DNA intervals
- **Key Features**: 
  - Multiple output types in single request
  - Tissue-specific predictions
  - Single base-pair resolution
- **Use Cases**: Regulatory analysis, gene expression, chromatin state
- **Performance Notes**: Scaling considerations for large intervals

#### `POST /api/v1/predict/variant`
- **Purpose**: Comprehensive variant effect prediction
- **Analysis Process**:
  1. Reference sequence prediction
  2. Alternate sequence prediction  
  3. Effect calculation and interpretation
- **Variant Types**: SNVs, insertions, deletions, complex variants
- **Clinical Applications**: Pathogenicity assessment, functional annotation

### Variant Analysis Endpoints

#### `POST /api/v1/score/variant`
- **Purpose**: Simplified variant impact scoring
- **Scoring System**: 0.0-1.0 scale with interpretation
- **Clinical Context**: Impact levels, significance, recommendations
- **Performance**: Optimized for high-throughput screening

### Async Job Endpoints

#### `POST /api/v1/jobs/predict/variant`
- **Purpose**: Create background variant prediction jobs
- **When to Use**: Large intervals, multiple outputs, batch processing
- **Workflow**: Submit → Poll → Retrieve results

#### `GET /api/v1/jobs/{job_id}`
- **Purpose**: Check job status and retrieve results
- **States**: Pending, running, completed, failed
- **Polling**: Recommendations for efficient status checking

## 🔧 Advanced Swagger Features

### Data Validation
All models include comprehensive validation:
- **Chromosome Format**: Regex validation for proper chromosome naming
- **Position Ranges**: Genomic coordinate validation
- **DNA Sequences**: Base composition validation (A, T, G, C)
- **Interval Logic**: Start < End validation

### Error Handling
Detailed error responses with:
- **HTTP Status Codes**: Proper REST status codes
- **Error Messages**: Descriptive, actionable error text
- **Error Context**: Timestamps and request metadata

### Response Examples
Every endpoint includes multiple examples:
- **Success Responses**: Typical successful operations
- **Error Responses**: Common error scenarios
- **Edge Cases**: Boundary conditions and special cases

## 🚀 Using the Interactive Documentation

### Swagger UI (`/docs`)
- **Try It Out**: Execute API calls directly from the browser
- **Authentication**: API key input for testing
- **Request/Response**: Live request/response inspection
- **Code Generation**: Auto-generated client code samples

### ReDoc (`/redoc`)
- **Clean Layout**: Professional documentation presentation
- **Detailed Schemas**: Comprehensive model documentation
- **Search**: Full-text search across all documentation
- **Export**: Download OpenAPI schema

## 🧪 Testing and Validation

### Built-in Examples
Every endpoint includes working examples based on:
- **Real Genomic Data**: Chromosome 22 examples from AlphaGenome docs
- **Common Variants**: Well-studied genetic variants
- **Multiple Tissues**: Representative tissue types
- **Various Outputs**: Different prediction types

### Validation Features
- **Real-time Validation**: Immediate feedback on invalid inputs
- **Format Checking**: Automatic format validation
- **Range Validation**: Genomic coordinate bounds checking
- **Biological Validation**: Scientifically meaningful parameters

## 📖 Integration Examples

### cURL Commands
```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Variant prediction
curl -X POST "http://localhost:8000/api/v1/predict/variant" \
  -H "Content-Type: application/json" \
  -d '{"interval": {...}, "variant": {...}}'
```

### Python Client
```python
import requests

# Using the API
response = requests.post(
    "http://localhost:8000/api/v1/predict/variant",
    json={"interval": {...}, "variant": {...}}
)
```

### JavaScript/Node.js
```javascript
const response = await fetch('/api/v1/predict/variant', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({interval: {...}, variant: {...}})
});
```

## 🔍 Troubleshooting Documentation

### Common Issues
- **API Key Problems**: Environment variable setup
- **Validation Errors**: Parameter format requirements
- **Performance Issues**: Interval size recommendations
- **Network Errors**: Connection and timeout handling

### Debug Information
- **Request Logging**: Detailed request/response logging
- **Error Codes**: Comprehensive error code reference
- **Status Monitoring**: Health check interpretation

## 📊 Performance Guidelines

### Optimal Usage Patterns
- **Interval Sizes**: Recommendations for different use cases
- **Batch Processing**: Async job usage guidelines
- **Rate Limiting**: Request frequency recommendations
- **Resource Usage**: Memory and processing considerations

### Scaling Considerations
- **Production Deployment**: Docker and orchestration
- **Load Balancing**: Multi-instance deployment
- **Caching**: Response caching strategies
- **Monitoring**: Performance metrics and alerting

## 🔐 Security and Compliance

### API Security
- **API Key Management**: Secure key storage and rotation
- **HTTPS Requirements**: Encrypted communication
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: Abuse prevention

### Data Privacy
- **No Data Storage**: Stateless processing
- **Secure Transmission**: Encrypted data transfer
- **Compliance**: AlphaGenome terms of service adherence

## 📝 Documentation Maintenance

### Version Control
- **API Versioning**: Semantic versioning strategy
- **Documentation Updates**: Synchronized with code changes
- **Backward Compatibility**: Breaking change management

### Quality Assurance
- **Example Validation**: Regular testing of documentation examples
- **Link Checking**: Automated link validation
- **Content Review**: Regular documentation review cycles

## 🌐 External Resources

### AlphaGenome Documentation
- [Official Documentation](https://www.alphagenomedocs.com/)
- [Quick Start Guide](https://www.alphagenomedocs.com/colabs/quick_start.html)
- [API Reference](https://www.alphagenomedocs.com/api/index.html)
- [Terms of Service](https://deepmind.google.com/science/alphagenome/terms)

### OpenAPI/Swagger Resources
- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

This comprehensive Swagger documentation ensures that users have all the information they need to effectively use the AlphaGenome REST API, with detailed biological context and practical examples based on the official AlphaGenome documentation. 