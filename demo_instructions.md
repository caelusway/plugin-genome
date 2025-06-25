# 🧬 AlphaGenome Streamlit Demo Instructions

## Quick Start

1. **Ensure your environment is set up:**
   ```bash
   source alphagenome-env/bin/activate  # If using virtual environment
   pip install streamlit  # If not already installed
   ```

2. **Set up your API key** (one of these options):
   - Create `.env` file: `echo "ALPHA_GENOME_API_KEY=your-key-here" > .env`
   - Or enter it directly in the app sidebar

3. **Launch the demo:**
   ```bash
   python run_streamlit_demo.py
   ```
   
   Or directly:
   ```bash
   streamlit run streamlit_alphagenome_demo.py
   ```

4. **Open your browser** to `http://localhost:8501`

## 🎛️ Using the Demo

### Sidebar Configuration
- **🔑 API Key**: Enter your AlphaGenome API key
- **🧬 Genomic Parameters**: 
  - Choose chromosome and genomic region
  - Select from predefined regions or enter custom coordinates
- **🧪 Variant Configuration**:
  - Set variant position and alleles (A, T, G, C)
- **🔬 Tissue Selection**: 
  - Choose from Liver, Lung, Heart, Brain, or Kidney

### Running Analysis
1. Configure your parameters in the sidebar
2. Review the analysis overview in the main panel
3. Click "🔬 Run AlphaGenome Prediction"
4. Watch the real-time progress bar
5. View comprehensive results with:
   - Interactive metrics
   - Statistical analysis
   - Biological interpretation
   - Downloadable visualizations

## 📊 Features

- **Interactive Configuration**: Easy parameter selection via dropdowns and inputs
- **Real-time Progress**: Visual progress tracking during API calls
- **Comprehensive Results**: Detailed statistics and biological interpretation
- **Automatic Visualization**: Generate and download publication-ready plots
- **Multiple Tissues**: Support for different tissue types and ontology terms
- **Error Handling**: Graceful error handling with detailed debugging information

## 🧬 Example Configurations

### Default Example (from GitHub README)
- **Region**: chr22:35,677,410-36,725,986
- **Variant**: chr22:36201698 A>C  
- **Tissue**: Liver

### Small Test Region
- **Region**: chr1:1,000,000-1,100,000
- **Variant**: chr1:1,050,000 G>T
- **Tissue**: Lung

### Custom Analysis
- Use "Manual coordinates" checkbox to enter your own genomic region
- Adjust variant position within the selected region
- Try different reference/alternate allele combinations

## 🚀 Tips

- **API Key**: Get your free key from https://deepmind.google.com/science/alphagenome
- **Region Size**: Larger regions take longer but provide more context
- **Visualization**: Plots are automatically saved and can be downloaded
- **Debugging**: Check the detailed error information if something goes wrong
- **Performance**: Analysis typically takes 30-60 seconds depending on region size

## 🛑 Stopping the Demo

Press `Ctrl+C` in the terminal to stop the Streamlit server.

## 📚 Next Steps

After trying the demo:
1. Explore the command-line examples: `python alphagenome_simple_demo.py`
2. Check out the comprehensive tutorials: `python alphagenome_notebook_example.py`
3. Read the official documentation: https://www.alphagenomedocs.com/
4. Try your own genomic variants and regions! 