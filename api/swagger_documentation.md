# 🧬 AlphaGenome REST API - Swagger Documentation Guide

This document provides comprehensive information about the AlphaGenome REST API's Swagger/OpenAPI documentation, based on the actual implementation in `simple_server.py`.

## 📚 API Overview

The AlphaGenome REST API provides programmatic access to Google DeepMind's AlphaGenome model through a simple HTTP server built with Python's standard library. The API includes comprehensive Swagger/OpenAPI documentation with:

- **Interactive Documentation**: Auto-generated docs at `/docs` (Swagger UI)
- **OpenAPI Schema**: Machine-readable schema at `/openapi.json`
- **Visualization Capabilities**: Built-in matplotlib-based plot generation
- **Standard Library Implementation**: No FastAPI dependencies, Python 3.13 compatible

## 🎯 Key Features of Our Swagger Documentation

### 1. **Comprehensive Descriptions**
Every endpoint includes detailed descriptions explaining:
- Scientific purpose and biological context
- Clinical and research applications
- Performance considerations and limitations
- Example use cases with real genomic coordinates

### 2. **Rich Examples**
All request/response models include:
- Realistic genomic data (chr22 examples from AlphaGenome docs)
- Multiple tissue types and output modalities
- Expected response formats with statistical summaries
- Visualization examples with base64 image encoding

### 3. **Detailed Parameter Documentation**
Each parameter includes:
- Data type validation (regex patterns for chromosomes, DNA sequences)
- Biological context and UBERON ontology terms
- Required vs optional status with sensible defaults
- Coordinate system specifications (1-based genomic coordinates)

### 4. **Organized Tag Structure**
Endpoints are grouped into logical categories:
- **System**: Health checks and server status
- **Configuration**: Available outputs and tissue ontology
- **Predictions**: Core genomic analysis functionality
- **Visualization**: Publication-quality plot generation

## 🔬 AlphaGenome Model Information

### Supported Output Types

Our implementation supports all AlphaGenome output types through the `dna_client.OutputType` enum:

#### Expression & Transcription
- **RNA_SEQ**: Gene expression levels from RNA sequencing
  - Resolution: Single base-pair predictions
  - Use case: Tissue-specific transcriptional activity
  - Statistical outputs: Mean, std, min, max across interval
- **CAGE**: Cap analysis gene expression (promoter activity)
  - Resolution: Single base-pair predictions
  - Use case: Transcription start site identification

#### Chromatin Accessibility
- **ATAC_SEQ**: Assay for transposase-accessible chromatin
  - Resolution: Single base-pair predictions
  - Use case: Open chromatin and regulatory element mapping
- **DNASE_SEQ**: DNase hypersensitivity sites
  - Resolution: Single base-pair predictions
  - Use case: Regulatory element discovery

#### Chromatin Modifications
- **CHIP_SEQ**: Chromatin immunoprecipitation sequencing
  - Resolution: Single base-pair predictions
  - Use case: Histone modifications and transcription factor binding
- **HiC**: High-throughput chromosome conformation capture
  - Resolution: Variable (depends on distance)
  - Use case: 3D genome organization and chromatin interactions

### Supported Sequence Lengths

The API documentation details AlphaGenome's supported sequence lengths:

- **2KB** (`SEQUENCE_LENGTH_2KB`): Promoter regions and small regulatory elements
- **16KB** (`SEQUENCE_LENGTH_16KB`): Gene loci with proximal regulatory elements
- **100KB** (`SEQUENCE_LENGTH_100KB`): Large regulatory domains and gene clusters
- **500KB** (`SEQUENCE_LENGTH_500KB`): Topologically associating domains (TADs)
- **1MB** (`SEQUENCE_LENGTH_1MB`): Large chromosomal segments and multi-gene regions

### Tissue Ontology Terms

Comprehensive tissue coverage with UBERON ontology terms (hardcoded in implementation):

#### Available Tissues
- **UBERON:0001157**: Colon - Transverse (default for many examples)
- **UBERON:0001114**: Right liver lobe (CYP2B6 drug metabolism examples)
- **UBERON:0002048**: Lung (respiratory system analysis)
- **UBERON:0000948**: Heart (cardiovascular genomics)
- **UBERON:0000955**: Brain (neurogenomics applications)
- **UBERON:0002113**: Kidney (renal disease genetics)

## 📋 Endpoint Documentation Details

### System Endpoints

#### `GET /health`
- **Implementation**: `_handle_health()` method
- **Purpose**: Server health check and AlphaGenome client verification
- **Response**: JSON with server status and client initialization state
- **Use Cases**: Monitoring, troubleshooting, capability verification
- **Technical Details**: Calls `initialize_alphagenome()` to verify client status

#### `GET /` and `GET /docs`
- **Implementation**: `_handle_docs()` method serving `get_swagger_html()`
- **Purpose**: Interactive Swagger UI documentation
- **Features**: 
  - Swagger UI 5.10.5 with modern styling
  - Try-it-out functionality for all endpoints
  - Automatic OpenAPI spec loading from `/openapi.json`

#### `GET /openapi.json`
- **Implementation**: `_handle_openapi()` method serving `get_openapi_spec()`
- **Purpose**: Complete OpenAPI 3.0 specification
- **Content**: 1000+ line comprehensive API specification with examples

### Configuration Endpoints

#### `GET /api/v1/outputs`
- **Implementation**: `_handle_outputs()` method
- **AlphaGenome Integration**: Uses `dna_client.OutputType` enum
- **Response**: List of all supported genomic output types
- **Error Handling**: Graceful fallback if AlphaGenome SDK unavailable

#### `GET /api/v1/tissues`
- **Implementation**: `_handle_tissues()` method
- **Data Source**: Hardcoded UBERON ontology terms dictionary
- **Response**: Tissue ID to human-readable name mapping
- **Use Case**: Populate tissue selection interfaces

### Prediction Endpoints

#### `POST /api/v1/predict/interval`
- **Implementation**: `_handle_predict_interval()` method
- **AlphaGenome Integration**: 
  - Creates `genome.Interval` objects from request data
  - Converts output names to `dna_client.OutputType` enums
  - Calls `client.predict_interval()` with proper parameters
- **Response Processing**:
  - Extracts `.values` arrays from AlphaGenome response objects
  - Calculates statistical summaries (mean, std, min, max, shape)
  - Returns structured JSON with metadata
- **Error Handling**: Comprehensive exception handling with detailed error messages

#### `POST /api/v1/predict/variant`
- **Implementation**: `_handle_predict_variant()` method
- **AlphaGenome Integration**:
  - Creates `genome.Interval` and `genome.Variant` objects
  - Calls `client.predict_variant()` for REF vs ALT comparison
- **Effect Analysis**:
  - Compares reference and alternate predictions
  - Calculates mean differences and effect directions
  - Determines increase/decrease/no_change classifications
- **Response Structure**: Nested variant_effects with reference/alternate/effect data

### Visualization Endpoints

#### `POST /api/v1/visualize/tracks`
- **Implementation**: `_handle_visualize_tracks()` method using `create_visualization()`
- **Visualization Engine**: Matplotlib with 'Agg' backend (non-interactive)
- **Plot Features**:
  - Multi-track genomic plots with aligned x-axes
  - Professional color schemes (#1f77b4, #ff7f0e, etc.)
  - Statistical annotations in legends (mean ± std)
  - Grid overlays and proper axis labeling
- **Output Format**: Base64 encoded PNG at 150 DPI resolution

#### `POST /api/v1/visualize/variant`
- **Implementation**: `_handle_visualize_variant()` method
- **Plot Type**: Side-by-side bar charts comparing REF vs ALT
- **Visual Features**:
  - Effect direction arrows (↑ increase, ↓ decrease, → no change)
  - Color coding (blue for REF, orange for ALT)
  - Statistical annotations and error bars
- **Interpretation**: Green/red/gray arrows indicate functional impact

#### `POST /api/v1/visualize/summary`
- **Implementation**: `_handle_visualize_summary()` method
- **Plot Type**: Statistical summary bar charts with error bars
- **Features**:
  - Mean values as bar heights
  - Standard deviation error bars
  - Quantitative value labels on bars
  - Rotated x-axis labels for readability

## 🔧 Technical Implementation Details

### HTTP Server Architecture
- **Base Class**: `BaseHTTPRequestHandler` from Python standard library
- **CORS Support**: Built-in cross-origin resource sharing headers
- **JSON Handling**: Manual JSON parsing and response generation
- **Error Handling**: Structured error responses with HTTP status codes

### AlphaGenome Client Management
- **Initialization**: Global client variable with lazy initialization
- **API Key**: Retrieved via `get_api_key()` from `load_env_helper.py`
- **Error Recovery**: Graceful degradation when client unavailable
- **Startup Verification**: Client initialization attempted at server startup

### Visualization Pipeline
- **Library**: Matplotlib with Agg backend for server environments
- **Image Processing**: PIL/base64 encoding for web delivery
- **Plot Styling**: Professional genomics color schemes and layouts
- **Error Handling**: Fallback text plots when visualization fails

### Data Validation
- **Genomic Coordinates**: 1-based coordinate system validation
- **Chromosome Format**: Regex pattern matching (chr1-22, X, Y, MT)
- **DNA Sequences**: ACGT base validation for variant sequences
- **Interval Logic**: Start < End validation with length constraints

## 🧪 Example Usage and Testing

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
# Response includes AlphaGenome client status
```

### Genomic Interval Prediction
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

### Variant Effect Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/predict/variant" \
  -H "Content-Type: application/json" \
  -d '{
    "interval": {
      "chromosome": "chr22",
      "start": 35677410,
      "end": 36725986
    },
    "variant": {
      "chromosome": "chr22",
      "position": 36201698,
      "reference_bases": "A",
      "alternate_bases": "C"
    },
    "ontology_terms": ["UBERON:0001157"],
    "requested_outputs": ["RNA_SEQ"]
  }'
```

### Visualization Generation
```bash
curl -X POST "http://localhost:8000/api/v1/visualize/tracks" \
  -H "Content-Type: application/json" \
  -d '{
    "prediction_data": {
      "predictions": {
        "RNA_SEQ": {"shape": [1048576, 3], "mean": 0.45, "std": 0.23}
      }
    },
    "title": "CYP2B6 Regulatory Landscape"
  }'
```

## 🚀 Swagger UI Features

### Interactive Testing
- **Try It Out**: Execute API calls directly from documentation
- **Parameter Input**: Form-based parameter entry with validation
- **Response Display**: Formatted JSON responses with syntax highlighting
- **Error Visualization**: Clear error message display with HTTP status codes

### Documentation Navigation
- **Tag Grouping**: Logical endpoint organization
- **Search Functionality**: Built-in documentation search
- **Model Exploration**: Expandable schema definitions
- **Example Values**: Pre-populated realistic examples

### Code Generation
- **Multiple Languages**: cURL, Python, JavaScript examples
- **Client Libraries**: Auto-generated client code snippets
- **Authentication**: API key parameter handling

## 📊 Performance and Limitations

### Scaling Considerations
- **Single-threaded**: Standard library HTTP server (not production-ready)
- **Memory Usage**: Large genomic intervals may require significant RAM
- **Processing Time**: 1MB intervals can take several minutes
- **Rate Limiting**: No built-in rate limiting (add via nginx)

### Production Deployment
- **Docker Container**: Included Dockerfile with Python 3.11
- **Nginx Proxy**: Production-ready reverse proxy configuration
- **Health Checks**: Docker health check integration
- **Logging**: Python logging with configurable levels

## 🔐 Security and Compliance

### API Security
- **CORS Headers**: Configurable cross-origin access
- **Input Validation**: Comprehensive parameter validation
- **Error Handling**: No sensitive information in error messages
- **API Key Protection**: Environment variable storage

### Data Privacy
- **Stateless Processing**: No data persistence or logging
- **Memory Management**: Automatic garbage collection
- **Secure Communication**: HTTPS support via nginx
- **Compliance**: AlphaGenome terms of service adherence

## 📝 Documentation Maintenance

### Version Control
- **OpenAPI 3.0**: Modern specification format
- **Semantic Versioning**: API version 1.0.0
- **Schema Evolution**: Backward compatibility considerations
- **Example Updates**: Regular testing of documentation examples

### Quality Assurance
- **Automated Testing**: GitHub Actions CI/CD pipeline
- **Link Validation**: Automated documentation link checking
- **Example Verification**: Regular testing of all code examples
- **User Feedback**: Documentation improvement based on user reports

## 🌐 External Resources

### AlphaGenome Documentation
- [Official Documentation](https://www.alphagenomedocs.com/)
- [Quick Start Guide](https://www.alphagenomedocs.com/colabs/quick_start.html)
- [Essential Commands](https://www.alphagenomedocs.com/colabs/essential_commands.html)
- [Installation Guide](https://www.alphagenomedocs.com/installation.html)

### API Standards
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

### Genomics Resources
- [UBERON Ontology](http://uberon.github.io/)
- [Human Genome Reference](https://www.ncbi.nlm.nih.gov/grc/human)
- [Genomic Coordinate Systems](https://genome.ucsc.edu/FAQ/FAQtracks.html#tracks1)

This comprehensive Swagger documentation ensures that users have complete information about the AlphaGenome REST API implementation, with detailed technical specifications, biological context, and practical examples for effective genomic analysis. 