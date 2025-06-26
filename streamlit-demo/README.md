# AlphaGenome Python Setup

This repository contains a simple Python setup for AlphaGenome, Google DeepMind's unifying model for deciphering the regulatory code within DNA sequences.

## 🧬 About AlphaGenome

AlphaGenome offers multimodal predictions, encompassing diverse functional outputs such as:
- Gene expression
- Splicing patterns  
- Chromatin features
- Contact maps

The model analyzes DNA sequences of up to 1 million base pairs in length and can deliver predictions at single base-pair resolution for most outputs.

## 🚀 Quick Start

### Option 1: Interactive Streamlit Demo (Recommended)

Launch the interactive web interface:

```bash
# Install streamlit if not already installed
pip install streamlit

# Launch the demo
python run_streamlit_demo.py
```

Or run directly:
```bash
streamlit run streamlit_alphagenome_demo.py
```

The demo will open in your browser at `http://localhost:8501` and provides:
- 🎛️ Interactive parameter configuration
- 📊 Real-time progress tracking  
- 📈 Automatic result visualization
- 💾 Downloadable plots
- 🧬 Multiple tissue types and genomic regions

### Option 2: Automated Installation

```bash
chmod +x install.sh
./install.sh
```

### Option 3: Manual Installation

1. **Create virtual environment:**
```bash
python3 -m venv alphagenome-env
source alphagenome-env/bin/activate
```

2. **Install AlphaGenome:**
```bash
pip install -U alphagenome
pip install -r requirements.txt
```

3. **Run setup script:**
```bash
python setup_alphagenome.py
```

## 🔑 API Key Setup

### Option 1: Using .env File (Recommended)

1. **Get your API key from:** https://deepmind.google.com/science/alphagenome
2. **Create a .env file** in the project directory:
```bash
# Create .env file
echo "ALPHA_GENOME_API_KEY=your-api-key-here" > .env
```

Or copy from the template:
```bash
cp env_template.txt .env
# Then edit .env and replace 'your-api-key-here' with your actual API key
```

### Option 2: Environment Variable
```bash
export ALPHA_GENOME_API_KEY='your-api-key'
```

The scripts will automatically detect and load your API key from either source!

## 📊 Usage Examples

After installation and API key setup, try these examples:

### 🌐 Interactive Streamlit Demo
```bash
python run_streamlit_demo.py
```
**Features:**
- Interactive parameter selection
- Real-time progress tracking
- Automatic visualization
- Multiple tissue types
- Downloadable results

### 1. Simple Demo (GitHub README Example)
```bash
python alphagenome_simple_demo.py
```
This runs the exact example from the AlphaGenome GitHub repository README.

### 2. Complete Quick Start Guide
```bash
python alphagenome_quickstart.py
```
Comprehensive examples including variant prediction, basic interval analysis, and variant scoring.

### 3. Notebook-Style Walkthrough
```bash
python alphagenome_notebook_example.py
```
Complete workflow mimicking the Google Colab tutorials with detailed explanations.

### 4. Basic Setup Test
```bash
python basic_example.py
```
Simple test to verify your installation and API connection.

## 📦 Dependencies

- `alphagenome` - The main AlphaGenome package
- `numpy` - Numerical computing
- `pandas` - Data manipulation
- `matplotlib` - Visualization
- `python-dotenv` - .env file support
- `streamlit` - Interactive web interface
- `jupyter` - Interactive notebooks (optional)

## 🏗️ Project Structure

```
plugin-genome/
├── requirements.txt                    # Python dependencies
├── setup_alphagenome.py               # Setup and installation script
├── basic_example.py                   # Basic usage example
├── alphagenome_simple_demo.py         # GitHub README example
├── alphagenome_quickstart.py          # Comprehensive quick start
├── alphagenome_notebook_example.py    # Complete workflow
├── streamlit_alphagenome_demo.py      # Interactive Streamlit demo
├── run_streamlit_demo.py              # Streamlit launcher script
├── load_env_helper.py                 # Environment variable loader
├── env_template.txt                   # .env file template
├── install.sh                         # Automated installation script
├── README.md                          # This file
├── .env                               # Your API key (create this file)
└── alphagenome-env/                   # Virtual environment (created after installation)
```

## 📚 Documentation Examples

All examples are based on the official AlphaGenome documentation:

### 📋 Example Features

- **Genomic Interval Creation**: Define and manipulate genomic regions
- **Variant Definition**: SNPs, insertions, deletions with proper formatting
- **API Predictions**: RNA-seq, ATAC-seq, ChIP-seq, and more
- **Variant Effect Prediction**: Compare reference vs. alternate sequences
- **Variant Scoring**: Quantify biological impacts
- **Data Visualization**: Create publication-ready plots
- **Interactive Interface**: Streamlit web app for easy exploration

### 🧬 Supported Capabilities

- **DNA sequence lengths**: ~2KB, ~16KB, ~100KB, ~500KB, up to 1MB
- **Genomic assemblies**: Human (hg38), Mouse (mm10)
- **Output modalities**: RNA-seq, ATAC-seq, ChIP-seq, Hi-C, and more
- **Tissue/cell types**: 600+ different contexts via ontology terms
- **Prediction resolution**: Single base-pair accuracy

## 🔬 API Features

- **Free for non-commercial use**
- **DNA sequences up to 1M base pairs**
- **Single base-pair resolution predictions**
- **State-of-the-art performance** on genomic prediction benchmarks
- **Suitable for small to medium-scale analyses** (1000s of predictions)

## 🤝 Usage Guidelines

The API is offered as a free service for non-commercial use. Query rates vary based on demand – it is well suited for smaller to medium-scale analyses but may not be suitable for large scale analyses requiring more than 1 million predictions.

## 📖 Official Resources

- [Official AlphaGenome Documentation](https://www.alphagenomedocs.com/)
- [Installation Guide](https://www.alphagenomedocs.com/installation.html)
- [Tutorials](https://www.alphagenomedocs.com/colabs/essential_commands.html)
- [GitHub Repository](https://github.com/google-deepmind/alphagenome)
- [API Reference](https://www.alphagenomedocs.com/api/)

## ⚡ Example Workflows

### Interactive Streamlit Demo
```bash
# Launch the web interface
python run_streamlit_demo.py

# Configure parameters in the sidebar:
# - Genomic coordinates
# - Variant definition  
# - Tissue selection
# - Click "Run Analysis"
```

### Basic Genomic Prediction
```python
from alphagenome.data import genome
from alphagenome.models import dna_client

# Create client
model = dna_client.create(API_KEY)

# Define genomic region
interval = genome.Interval('chr1', 1000000, 1002048)

# Make predictions
outputs = model.predict(
    interval=interval,
    ontology_terms=['UBERON:0001157'],  # liver tissue
    requested_outputs=[dna_client.OutputType.RNA_SEQ],
)
```

### Variant Effect Analysis
```python
# Define variant
variant = genome.Variant(
    chromosome='chr22',
    position=36201698,
    reference_bases='A',
    alternate_bases='C',
)

# Predict variant effects
outputs = model.predict_variant(
    interval=interval,
    variant=variant,
    ontology_terms=['UBERON:0001157'],
    requested_outputs=[dna_client.OutputType.RNA_SEQ],
)

# Compare reference vs alternate
ref_signal = outputs.reference.rna_seq.values.mean()
alt_signal = outputs.alternate.rna_seq.values.mean()
effect = alt_signal - ref_signal
```

## 🎯 Next Steps

Once setup is complete, you can:

1. **🌐 Try the interactive Streamlit demo** for easy exploration
2. **📓 Explore the tutorial notebooks**
3. **🧬 Analyze your genomic data**
4. **🧪 Make variant effect predictions**
5. **📊 Generate gene expression predictions**
6. **🔬 Analyze chromatin features**
7. **📈 Create publication-ready visualizations**

For interactive analysis, consider using Jupyter notebooks with the installed environment.

## 🆘 Getting Help

- **GitHub Issues**: [Submit bugs and feature requests](https://github.com/google-deepmind/alphagenome/issues)
- **Community Forum**: Active monitoring by the DeepMind team
- **Email Support**: alphagenome@google.com

## 📄 Citation

If you use AlphaGenome in your research, please cite:

```bibtex
@misc{alphagenome,
  title={AlphaGenome: advancing regulatory variant effect prediction with a unified DNA sequence model},
  author={Avsec, Žiga and Latysheva, Natasha and Cheng, Jun and Novati, Guido and Taylor, Kyle R. and Ward, Tom and Bycroft, Clare and Nicolaisen, Lauren and Arvaniti, Eirini and Pan, Joshua and Thomas, Raina and Dutordoir, Vincent and Perino, Matteo and De, Soham and Karollus, Alexander and Gayoso, Adam and Sargeant, Toby and Mottram, Anne and Hong Wong, Lai and Drotár, Pavol and Kosiorek, Adam and Senior, Andrew and Tanburn, Richard and Applebaum, Taylor and Basu, Souradeep and Hassabis, Demis and Kohli, Pushmeet},
  url={https://storage.googleapis.com/deepmind-media/papers/alphagenome.pdf},
  year={2025},
}
``` 