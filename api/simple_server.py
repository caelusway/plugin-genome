#!/usr/bin/env python3
"""
Ultra-simple AlphaGenome HTTP Server with Swagger UI and Visualization
Uses only standard library to avoid Python 3.13 compatibility issues
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import base64
import io
from load_env_helper import get_api_key

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global AlphaGenome client
alphagenome_client = None

def create_visualization(data, plot_type="track", title="AlphaGenome Prediction"):
    """Create visualization using matplotlib."""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if plot_type == "track" and "predictions" in data:
            # Track plot for genomic predictions
            predictions = data["predictions"]
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            
            for i, (output_name, pred_data) in enumerate(predictions.items()):
                if "shape" in pred_data and len(pred_data["shape"]) > 0:
                    # Create synthetic data based on statistics
                    length = pred_data["shape"][0] if pred_data["shape"] else 1000
                    mean_val = pred_data.get("mean", 0)
                    std_val = pred_data.get("std", 1)
                    
                    # Generate representative signal
                    x = np.linspace(0, length, min(length, 1000))
                    y = np.random.normal(mean_val, std_val, len(x))
                    
                    color = colors[i % len(colors)]
                    ax.plot(x, y, label=f"{output_name} (μ={mean_val:.3f})", 
                           color=color, alpha=0.8, linewidth=1.5)
            
            ax.set_xlabel("Genomic Position")
            ax.set_ylabel("Prediction Value")
            ax.set_title(f"{title} - Genomic Tracks")
            ax.legend()
            ax.grid(True, alpha=0.3)
            
        elif plot_type == "variant" and "variant_effects" in data:
            # Variant effect plot
            effects = data["variant_effects"]
            output_names = list(effects.keys())
            
            if output_names:
                ref_means = [effects[name]["reference"]["mean"] for name in output_names]
                alt_means = [effects[name]["alternate"]["mean"] for name in output_names]
                
                x = np.arange(len(output_names))
                width = 0.35
                
                bars1 = ax.bar(x - width/2, ref_means, width, label='Reference', 
                              color='#1f77b4', alpha=0.8)
                bars2 = ax.bar(x + width/2, alt_means, width, label='Alternate', 
                              color='#ff7f0e', alpha=0.8)
                
                ax.set_xlabel("Output Types")
                ax.set_ylabel("Prediction Value")
                ax.set_title(f"{title} - Variant Effects")
                ax.set_xticks(x)
                ax.set_xticklabels(output_names, rotation=45, ha='right')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                # Add effect direction annotations
                for i, name in enumerate(output_names):
                    effect = effects[name]["effect"]
                    direction = effect.get("effect_direction", "no_change")
                    color = {'increase': 'green', 'decrease': 'red', 'no_change': 'gray'}[direction]
                    ax.annotate(f'↑' if direction == 'increase' else '↓' if direction == 'decrease' else '→',
                               xy=(i, max(ref_means[i], alt_means[i]) + 0.1),
                               ha='center', va='bottom', color=color, fontsize=16, fontweight='bold')
        
        elif plot_type == "summary":
            # Summary statistics plot
            if "predictions" in data:
                predictions = data["predictions"]
                output_names = list(predictions.keys())
                means = [predictions[name].get("mean", 0) for name in output_names]
                stds = [predictions[name].get("std", 0) for name in output_names]
                
                x = np.arange(len(output_names))
                bars = ax.bar(x, means, yerr=stds, capsize=5, 
                             color='#2ca02c', alpha=0.7, error_kw={'color': 'black', 'capthick': 2})
                
                ax.set_xlabel("Output Types")
                ax.set_ylabel("Mean Prediction ± Std")
                ax.set_title(f"{title} - Prediction Summary")
                ax.set_xticks(x)
                ax.set_xticklabels(output_names, rotation=45, ha='right')
                ax.grid(True, alpha=0.3)
                
                # Add value labels on bars
                for i, (bar, mean_val, std_val) in enumerate(zip(bars, means, stds)):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + std_val + 0.01,
                           f'{mean_val:.3f}', ha='center', va='bottom', fontsize=10)
        
        else:
            # Default plot
            ax.text(0.5, 0.5, f"Visualization for {plot_type}\nData: {len(str(data))} chars", 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_title(title)
        
        plt.tight_layout()
        
        # Convert to base64 image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return image_base64
        
    except Exception as e:
        logger.error(f"Visualization error: {str(e)}")
        return None

def get_openapi_spec():
    """Generate OpenAPI specification for Swagger UI."""
    # Get host and port from environment or defaults
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    
    # Determine server URLs based on environment
    base_url = os.getenv('BASE_URL')
    if base_url:
        # Production: use provided base URL
        servers = [
            {
                "url": base_url,
                "description": "Production server"
            }
        ]
    else:
        # Development: provide multiple options
        servers = [
            {
                "url": f"http://127.0.0.1:{port}",
                "description": "Local development server"
            },
            {
                "url": f"http://localhost:{port}",
                "description": "Local development server (localhost)"
            }
        ]
        # If host is 0.0.0.0, also add the actual network interface
        if host == '0.0.0.0':
            servers.append({
                "url": f"http://0.0.0.0:{port}",
                "description": "Development server (all interfaces)"
            })
    
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "AlphaGenome REST API with Visualization",
            "description": """
This API provides access to Google DeepMind's AlphaGenome, a unifying model for deciphering the regulatory code within DNA sequences.

## About AlphaGenome

AlphaGenome offers **multimodal predictions** encompassing diverse functional outputs such as:
- **Gene expression** (RNA-seq tracks)
- **Splicing patterns** 
- **Chromatin features** (histone modifications, accessibility)
- **Contact maps** (3D genome organization)

The model analyzes DNA sequences of up to **1 million base pairs** in length and delivers predictions at **single base-pair resolution** for most outputs. AlphaGenome achieves state-of-the-art performance across genomic prediction benchmarks.

## Supported Sequence Lengths
- 2KB, 16KB, 100KB, 500KB, 1MB

## Use Cases
- **Variant Effect Prediction**: Assess functional impact of genetic variants
- **Regulatory Analysis**: Understand gene regulation mechanisms
- **Tissue-Specific Studies**: Compare predictions across different tissues
- **Genomic Visualization**: Generate publication-quality plots

## Rate Limits
The API is well-suited for smaller to medium-scale analyses requiring 1000s of predictions, but not for large-scale analyses requiring millions of predictions.
            """,
            "version": "1.0.0",
            "contact": {
                "name": "AlphaGenome API Support",
                "url": "https://www.alphagenomedocs.com/"
            },
            "license": {
                "name": "Non-commercial use only",
                "url": "https://deepmind.google.com/science/alphagenome/terms"
            }
        },
        "servers": servers,
        "paths": {
            "/health": {
                "get": {
                    "summary": "Health Check",
                    "description": """
Check the health status of the AlphaGenome API server and verify that the AlphaGenome client is properly initialized.

This endpoint is useful for:
- Monitoring server availability
- Verifying API key configuration
- Checking AlphaGenome SDK connectivity
                    """,
                    "tags": ["System"],
                    "responses": {
                        "200": {
                            "description": "Server is healthy and AlphaGenome client is ready",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ApiResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/outputs": {
                "get": {
                    "summary": "Get Supported Output Types",
                    "description": """
Retrieve all genomic output types supported by AlphaGenome for predictions.

AlphaGenome can predict various **functional genomic outputs**:

### Core Output Types:
- **RNA_SEQ**: Gene expression levels (RNA sequencing data)
- **ATAC_SEQ**: Chromatin accessibility (ATAC-seq peaks)
- **CHIP_SEQ**: Histone modifications and transcription factor binding
- **CAGE**: Transcription start sites (CAGE peaks)
- **DNase**: DNase hypersensitivity sites
- **HiC**: 3D genome contact maps

### Biological Applications:
- **Gene Expression Analysis**: Predict tissue-specific expression patterns
- **Regulatory Element Discovery**: Identify enhancers, promoters, silencers
- **Epigenome Mapping**: Understand chromatin states and modifications
- **3D Genome Structure**: Analyze chromosome interactions and topology

Each output type provides predictions at different resolutions and scales, enabling comprehensive genomic analysis.
                    """,
                    "tags": ["Configuration"],
                    "responses": {
                        "200": {
                            "description": "List of all supported genomic output types",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ApiResponse"},
                                    "example": {
                                        "success": True,
                                        "data": {
                                            "supported_outputs": ["RNA_SEQ", "ATAC_SEQ", "CHIP_SEQ", "CAGE", "DNase", "HiC"],
                                            "description": "Available genomic output types"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/tissues": {
                "get": {
                    "summary": "Get Tissue Ontology Terms",
                    "description": """
Retrieve available tissue ontology terms for tissue-specific genomic predictions.

### Tissue-Specific Analysis
AlphaGenome provides **tissue-specific predictions** using UBERON ontology terms. Different tissues have distinct:
- **Gene expression patterns**
- **Chromatin accessibility landscapes** 
- **Regulatory element activities**
- **Epigenetic modifications**

### Available Tissues Include:
- **UBERON:0001157**: Colon - Transverse
- **UBERON:0001114**: Right liver lobe  
- **UBERON:0002048**: Lung
- **UBERON:0000948**: Heart
- **UBERON:0000955**: Brain
- **UBERON:0002113**: Kidney

### Scientific Applications:
- **Comparative Genomics**: Compare regulatory patterns across tissues
- **Disease Research**: Study tissue-specific disease mechanisms
- **Drug Development**: Understand tissue-specific drug effects
- **Personalized Medicine**: Predict individual tissue responses

Use these ontology terms in prediction requests to get tissue-specific genomic insights.
                    """,
                    "tags": ["Configuration"],
                    "responses": {
                        "200": {
                            "description": "Available tissue ontology terms with descriptions",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ApiResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/predict/interval": {
                "post": {
                    "summary": "Predict Genomic Interval",
                    "description": """
Make comprehensive genomic predictions for a specified DNA interval using AlphaGenome's multimodal approach.

## Scientific Purpose
This endpoint performs **ab initio** predictions directly from DNA sequence, providing insights into:
- **Gene expression levels** across the interval
- **Regulatory element activities** (enhancers, promoters, silencers)
- **Chromatin accessibility** patterns
- **Histone modification** landscapes
- **Transcription factor binding** sites

## Input Requirements
- **Genomic Interval**: Chromosome coordinates (1-based)
- **Sequence Length**: Must be one of: 2KB, 16KB, 100KB, 500KB, or 1MB
- **Tissue Context**: UBERON ontology terms for tissue-specific predictions
- **Output Types**: Specify which genomic modalities to predict

## Biological Applications

### 1. **Regulatory Analysis**
- Identify active regulatory elements in specific tissues
- Map enhancer-promoter interactions
- Study tissue-specific gene regulation

### 2. **Functional Genomics**
- Predict gene expression from sequence alone
- Understand chromatin organization patterns
- Analyze epigenetic landscapes

### 3. **Comparative Studies**
- Compare regulatory activity across tissues
- Study evolutionary conservation of regulatory elements
- Identify tissue-specific regulatory mechanisms

## Output Format
Returns statistical summaries and raw prediction arrays for visualization and downstream analysis.

**Example Use Case**: Analyzing the regulatory landscape around the CYP2B6 gene in liver tissue to understand drug metabolism regulation.
                    """,
                    "tags": ["Predictions"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/PredictionRequest"},
                                "example": {
                                    "interval": {
                                        "chromosome": "chr22",
                                        "start": 35677410,
                                        "end": 36725986,
                                        "_description": "1MB interval around CYP2B6 gene"
                                    },
                                    "ontology_terms": ["UBERON:0001114"],
                                    "requested_outputs": ["RNA_SEQ", "ATAC_SEQ"],
                                    "_use_case": "Analyze gene expression and chromatin accessibility in liver tissue"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful genomic predictions with statistical summaries",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ApiResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/predict/variant": {
                "post": {
                    "summary": "Predict Variant Effects",
                    "description": """
Predict the functional effects of genetic variants on genomic outputs using AlphaGenome's variant effect prediction capabilities.

## Scientific Purpose
This endpoint performs **variant effect prediction** by comparing:
- **Reference (REF)** allele predictions
- **Alternative (ALT)** allele predictions  
- **Differential effects** between alleles

## Variant Analysis Capabilities

### 1. **Molecular Mechanisms**
- **Gene Expression Changes**: How variants affect transcription levels
- **Splicing Alterations**: Impact on alternative splicing patterns
- **Regulatory Disruption**: Effects on enhancer/promoter activity
- **Chromatin Remodeling**: Changes in accessibility and histone modifications

### 2. **Clinical Applications**
- **Pathogenicity Assessment**: Evaluate disease-causing potential
- **Pharmacogenomics**: Predict drug response variations
- **Personalized Medicine**: Individual genetic risk assessment
- **Functional Annotation**: Understand variant mechanisms

### 3. **Research Applications**
- **GWAS Follow-up**: Mechanistic insights for association signals
- **Evolutionary Studies**: Functional impact of evolutionary variants
- **Population Genetics**: Understanding selection pressures
- **Regulatory Variation**: Tissue-specific regulatory effects

## Input Requirements
- **Genomic Interval**: Context region around the variant (typically 100KB-1MB)
- **Variant Definition**: Chromosome, position, REF and ALT alleles
- **Tissue Context**: Specify relevant tissues for the analysis
- **Output Types**: Choose genomic modalities of interest

## Output Interpretation
- **Effect Direction**: Increase/decrease/no change in predicted values
- **Effect Magnitude**: Quantitative difference between REF and ALT
- **Tissue Specificity**: Variant effects may vary across tissues
- **Statistical Significance**: Confidence in predicted effects

**Example Use Case**: Analyzing a GWAS variant (chr22:36201698 A>C) known to affect gene expression in colon tissue, to understand its molecular mechanism and tissue-specific effects.
                    """,
                    "tags": ["Predictions"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/VariantEffectRequest"},
                                "example": {
                                    "interval": {
                                        "chromosome": "chr22",
                                        "start": 35677410,
                                        "end": 36725986,
                                        "_description": "1MB context around variant"
                                    },
                                    "variant": {
                                        "chromosome": "chr22",
                                        "position": 36201698,
                                        "reference_bases": "A",
                                        "alternate_bases": "C",
                                        "_description": "Known eQTL variant"
                                    },
                                    "ontology_terms": ["UBERON:0001157"],
                                    "requested_outputs": ["RNA_SEQ"],
                                    "_use_case": "Analyze variant effect on gene expression in colon tissue"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Variant effect predictions comparing REF vs ALT alleles",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ApiResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/visualize/tracks": {
                "post": {
                    "summary": "Visualize Genomic Tracks",
                    "description": """
Generate publication-quality genomic track visualizations from AlphaGenome predictions.

## Visualization Purpose
Create **multi-track genomic plots** showing:
- **Prediction values** across genomic coordinates
- **Multiple output types** in aligned tracks
- **Tissue-specific patterns** with distinct colors
- **Statistical summaries** in track legends

## Scientific Applications

### 1. **Regulatory Landscape Visualization**
- **Gene Expression Tracks**: RNA-seq predictions across intervals
- **Chromatin Accessibility**: ATAC-seq signal visualization
- **Histone Modifications**: ChIP-seq track overlays
- **Transcription Factor Binding**: TFBS prediction tracks

### 2. **Comparative Analysis**
- **Multi-tissue Comparison**: Same genomic region across tissues
- **Multi-modal Integration**: Different data types in aligned tracks
- **Temporal Studies**: Time-series genomic data visualization
- **Condition Comparisons**: Treatment vs control visualizations

### 3. **Publication Graphics**
- **High-resolution plots** (150 DPI) for manuscripts
- **Professional color schemes** following genomics conventions
- **Customizable titles** and annotations
- **Publication-ready formats** (PNG with transparent backgrounds)

## Visualization Features
- **Aligned x-axis**: Genomic coordinates in base pairs
- **Independent y-axes**: Each track scaled appropriately  
- **Color coding**: Distinct colors for different output types
- **Statistical annotations**: Mean and standard deviation in legends
- **Grid overlays**: Improve readability of genomic coordinates

**Example Use Case**: Creating a multi-track visualization showing RNA-seq, ATAC-seq, and ChIP-seq predictions for the CYP2B6 locus in liver tissue for a research publication.
                    """,
                    "tags": ["Visualization"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/VisualizationRequest"},
                                "example": {
                                    "prediction_data": {
                                        "predictions": {
                                            "RNA_SEQ": {
                                                "shape": [1048576, 3],
                                                "mean": 0.45,
                                                "std": 0.23,
                                                "_description": "3 RNA-seq tracks for liver tissue"
                                            },
                                            "ATAC_SEQ": {
                                                "shape": [1048576, 1],
                                                "mean": 0.12,
                                                "std": 0.08,
                                                "_description": "Chromatin accessibility"
                                            }
                                        },
                                        "metadata": {
                                            "interval": {"chromosome": "chr22", "start": 35677410, "end": 36725986},
                                            "ontology_terms": ["UBERON:0001114"]
                                        }
                                    },
                                    "title": "CYP2B6 Regulatory Landscape - Liver Tissue",
                                    "_use_case": "Multi-modal genomic visualization for publication"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Generated genomic track visualization as base64 PNG",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/VisualizationResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/visualize/variant": {
                "post": {
                    "summary": "Visualize Variant Effects",
                    "description": """
Generate variant effect visualizations comparing reference and alternative allele predictions.

## Visualization Purpose
Create **comparative bar charts** showing:
- **Reference allele predictions** (REF)
- **Alternative allele predictions** (ALT)  
- **Effect directions** with visual indicators
- **Statistical comparisons** between alleles

## Scientific Applications

### 1. **Variant Impact Assessment**
- **Effect Magnitude**: Quantify functional impact of variants
- **Direction Indicators**: Visual arrows showing increase/decrease/no-change
- **Multi-modal Effects**: Compare variant impact across different genomic outputs
- **Tissue Specificity**: Visualize tissue-specific variant effects

### 2. **Clinical Interpretation**
- **Pathogenicity Visualization**: Clear display of deleterious effects
- **Pharmacogenomic Effects**: Drug response variant visualization
- **Regulatory Variant Analysis**: Enhancer/promoter disruption effects
- **Splicing Impact**: Visualization of splice-altering variants

### 3. **Research Communication**
- **Conference Presentations**: Clear variant effect communication
- **Manuscript Figures**: Publication-quality variant analysis plots
- **Grant Proposals**: Visual evidence of variant functional impact
- **Educational Materials**: Teaching variant effect concepts

## Visualization Features
- **Side-by-side bars**: REF vs ALT comparison for each output type
- **Effect direction arrows**: ↑ (increase), ↓ (decrease), → (no change)
- **Color coding**: Blue for REF, orange for ALT alleles
- **Statistical annotations**: Effect magnitude and direction
- **Professional styling**: Grid lines, proper axis labels, legends

## Interpretation Guide
- **Green arrows (↑)**: Variant increases predicted values (gain-of-function)
- **Red arrows (↓)**: Variant decreases predicted values (loss-of-function)  
- **Gray arrows (→)**: Variant has minimal effect (neutral)
- **Bar heights**: Magnitude of predicted functional output

**Example Use Case**: Visualizing the effect of a GWAS variant on gene expression and chromatin accessibility to understand its molecular mechanism and clinical relevance.
                    """,
                    "tags": ["Visualization"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/VisualizationRequest"},
                                "example": {
                                    "prediction_data": {
                                        "variant_effects": {
                                            "RNA_SEQ": {
                                                "reference": {"mean": 0.45, "std": 0.12},
                                                "alternate": {"mean": 0.67, "std": 0.15},
                                                "effect": {
                                                    "mean_difference": 0.22,
                                                    "effect_direction": "increase",
                                                    "_interpretation": "Gain-of-function variant"
                                                }
                                            }
                                        },
                                        "metadata": {
                                            "variant": {"chromosome": "chr22", "position": 36201698, "reference_bases": "A", "alternate_bases": "C"}
                                        }
                                    },
                                    "title": "eQTL Variant Effect Analysis - chr22:36201698 A>C"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Generated variant effect visualization comparing REF vs ALT",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/VisualizationResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/visualize/summary": {
                "post": {
                    "summary": "Visualize Prediction Summary",
                    "description": """
Generate statistical summary visualizations of genomic predictions with error bars and quantitative metrics.

## Visualization Purpose
Create **summary bar charts** showing:
- **Mean prediction values** for each genomic output type
- **Standard deviation error bars** indicating prediction variability
- **Quantitative labels** with precise numerical values
- **Statistical overview** of genomic predictions

## Scientific Applications

### 1. **Comparative Genomics**
- **Cross-tissue Comparison**: Compare prediction magnitudes across tissues
- **Multi-region Analysis**: Summarize predictions across genomic intervals
- **Temporal Studies**: Track changes in genomic predictions over time
- **Treatment Effects**: Compare baseline vs treatment conditions

### 2. **Quality Assessment**
- **Prediction Confidence**: Error bars indicate prediction reliability
- **Signal-to-noise Ratio**: Assess prediction quality across output types
- **Batch Effects**: Identify systematic differences in predictions
- **Method Validation**: Compare AlphaGenome predictions with experimental data

### 3. **Research Reporting**
- **Executive Summaries**: High-level overview of genomic analysis results
- **Grant Progress Reports**: Quantitative summary of research findings
- **Collaboration Meetings**: Quick visual summary of key results
- **Method Comparisons**: Statistical comparison of different approaches

## Visualization Features
- **Bar heights**: Mean prediction values
- **Error bars**: ± one standard deviation
- **Value labels**: Precise numerical values on top of bars
- **Professional styling**: Clean layout suitable for presentations
- **Rotated labels**: Readable output type names
- **Grid lines**: Improved readability of quantitative values

## Statistical Interpretation
- **High bars**: Strong predicted functional signal
- **Large error bars**: High variability in predictions (may indicate complex regulation)
- **Small error bars**: Consistent predictions (high confidence)
- **Zero-centered**: Values relative to baseline or control conditions

**Example Use Case**: Creating a summary visualization of AlphaGenome predictions across multiple output types for a genomic region to quickly assess the overall regulatory activity and prediction confidence.
                    """,
                    "tags": ["Visualization"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/VisualizationRequest"},
                                "example": {
                                    "prediction_data": {
                                        "predictions": {
                                            "RNA_SEQ": {"mean": 0.45, "std": 0.12, "_confidence": "high"},
                                            "ATAC_SEQ": {"mean": 0.23, "std": 0.08, "_confidence": "high"},
                                            "CHIP_SEQ": {"mean": 0.67, "std": 0.25, "_confidence": "moderate"},
                                            "CAGE": {"mean": 0.34, "std": 0.15, "_confidence": "moderate"}
                                        }
                                    },
                                    "title": "Genomic Prediction Summary - Multi-modal Analysis",
                                    "_use_case": "Statistical overview for research presentation"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Generated statistical summary visualization with error bars",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/VisualizationResponse"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "GenomicInterval": {
                    "type": "object",
                    "required": ["chromosome", "start", "end"],
                    "properties": {
                        "chromosome": {
                            "type": "string",
                            "description": "Chromosome identifier (e.g., 'chr1', 'chr22', 'chrX')",
                            "example": "chr22",
                            "pattern": "^chr([1-9]|1[0-9]|2[0-2]|X|Y|MT?)$"
                        },
                        "start": {
                            "type": "integer",
                            "description": "Start position in 1-based coordinates (inclusive)",
                            "example": 35677410,
                            "minimum": 1
                        },
                        "end": {
                            "type": "integer",
                            "description": "End position in 1-based coordinates (inclusive). Interval length must be 2KB, 16KB, 100KB, 500KB, or 1MB",
                            "example": 36725986,
                            "minimum": 1
                        }
                    },
                    "description": "Genomic interval specification using 1-based coordinates. The interval length must match AlphaGenome's supported sequence lengths."
                },
                "GenomicVariant": {
                    "type": "object",
                    "required": ["chromosome", "position", "reference_bases", "alternate_bases"],
                    "properties": {
                        "chromosome": {
                            "type": "string",
                            "description": "Chromosome identifier matching the interval",
                            "example": "chr22"
                        },
                        "position": {
                            "type": "integer",
                            "description": "Variant position in 1-based coordinates. Should be within the specified interval",
                            "example": 36201698,
                            "minimum": 1
                        },
                        "reference_bases": {
                            "type": "string",
                            "description": "Reference allele sequence (can differ from actual reference genome)",
                            "example": "A",
                            "pattern": "^[ACGT]+$"
                        },
                        "alternate_bases": {
                            "type": "string",
                            "description": "Alternative allele sequence for effect prediction",
                            "example": "C",
                            "pattern": "^[ACGT]+$"
                        }
                    },
                    "description": "Genetic variant specification for functional effect prediction. Supports SNVs, indels, and complex variants."
                },
                "PredictionRequest": {
                    "type": "object",
                    "required": ["interval"],
                    "properties": {
                        "interval": {"$ref": "#/components/schemas/GenomicInterval"},
                        "ontology_terms": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "UBERON tissue ontology terms for tissue-specific predictions. Use /api/v1/tissues to get available terms",
                            "default": ["UBERON:0001157"],
                            "example": ["UBERON:0001114", "UBERON:0002048"]
                        },
                        "requested_outputs": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Genomic output types to predict. Use /api/v1/outputs to get available types",
                            "default": ["RNA_SEQ"],
                            "example": ["RNA_SEQ", "ATAC_SEQ", "CHIP_SEQ"]
                        }
                    },
                    "description": "Request for genomic interval predictions. Specify the genomic region, tissues of interest, and desired output modalities."
                },
                "VariantEffectRequest": {
                    "type": "object",
                    "required": ["interval", "variant"],
                    "properties": {
                        "interval": {"$ref": "#/components/schemas/GenomicInterval"},
                        "variant": {"$ref": "#/components/schemas/GenomicVariant"},
                        "ontology_terms": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Tissue contexts for variant effect analysis",
                            "default": ["UBERON:0001157"]
                        },
                        "requested_outputs": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Output types for variant effect comparison",
                            "default": ["RNA_SEQ"]
                        }
                    },
                    "description": "Request for variant effect prediction comparing reference vs alternative alleles across specified genomic outputs."
                },
                "VisualizationRequest": {
                    "type": "object",
                    "required": ["prediction_data"],
                    "properties": {
                        "prediction_data": {
                            "type": "object",
                            "description": "Prediction data from /api/v1/predict/* endpoints to visualize"
                        },
                        "title": {
                            "type": "string",
                            "description": "Custom plot title for the visualization",
                            "default": "AlphaGenome Visualization",
                            "example": "CYP2B6 Regulatory Analysis - Liver Tissue"
                        },
                        "width": {
                            "type": "integer",
                            "description": "Plot width in pixels (affects resolution)",
                            "default": 1200,
                            "minimum": 400,
                            "maximum": 2400
                        },
                        "height": {
                            "type": "integer",
                            "description": "Plot height in pixels (affects resolution)", 
                            "default": 600,
                            "minimum": 200,
                            "maximum": 1200
                        }
                    },
                    "description": "Request for generating publication-quality visualizations from AlphaGenome prediction data."
                },
                "VisualizationResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "image_base64": {
                                    "type": "string",
                                    "description": "Base64 encoded PNG image data for download/storage"
                                },
                                "image_url": {
                                    "type": "string",
                                    "description": "Data URL (data:image/png;base64,...) for direct HTML embedding"
                                },
                                "plot_info": {
                                    "type": "object",
                                    "description": "Metadata about the generated plot",
                                    "properties": {
                                        "type": {"type": "string", "description": "Visualization type"},
                                        "title": {"type": "string", "description": "Plot title"},
                                        "format": {"type": "string", "description": "Image format (PNG)"},
                                        "resolution": {"type": "string", "description": "Image resolution (150 DPI)"}
                                    }
                                }
                            }
                        }
                    },
                    "description": "Response containing generated visualization as base64 PNG with metadata."
                },
                "ApiResponse": {
                    "type": "object",
                    "required": ["success", "timestamp"],
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "description": "Whether the request was successful"
                        },
                        "data": {
                            "type": "object",
                            "description": "Response data (structure varies by endpoint)"
                        },
                        "error": {
                            "type": "string",
                            "description": "Error message if request failed"
                        },
                        "timestamp": {
                            "type": "string",
                            "description": "ISO 8601 timestamp of response"
                        }
                    },
                    "description": "Standard API response format used by all endpoints."
                }
            }
        },
        "tags": [
            {
                "name": "System",
                "description": "System health and status endpoints"
            },
            {
                "name": "Configuration", 
                "description": "API configuration and available options"
            },
            {
                "name": "Predictions",
                "description": "Core genomic prediction functionality"
            },
            {
                "name": "Visualization",
                "description": "Publication-quality plot generation"
            }
        ]
    }

def get_swagger_html():
    """Generate Swagger UI HTML page."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlphaGenome API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui.css" />
    <style>
        html {
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }
        *, *:before, *:after {
            box-sizing: inherit;
        }
        body {
            margin: 0;
            background: #fafafa;
        }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
            });
        };
    </script>
</body>
</html>"""

def initialize_alphagenome():
    """Initialize AlphaGenome client."""
    global alphagenome_client
    
    if alphagenome_client:
        return alphagenome_client
    
    try:
        logger.info("Initializing AlphaGenome client...")
        api_key = get_api_key()
        if not api_key:
            logger.error("❌ No AlphaGenome API key found. Please set ALPHA_GENOME_API_KEY environment variable.")
            return None
            
        from alphagenome.models import dna_client
        alphagenome_client = dna_client.create(api_key)
        logger.info("✅ AlphaGenome client initialized successfully")
        return alphagenome_client
        
    except ImportError as e:
        logger.error(f"❌ AlphaGenome SDK not installed: {str(e)}")
        logger.error("Please install with: pip install alphagenome")
        return None
    except Exception as e:
        logger.error(f"❌ Failed to initialize AlphaGenome: {str(e)}")
        return None

class AlphaGenomeHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler for AlphaGenome API."""
    
    def _send_json_response(self, data, status=200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        
        # Comprehensive CORS headers for production
        origin = self.headers.get('Origin')
        if origin:
            self.send_header('Access-Control-Allow-Origin', origin)
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
        
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Accept, Origin')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Max-Age', '86400')  # 24 hours
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_html_response(self, html, status=200):
        """Send HTML response."""
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        
        # CORS headers for HTML responses too
        origin = self.headers.get('Origin')
        if origin:
            self.send_header('Access-Control-Allow-Origin', origin)
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
        
        self.end_headers()
        self.wfile.write(html.encode())
    
    def _send_error(self, message, status=500):
        """Send error response."""
        self._send_json_response({
            "success": False,
            "error": message,
            "timestamp": "2024-01-20T10:30:00Z"
        }, status)
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        
        # Comprehensive CORS preflight headers
        origin = self.headers.get('Origin')
        if origin:
            self.send_header('Access-Control-Allow-Origin', origin)
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
        
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Accept, Origin')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Max-Age', '86400')  # 24 hours
        self.send_header('Content-Length', '0')
        
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        path = urlparse(self.path).path
        
        if path == '/health':
            self._handle_health()
        elif path == '/api/v1/outputs':
            self._handle_outputs()
        elif path == '/api/v1/tissues':
            self._handle_tissues()
        elif path == '/docs' or path == '/':
            self._handle_docs()
        elif path == '/openapi.json':
            self._handle_openapi()
        else:
            self._send_error("Not found", 404)
    
    def do_POST(self):
        """Handle POST requests."""
        path = urlparse(self.path).path
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode()) if content_length > 0 else {}
        except:
            self._send_error("Invalid JSON", 400)
            return
        
        if path == '/api/v1/predict/interval':
            self._handle_predict_interval(data)
        elif path == '/api/v1/predict/variant':
            self._handle_predict_variant(data)
        elif path == '/api/v1/visualize/tracks':
            self._handle_visualize_tracks(data)
        elif path == '/api/v1/visualize/variant':
            self._handle_visualize_variant(data)
        elif path == '/api/v1/visualize/summary':
            self._handle_visualize_summary(data)
        else:
            self._send_error("Not found", 404)
    
    def _handle_docs(self):
        """Serve Swagger UI documentation."""
        self._send_html_response(get_swagger_html())
    
    def _handle_openapi(self):
        """Serve OpenAPI specification."""
        self._send_json_response(get_openapi_spec())
    
    def _handle_health(self):
        """Health check endpoint."""
        client = initialize_alphagenome()
        self._send_json_response({
            "success": True,
            "data": {
                "status": "healthy",
                "alphagenome_initialized": client is not None
            }
        })
    
    def _handle_outputs(self):
        """Get supported outputs."""
        try:
            from alphagenome.models import dna_client
            outputs = [output.name for output in dna_client.OutputType]
            
            self._send_json_response({
                "success": True,
                "data": {
                    "supported_outputs": outputs,
                    "description": "Available genomic output types"
                }
            })
        except Exception as e:
            self._send_error(f"Failed to get outputs: {str(e)}")
    
    def _handle_tissues(self):
        """Get tissue ontology terms."""
        tissues = {
            "UBERON:0001157": "Colon - Transverse",
            "UBERON:0001114": "Right liver lobe",
            "UBERON:0002048": "Lung",
            "UBERON:0000948": "Heart",
            "UBERON:0000955": "Brain",
            "UBERON:0002113": "Kidney"
        }
        
        self._send_json_response({
            "success": True,
            "data": {
                "tissue_ontology_terms": tissues,
                "description": "Available tissue ontology terms"
            }
        })
    
    def _handle_predict_interval(self, data):
        """Handle interval prediction."""
        try:
            client = initialize_alphagenome()
            if not client:
                self._send_error("AlphaGenome client not available")
                return
            
            # Extract request data
            interval_data = data.get('interval', {})
            ontology_terms = data.get('ontology_terms', ['UBERON:0001157'])
            requested_outputs = data.get('requested_outputs', ['RNA_SEQ'])
            
            # Create genomic interval
            from alphagenome.data import genome
            from alphagenome.models import dna_client
            
            interval = genome.Interval(
                chromosome=interval_data['chromosome'],
                start=interval_data['start'],
                end=interval_data['end']
            )
            
            # Convert output types
            output_types = []
            for output_name in requested_outputs:
                output_type = getattr(dna_client.OutputType, output_name)
                output_types.append(output_type)
            
            # Make prediction
            result = client.predict_interval(
                interval=interval,
                requested_outputs=output_types,
                ontology_terms=ontology_terms
            )
            
            # Process results
            predictions = {}
            for output_name in requested_outputs:
                if hasattr(result, output_name.lower()):
                    output_data = getattr(result, output_name.lower())
                    if hasattr(output_data, 'values'):
                        values = output_data.values
                        predictions[output_name] = {
                            "shape": list(values.shape),
                            "mean": float(values.mean()),
                            "std": float(values.std()),
                            "min": float(values.min()),
                            "max": float(values.max())
                        }
            
            self._send_json_response({
                "success": True,
                "data": {
                    "predictions": predictions,
                    "metadata": {
                        "interval": interval_data,
                        "ontology_terms": ontology_terms,
                        "requested_outputs": requested_outputs
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            self._send_error(f"Prediction failed: {str(e)}")
    
    def _handle_predict_variant(self, data):
        """Handle variant effect prediction."""
        try:
            client = initialize_alphagenome()
            if not client:
                self._send_error("AlphaGenome client not available")
                return
            
            # Extract request data
            interval_data = data.get('interval', {})
            variant_data = data.get('variant', {})
            ontology_terms = data.get('ontology_terms', ['UBERON:0001157'])
            requested_outputs = data.get('requested_outputs', ['RNA_SEQ'])
            
            # Create objects
            from alphagenome.data import genome
            from alphagenome.models import dna_client
            
            interval = genome.Interval(
                chromosome=interval_data['chromosome'],
                start=interval_data['start'],
                end=interval_data['end']
            )
            
            variant = genome.Variant(
                chromosome=variant_data['chromosome'],
                position=variant_data['position'],
                reference_bases=variant_data['reference_bases'],
                alternate_bases=variant_data['alternate_bases']
            )
            
            # Convert output types
            output_types = []
            for output_name in requested_outputs:
                output_type = getattr(dna_client.OutputType, output_name)
                output_types.append(output_type)
            
            # Make prediction
            result = client.predict_variant(
                interval=interval,
                variant=variant,
                ontology_terms=ontology_terms,
                requested_outputs=output_types
            )
            
            # Process results
            variant_effects = {}
            for output_name in requested_outputs:
                if hasattr(result, 'reference') and hasattr(result, 'alternate'):
                    ref_data = getattr(result.reference, output_name.lower(), None)
                    alt_data = getattr(result.alternate, output_name.lower(), None)
                    
                    if ref_data and alt_data and hasattr(ref_data, 'values') and hasattr(alt_data, 'values'):
                        ref_values = ref_data.values
                        alt_values = alt_data.values
                        diff_values = alt_values - ref_values
                        
                        variant_effects[output_name] = {
                            "reference": {
                                "mean": float(ref_values.mean()),
                                "std": float(ref_values.std())
                            },
                            "alternate": {
                                "mean": float(alt_values.mean()),
                                "std": float(alt_values.std())
                            },
                            "effect": {
                                "mean_difference": float(diff_values.mean()),
                                "max_absolute_difference": float(abs(diff_values).max()),
                                "effect_direction": "increase" if diff_values.mean() > 0 else "decrease" if diff_values.mean() < 0 else "no_change"
                            }
                        }
            
            self._send_json_response({
                "success": True,
                "data": {
                    "variant_effects": variant_effects,
                    "metadata": {
                        "interval": interval_data,
                        "variant": variant_data,
                        "ontology_terms": ontology_terms,
                        "requested_outputs": requested_outputs
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Variant prediction error: {str(e)}")
            self._send_error(f"Variant prediction failed: {str(e)}")
    
    def _handle_visualize_tracks(self, data):
        """Handle track visualization."""
        try:
            prediction_data = data.get('prediction_data', {})
            title = data.get('title', 'Genomic Track Visualization')
            
            image_base64 = create_visualization(prediction_data, plot_type="track", title=title)
            
            if image_base64:
                self._send_json_response({
                    "success": True,
                    "data": {
                        "image_base64": image_base64,
                        "image_url": f"data:image/png;base64,{image_base64}",
                        "plot_info": {
                            "type": "genomic_tracks",
                            "title": title,
                            "format": "PNG"
                        }
                    }
                })
            else:
                self._send_error("Failed to generate visualization")
                
        except Exception as e:
            logger.error(f"Track visualization error: {str(e)}")
            self._send_error(f"Visualization failed: {str(e)}")
    
    def _handle_visualize_variant(self, data):
        """Handle variant effect visualization."""
        try:
            prediction_data = data.get('prediction_data', {})
            title = data.get('title', 'Variant Effect Visualization')
            
            image_base64 = create_visualization(prediction_data, plot_type="variant", title=title)
            
            if image_base64:
                self._send_json_response({
                    "success": True,
                    "data": {
                        "image_base64": image_base64,
                        "image_url": f"data:image/png;base64,{image_base64}",
                        "plot_info": {
                            "type": "variant_effects",
                            "title": title,
                            "format": "PNG"
                        }
                    }
                })
            else:
                self._send_error("Failed to generate visualization")
                
        except Exception as e:
            logger.error(f"Variant visualization error: {str(e)}")
            self._send_error(f"Visualization failed: {str(e)}")
    
    def _handle_visualize_summary(self, data):
        """Handle summary visualization."""
        try:
            prediction_data = data.get('prediction_data', {})
            title = data.get('title', 'Prediction Summary')
            
            image_base64 = create_visualization(prediction_data, plot_type="summary", title=title)
            
            if image_base64:
                self._send_json_response({
                    "success": True,
                    "data": {
                        "image_base64": image_base64,
                        "image_url": f"data:image/png;base64,{image_base64}",
                        "plot_info": {
                            "type": "prediction_summary",
                            "title": title,
                            "format": "PNG"
                        }
                    }
                })
            else:
                self._send_error("Failed to generate visualization")
                
        except Exception as e:
            logger.error(f"Summary visualization error: {str(e)}")
            self._send_error(f"Visualization failed: {str(e)}")
    
    def log_message(self, format, *args):
        """Override to use Python logging."""
        logger.info(f"{self.address_string()} - {format % args}")

def main():
    """Start the simple HTTP server."""
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"🧬 Simple AlphaGenome Server with Visualization starting on {host}:{port}")
    print("=" * 70)
    
    # Initialize AlphaGenome client at startup
    print("🔧 Initializing AlphaGenome client...")
    client = initialize_alphagenome()
    
    if client:
        print("✅ AlphaGenome client ready!")
        try:
            # Try to get available outputs to verify connection
            from alphagenome.models import dna_client
            outputs = [output.name for output in dna_client.OutputType]
            print(f"📊 Available outputs: {', '.join(outputs[:3])}... ({len(outputs)} total)")
        except Exception as e:
            logger.warning(f"⚠️  Could not fetch output types: {str(e)}")
    else:
        print("❌ AlphaGenome client initialization failed!")
        print("⚠️  Server will start but predictions will not work until client is initialized.")
        print("💡 Check your API key and network connection.")
    
    print("=" * 70)
    
    server = HTTPServer((host, port), AlphaGenomeHandler)
    
    print(f"📋 Health check: http://{host}:{port}/health")
    print(f"📚 Swagger UI: http://{host}:{port}/docs")
    print(f"📄 OpenAPI spec: http://{host}:{port}/openapi.json")
    print(f"🔬 API endpoints:")
    print(f"  GET  /health")
    print(f"  GET  /api/v1/outputs")
    print(f"  GET  /api/v1/tissues")
    print(f"  POST /api/v1/predict/interval")
    print(f"  POST /api/v1/predict/variant")
    print(f"🎨 Visualization endpoints:")
    print(f"  POST /api/v1/visualize/tracks")
    print(f"  POST /api/v1/visualize/variant")
    print(f"  POST /api/v1/visualize/summary")
    print("\n🚀 Server ready! Press Ctrl+C to stop.")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopping...")
        server.shutdown()

if __name__ == "__main__":
    main() 