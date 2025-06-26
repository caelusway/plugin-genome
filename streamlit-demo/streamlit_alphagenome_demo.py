#!/usr/bin/env python3
"""
Streamlit AlphaGenome Demo
Interactive web interface for the AlphaGenome simple demo
"""

import streamlit as st
import os
import sys
import traceback
import time
import matplotlib.pyplot as plt
import numpy as np
import io
import warnings

# Suppress protobuf warnings
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

# Import our environment loader helper
from load_env_helper import get_api_key

# Page configuration
st.set_page_config(
    page_title="🧬 AlphaGenome Demo",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* CSS Custom Properties for theme adaptation */
    :root {
        --primary-color: #1f77b4;
        --success-color: #32cd32;
        --error-color: #ff4444;
        --warning-color: #ffa500;
        --info-color: #1f77b4;
    }
    
    /* Theme-adaptive colors */
    @media (prefers-color-scheme: light) {
        :root {
            --card-bg-color: #ffffff;
            --card-text-color: #333333;
            --card-border-color: rgba(0,0,0,0.1);
            --card-shadow: 0 2px 4px rgba(0,0,0,0.1);
            --secondary-bg-color: #f8f9fa;
        }
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg-color: #262730;
            --card-text-color: #ffffff;
            --card-border-color: rgba(255,255,255,0.1);
            --card-shadow: 0 2px 4px rgba(0,0,0,0.3);
            --secondary-bg-color: #1e1e1e;
        }
    }
    
    /* Fallback for browsers that don't support prefers-color-scheme */
    [data-theme="light"] {
        --card-bg-color: #ffffff;
        --card-text-color: #333333;
        --card-border-color: rgba(0,0,0,0.1);
        --card-shadow: 0 2px 4px rgba(0,0,0,0.1);
        --secondary-bg-color: #f8f9fa;
    }
    
    [data-theme="dark"] {
        --card-bg-color: #262730;
        --card-text-color: #ffffff;
        --card-border-color: rgba(255,255,255,0.1);
        --card-shadow: 0 2px 4px rgba(0,0,0,0.3);
        --secondary-bg-color: #1e1e1e;
    }
    
    /* Main header styling - works with both themes */
    .main-header {
        font-size: 3rem;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    /* Sub headers - use default theme colors */
    .sub-header {
        font-size: 1.5rem;
        margin: 1rem 0;
        font-weight: bold;
    }
    
    /* Base card styling */
    .card-base {
        background-color: var(--card-bg-color);
        color: var(--card-text-color);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--card-border-color);
        transition: all 0.3s ease;
    }
    
    .card-base:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Info boxes with theme-adaptive colors */
    .info-box {
        background-color: var(--card-bg-color);
        color: var(--card-text-color);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--card-border-color);
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .info-box h4 {
        color: var(--primary-color);
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    
    .info-box ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .info-box li {
        margin-bottom: 0.3rem;
        color: var(--card-text-color);
    }
    
    .success-box {
        background-color: var(--card-bg-color);
        color: var(--card-text-color);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--success-color);
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--card-border-color);
        transition: all 0.3s ease;
    }
    
    .success-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .success-box h4 {
        color: var(--success-color);
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    
    .error-box {
        background-color: var(--card-bg-color);
        color: var(--card-text-color);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--error-color);
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--card-border-color);
        transition: all 0.3s ease;
    }
    
    .error-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .error-box h3 {
        color: var(--error-color);
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    
    .error-box a {
        color: var(--primary-color);
        text-decoration: underline;
    }
    
    .error-box code {
        background-color: var(--secondary-bg-color);
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-family: 'Monaco', 'Consolas', monospace;
        font-size: 0.9em;
    }
    
    .metric-container {
        background-color: var(--card-bg-color);
        color: var(--card-text-color);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--card-border-color);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .metric-container h4 {
        color: var(--primary-color);
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    
    .metric-container ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .metric-container li {
        margin-bottom: 0.3rem;
        color: var(--card-text-color);
    }
    
    .config-summary {
        background-color: var(--card-bg-color);
        color: var(--card-text-color);
        padding: 0.8rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary-color);
        margin: 0.5rem 0;
        font-size: 0.95rem;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--card-border-color);
        transition: all 0.3s ease;
    }
    
    .config-summary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Ensure good contrast for both themes */
    .stMarkdown a {
        color: var(--primary-color) !important;
        text-decoration: underline;
    }
    
    .stMarkdown a:hover {
        color: #0d5aa7 !important;
        opacity: 0.8;
    }
    
    /* Status text colors - theme adaptive */
    .status-text-success {
        color: var(--success-color) !important;
        font-weight: bold;
    }
    
    .status-text-info {
        color: var(--info-color) !important;
        font-weight: bold;
    }
    
    .status-text-default {
        font-weight: bold;
        color: var(--card-text-color);
    }
    
    /* Make sure metrics are readable */
    .metric-label {
        font-weight: bold;
    }
    
    /* Code blocks - adaptive */
    .stCode {
        background-color: var(--secondary-bg-color) !important;
        color: var(--card-text-color) !important;
        border: 1px solid var(--card-border-color) !important;
    }
    
    /* Progress bar text */
    .stProgress .stText {
        font-weight: bold;
    }
    
    /* Buttons maintain their theme colors */
    .stButton button {
        font-weight: bold;
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        font-weight: bold;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 0.5rem;
        border: 1px solid var(--card-border-color);
    }
    
    /* Responsive design for smaller screens */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .info-box, .success-box, .error-box, .metric-container, .config-summary {
            margin: 0.5rem 0;
            padding: 0.8rem;
        }
    }
    
    /* Smooth transitions for theme changes */
    * {
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def test_alphagenome_connection(api_key):
    """Test AlphaGenome connection"""
    try:
        from alphagenome.models import dna_client
        model = dna_client.create(api_key)
        # Try to get metadata as a simple test
        metadata = model.output_metadata(organism=dna_client.Organism.HOMO_SAPIENS)
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    if 'prediction_running' not in st.session_state:
        st.session_state.prediction_running = False
    if 'prediction_results' not in st.session_state:
        st.session_state.prediction_results = None
    
    # Header
    st.markdown('<h1 class="main-header">🧬 AlphaGenome Interactive Demo</h1>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 1.1rem; text-align: center; font-weight: 500; margin-bottom: 2rem;"><strong>Explore Google DeepMind\'s AlphaGenome API for genomic variant effect prediction</strong></div>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    st.sidebar.header("🔧 Configuration")
    
    # API Key Setup
    st.sidebar.subheader("🔑 API Key Setup")
    
    # Check for existing API key
    existing_key = get_api_key()
    if existing_key:
        st.sidebar.success("✅ API key loaded from environment")
        api_key_status = "loaded"
    else:
        st.sidebar.warning("⚠️ No API key found in environment")
        api_key_status = "missing"
    
    # Manual API key input
    manual_key = st.sidebar.text_input(
        "Enter API Key (optional)", 
        type="password",
        help="Get your API key from https://deepmind.google.com/science/alphagenome"
    )
    
    # Determine which API key to use
    api_key = manual_key if manual_key else existing_key
    
    if not api_key:
        st.sidebar.error("❌ API key required to run predictions")
        st.markdown("""
        <div class="error-box">
        <h3>🔑 API Key Required</h3>
        <p>To use this demo, you need an AlphaGenome API key:</p>
        <ol>
        <li>Get your free API key from: <a href="https://deepmind.google.com/science/alphagenome" target="_blank">https://deepmind.google.com/science/alphagenome</a></li>
        <li>Either:
            <ul>
            <li>Create a <code>.env</code> file with: <code>ALPHA_GENOME_API_KEY=your-key</code></li>
            <li>Or enter it in the sidebar</li>
            </ul>
        </li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Test connection
    if st.sidebar.button("🔍 Test API Connection"):
        with st.sidebar:
            with st.spinner("Testing connection..."):
                success, message = test_alphagenome_connection(api_key)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
    
    # Demo Configuration
    st.sidebar.subheader("🧬 Genomic Parameters")
    
    # Genomic interval settings
    chromosome = st.sidebar.selectbox(
        "Chromosome", 
        ["chr22", "chr1", "chr2", "chr3", "chr4", "chr5"],
        index=0,
        help="Select the chromosome for analysis"
    )
    
    # Predefined regions for easy selection
    predefined_regions = {
        "Default (chr22)": {"chr": "chr22", "start": 35677410, "end": 36725986},
        "Small region (chr1)": {"chr": "chr1", "start": 1000000, "end": 1100000},
        "Medium region (chr22)": {"chr": "chr22", "start": 36000000, "end": 36200000},
    }
    
    selected_region = st.sidebar.selectbox(
        "Predefined Regions",
        list(predefined_regions.keys()),
        help="Choose a predefined genomic region"
    )
    
    region = predefined_regions[selected_region]
    
    # Allow manual override
    if st.sidebar.checkbox("Manual coordinates"):
        start_pos = st.sidebar.number_input(
            "Start Position", 
            min_value=1, 
            max_value=300000000,
            value=region["start"],
            help="Genomic start position (1-based)"
        )
        end_pos = st.sidebar.number_input(
            "End Position", 
            min_value=1, 
            max_value=300000000,
            value=region["end"],
            help="Genomic end position (1-based)"
        )
    else:
        start_pos = region["start"]
        end_pos = region["end"]
        chromosome = region["chr"]
    
    # Variant settings
    st.sidebar.subheader("🧪 Variant Configuration")
    
    variant_pos = st.sidebar.number_input(
        "Variant Position",
        min_value=start_pos,
        max_value=end_pos,
        value=min(36201698, end_pos),
        help="Position of the genetic variant (1-based)"
    )
    
    ref_base = st.sidebar.selectbox(
        "Reference Base",
        ["A", "T", "G", "C"],
        index=0,
        help="Reference allele"
    )
    
    alt_base = st.sidebar.selectbox(
        "Alternate Base",
        ["A", "T", "G", "C"],
        index=2,
        help="Alternate allele"
    )
    
    # Tissue selection
    tissue_options = {
        "Liver": "UBERON:0001157",
        "Lung": "UBERON:0002048", 
        "Heart": "UBERON:0000948",
        "Brain": "UBERON:0000955",
        "Kidney": "UBERON:0002113"
    }
    
    selected_tissue = st.sidebar.selectbox(
        "Tissue Type",
        list(tissue_options.keys()),
        help="Select tissue for prediction"
    )
    
    tissue_ontology = tissue_options[selected_tissue]
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">📊 Analysis Overview</h2>', unsafe_allow_html=True)
        
        # Compact configuration display
        st.markdown(f"""
        <div class="config-summary">
        <strong>Region:</strong> {chromosome}:{start_pos:,}-{end_pos:,} ({end_pos - start_pos:,} bp) | 
        <strong>Variant:</strong> {chromosome}:{variant_pos} {ref_base}>{alt_base} | 
        <strong>Tissue:</strong> {selected_tissue}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h2 class="sub-header">🚀 Run Analysis</h2>', unsafe_allow_html=True)
        
        # Disable button if prediction is running
        button_disabled = st.session_state.prediction_running
        button_text = "🔄 Running..." if button_disabled else "🔬 Run AlphaGenome Prediction"
        
        if st.button(button_text, type="primary", use_container_width=True, disabled=button_disabled):
            st.session_state.prediction_running = True
            st.session_state.prediction_results = None
            st.rerun()
    
    # Handle prediction execution
    if st.session_state.prediction_running and st.session_state.prediction_results is None:
        run_alphagenome_demo(
            api_key, chromosome, start_pos, end_pos,
            variant_pos, ref_base, alt_base, tissue_ontology, selected_tissue
        )
    
    # Display results if available
    if st.session_state.prediction_results is not None:
        if st.session_state.prediction_results['success']:
            display_results(
                st.session_state.prediction_results['outputs'],
                st.session_state.prediction_results['interval'],
                st.session_state.prediction_results['variant'],
                selected_tissue
            )
        else:
            st.error(f"❌ Error during prediction: {st.session_state.prediction_results['error']}")
            
            # Show detailed error in expander
            with st.expander("🔍 Detailed Error Information"):
                st.code(st.session_state.prediction_results['traceback'])
                
                # Common issues and solutions
                st.markdown("""
                <div class="card-base">
                <strong>Common Issues:</strong><br>
                • <strong>API Key:</strong> Ensure your API key is valid and has quota remaining<br>
                • <strong>Network:</strong> Check your internet connection<br>
                • <strong>Region Size:</strong> Try a smaller genomic region<br>
                • <strong>Protobuf:</strong> Version conflicts (restart the app if needed)
                </div>
                """, unsafe_allow_html=True)
    
    # Information sections
    st.markdown('<h2 class="sub-header">📚 About AlphaGenome</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>🧬 Capabilities</h4>
        <ul>
        <li>DNA sequences up to 1 million base pairs</li>
        <li>Single base-pair resolution</li>
        <li>Multiple output modalities</li>
        <li>Variant effect prediction</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>🔬 Output Types</h4>
        <ul>
        <li>Gene expression (RNA-seq)</li>
        <li>Chromatin accessibility</li>
        <li>Splicing patterns</li>
        <li>Histone modifications</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
        <h4>🌐 Resources</h4>
        <ul>
        <li><a href="https://www.alphagenomedocs.com/" target="_blank">Documentation</a></li>
        <li><a href="https://www.alphagenomedocs.com/tutorials/" target="_blank">Tutorials</a></li>
        <li><a href="https://deepmind.google.com/science/alphagenome" target="_blank">Get API Key</a></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def run_alphagenome_demo(api_key, chromosome, start_pos, end_pos, variant_pos, ref_base, alt_base, tissue_ontology, tissue_name):
    """Run the AlphaGenome prediction demo"""
    
    # Create progress container
    st.markdown('<h2 class="sub-header">⚡ Running Analysis</h2>', unsafe_allow_html=True)
    
    # Progress bar and status
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Import dependencies
        status_text.markdown('<p class="status-text-default">📦 Importing AlphaGenome modules...</p>', unsafe_allow_html=True)
        progress_bar.progress(10)
        
        from alphagenome.data import genome
        from alphagenome.models import dna_client
        from alphagenome.visualization import plot_components
        
        status_text.markdown('<p class="status-text-success">✅ Imports successful</p>', unsafe_allow_html=True)
        progress_bar.progress(20)
        
        # Step 2: Create client
        status_text.markdown('<p class="status-text-default">🔧 Setting up AlphaGenome client...</p>', unsafe_allow_html=True)
        progress_bar.progress(30)
        
        model = dna_client.create(api_key)
        
        status_text.markdown('<p class="status-text-success">✅ Client created successfully</p>', unsafe_allow_html=True)
        progress_bar.progress(40)
        
        # Step 3: Define genomic objects
        status_text.markdown('<p class="status-text-default">🧬 Creating genomic interval and variant...</p>', unsafe_allow_html=True)
        progress_bar.progress(50)
        
        interval = genome.Interval(
            chromosome=chromosome, 
            start=start_pos, 
            end=end_pos
        )
        
        variant = genome.Variant(
            chromosome=chromosome,
            position=variant_pos,
            reference_bases=ref_base,
            alternate_bases=alt_base,
        )
        
        status_text.markdown('<p class="status-text-success">✅ Genomic objects created</p>', unsafe_allow_html=True)
        progress_bar.progress(60)
        
        # Step 4: Make prediction
        status_text.markdown('<p class="status-text-info">🔮 Making variant effect prediction... (this may take a moment)</p>', unsafe_allow_html=True)
        progress_bar.progress(70)
        
        outputs = model.predict_variant(
            interval=interval,
            variant=variant,
            ontology_terms=[tissue_ontology],
            requested_outputs=[dna_client.OutputType.RNA_SEQ],
        )
        
        status_text.markdown('<p class="status-text-success">✅ Prediction completed!</p>', unsafe_allow_html=True)
        progress_bar.progress(90)
        
        # Step 5: Process results
        status_text.markdown('<p class="status-text-default">📊 Processing results...</p>', unsafe_allow_html=True)
        progress_bar.progress(100)
        
        # Store results in session state
        st.session_state.prediction_results = {
            'success': True,
            'outputs': outputs,
            'interval': interval,
            'variant': variant
        }
        st.session_state.prediction_running = False
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Force rerun to display results
        st.rerun()
        
    except Exception as e:
        # Store error in session state
        st.session_state.prediction_results = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        st.session_state.prediction_running = False
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Force rerun to display error
        st.rerun()

def display_results(outputs, interval, variant, tissue_name):
    """Display the prediction results"""
    
    st.markdown('<h2 class="sub-header">📈 Prediction Results</h2>', unsafe_allow_html=True)
    
    # Extract data
    ref_data = outputs.reference.rna_seq.values
    alt_data = outputs.alternate.rna_seq.values
    difference = alt_data - ref_data
    
    # Summary statistics
    ref_mean = ref_data.mean()
    alt_mean = alt_data.mean()
    diff_mean = difference.mean()
    
    # Results overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Reference Mean",
            f"{ref_mean:.6f}",
            help="Average RNA expression for reference allele"
        )
    
    with col2:
        st.metric(
            "Alternate Mean", 
            f"{alt_mean:.6f}",
            delta=f"{diff_mean:.6f}",
            help="Average RNA expression for alternate allele"
        )
    
    with col3:
        st.metric(
            "Effect Size",
            f"{abs(diff_mean):.6f}",
            help="Absolute difference between alleles"
        )
    
    with col4:
        effect_direction = "Increase" if diff_mean > 0 else "Decrease" if diff_mean < 0 else "No change"
        st.metric(
            "Effect Direction",
            effect_direction,
            help="Direction of expression change"
        )
    
    # Detailed statistics
    st.markdown('<h3 class="sub-header">📊 Detailed Statistics</h3>', unsafe_allow_html=True)
    
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        st.markdown(f"""
        <div class="metric-container">
        <h4>🧬 Data Shapes</h4>
        <ul>
        <li><strong>Reference RNA-seq:</strong> {ref_data.shape}</li>
        <li><strong>Alternate RNA-seq:</strong> {alt_data.shape}</li>
        <li><strong>Tissue:</strong> {tissue_name}</li>
        <li><strong>Region size:</strong> {interval.end - interval.start:,} bp</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown(f"""
        <div class="metric-container">
        <h4>📈 Signal Statistics</h4>
        <ul>
        <li><strong>Max absolute difference:</strong> {abs(difference).max():.6f}</li>
        <li><strong>Standard deviation:</strong> {difference.std():.6f}</li>
        <li><strong>Min difference:</strong> {difference.min():.6f}</li>
        <li><strong>Max difference:</strong> {difference.max():.6f}</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Interpretation
    st.markdown('<h3 class="sub-header">🎯 Biological Interpretation</h3>', unsafe_allow_html=True)
    
    if abs(diff_mean) > 0.001:
        effect = "increases" if diff_mean > 0 else "decreases"
        interpretation = f"The variant {variant.chromosome}:{variant.position} {variant.reference_bases}>{variant.alternate_bases} appears to **{effect}** RNA expression in {tissue_name.lower()} tissue."
        st.success(interpretation)
    else:
        st.info(f"The variant {variant.chromosome}:{variant.position} {variant.reference_bases}>{variant.alternate_bases} has minimal effect on RNA expression in {tissue_name.lower()} tissue.")
    
    # Visualization
    st.markdown('<h3 class="sub-header">📊 Visualization</h3>', unsafe_allow_html=True)
    
    try:
        create_visualization(outputs, variant, tissue_name)
        
        # Try AlphaGenome's native visualization too
        st.markdown('<h3 class="sub-header">🎨 AlphaGenome Native Visualization</h3>', unsafe_allow_html=True)
        create_alphagenome_native_plot(outputs, variant, tissue_name)
        
    except Exception as e:
        st.warning(f"⚠️ Visualization not available: {str(e)}")
        st.info("This is normal in some environments. Results are still valid.")
    
    # Reset button
    if st.button("🔄 Run Another Analysis", type="secondary"):
        st.session_state.prediction_results = None
        st.session_state.prediction_running = False
        st.rerun()
    
    # Success message
    st.markdown("""
    <div class="success-box">
    <h4>Analysis Completed Successfully!</h4>
    <p>Your AlphaGenome variant effect prediction has been completed. The results show the predicted impact of your genetic variant on RNA expression.</p>
    </div>
    """, unsafe_allow_html=True)

def create_visualization(outputs, variant, tissue_name):
    """Create and display visualization - ONLY AlphaGenome API output"""
    
    try:
        # Set matplotlib backend for Streamlit
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.ioff()
        
        # Extract ONLY what AlphaGenome API returns
        ref_data = outputs.reference.rna_seq.values  # Raw API output
        alt_data = outputs.alternate.rna_seq.values  # Raw API output
        
        # Create simple plot - just show the raw API data
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot 1: Reference (exactly as API returns it)
        ax1.plot(ref_data.mean(axis=1), color='blue', label='Reference', linewidth=1)
        ax1.set_title(f'Reference Allele ({variant.reference_bases}) - Raw AlphaGenome Output')
        ax1.set_ylabel('RNA Expression')
        ax1.legend()
        
        # Plot 2: Alternate (exactly as API returns it)  
        ax2.plot(alt_data.mean(axis=1), color='red', label='Alternate', linewidth=1)
        ax2.set_title(f'Alternate Allele ({variant.alternate_bases}) - Raw AlphaGenome Output')
        ax2.set_ylabel('RNA Expression')
        ax2.set_xlabel('Position Index')
        ax2.legend()
        
        plt.tight_layout()
        
        # Display in Streamlit
        st.pyplot(fig)
        
        # Show raw data info
        st.markdown('<h3 class="sub-header">📊 Raw AlphaGenome API Output</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Reference Data Shape", str(ref_data.shape))
        with col2:
            st.metric("Alternate Data Shape", str(alt_data.shape))
        
        # Download option
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Plot",
            data=img_buffer.getvalue(),
            file_name=f"alphagenome_raw_{variant.chromosome}_{variant.position}.png",
            mime="image/png"
        )
        
        plt.close(fig)
        
    except Exception as e:
        st.error(f"❌ Could not visualize AlphaGenome output: {str(e)}")
        
        # Show what we actually got from the API
        with st.expander("🔍 Raw API Response Debug"):
            st.code(f"""
API Response Structure:
- Type: {type(outputs)}
- Has reference: {hasattr(outputs, 'reference')}
- Has alternate: {hasattr(outputs, 'alternate')}
- Reference RNA-seq shape: {outputs.reference.rna_seq.values.shape if hasattr(outputs, 'reference') else 'N/A'}
- Alternate RNA-seq shape: {outputs.alternate.rna_seq.values.shape if hasattr(outputs, 'alternate') else 'N/A'}
            """)

def create_alphagenome_native_plot(outputs, variant, tissue_name):
    """Try AlphaGenome's own visualization if available"""
    try:
        from alphagenome.visualization import plot_components
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')
        
        # Use AlphaGenome's native visualization - exactly as in their docs
        fig = plot_components.plot(
            [
                plot_components.OverlaidTracks(
                    tdata={
                        'REF': outputs.reference.rna_seq,
                        'ALT': outputs.alternate.rna_seq,
                    },
                    colors={'REF': 'blue', 'ALT': 'red'},
                ),
            ],
            interval=outputs.reference.rna_seq.interval,
            annotations=[plot_components.VariantAnnotation([variant])],
            title=f'AlphaGenome Native Visualization - {tissue_name}'
        )
        
        # Display in Streamlit
        st.pyplot(fig)
        
        plt.close(fig)
        
    except Exception as e:
        st.info(f"AlphaGenome native visualization not available: {str(e)}")

if __name__ == "__main__":
    main() 