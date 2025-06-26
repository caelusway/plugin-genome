#!/usr/bin/env python3
"""
AlphaGenome Notebook-Style Example
Based on the Quick Start Guide and Essential Commands from the documentation.
This mimics the structure of the Google Colab notebooks.
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Import our environment loader helper
from load_env_helper import get_api_key

def install_check():
    """Check AlphaGenome installation - mimics the @title Install AlphaGenome cell"""
    print("🔧 AlphaGenome Installation Check")
    print("=" * 40)
    
    try:
        import alphagenome
        print(f"✅ AlphaGenome installed successfully")
        print(f"📦 Version: {getattr(alphagenome, '__version__', 'unknown')}")
        return True
    except ImportError:
        print("❌ AlphaGenome not installed")
        print("Install with: pip install -U alphagenome")
        return False

def imports_cell():
    """Import all dependencies - mimics the imports cell from the quick start guide"""
    print("\n📦 Importing Dependencies")
    print("=" * 40)
    
    try:
        # Essential imports from the quick start guide
        from alphagenome.data import gene_annotation
        from alphagenome.data import genome
        from alphagenome.data import transcript as transcript_utils
        from alphagenome.interpretation import ism
        from alphagenome.models import dna_client
        from alphagenome.models import variant_scorers
        from alphagenome.visualization import plot_components
        import matplotlib.pyplot as plt
        import pandas as pd
        
        print("✅ Core AlphaGenome modules imported")
        print("✅ Visualization and analysis tools imported")
        
        return {
            'gene_annotation': gene_annotation,
            'genome': genome,
            'transcript_utils': transcript_utils,
            'ism': ism,
            'dna_client': dna_client,
            'variant_scorers': variant_scorers,
            'plot_components': plot_components,
            'plt': plt,
            'pd': pd
        }
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return None

def setup_client(modules):
    """Set up the AlphaGenome client"""
    print("\n🔧 Setting Up AlphaGenome Client")
    print("=" * 40)
    
    # Check for API key
    api_key = get_api_key()
    if not api_key:
        print("❌ ALPHA_GENOME_API_KEY not found")
        print("📝 Get your API key from: https://deepmind.google.com/science/alphagenome")
        print("🔐 Set it with: export ALPHA_GENOME_API_KEY='your-api-key'")
        return None
    
    try:
        # Create the DNA client
        model = modules['dna_client'].create(api_key)
        print("✅ AlphaGenome client created successfully")
        print("🌐 Connected to Google DeepMind's AlphaGenome API")
        return model
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return None

def genomic_basics_example(modules, model):
    """Basic genomic interval and data exploration"""
    print("\n🧬 Genomic Basics Example")
    print("=" * 40)
    
    try:
        # Create a basic genomic interval
        print("📍 Creating genomic intervals...")
        
        # Example 1: Small interval for quick testing
        small_interval = modules['genome'].Interval(
            chromosome='chr1',
            start=1000000,
            end=1002048  # ~2KB
        )
        
        # Example 2: Medium interval
        medium_interval = modules['genome'].Interval(
            chromosome='chr22',
            start=36000000,
            end=36016384  # ~16KB
        )
        
        print(f"🔬 Small interval: {small_interval}")
        print(f"🔬 Medium interval: {medium_interval}")
        print(f"📏 Small size: {small_interval.end - small_interval.start:,} bp")
        print(f"📏 Medium size: {medium_interval.end - medium_interval.start:,} bp")
        
        # Show supported sequence lengths
        print("\n📋 AlphaGenome supported sequence lengths:")
        supported_lengths = [2048, 16384, 131072, 524288, 1048576]
        for length in supported_lengths:
            kb = length // 1024
            if kb >= 1024:
                size_str = f"{kb//1024}MB"
            else:
                size_str = f"{kb}KB"
            print(f"  - {length:,} bp (~{size_str})")
        
        # Demonstrate interval operations
        print(f"\n🔧 Interval operations:")
        
        # Resize to nearest supported length
        resized = small_interval.resize(2048)
        print(f"📐 Resized interval: {resized}")
        print(f"📏 New size: {resized.end - resized.start:,} bp")
        
        # Check overlap
        test_interval = modules['genome'].Interval('chr1', 1001000, 1003000)
        overlap = small_interval.overlaps(test_interval)
        print(f"🔄 Overlaps with test interval: {overlap}")
        
        return small_interval, medium_interval
        
    except Exception as e:
        print(f"❌ Error in genomic basics: {e}")
        return None, None

def variant_definition_example(modules):
    """Show how to define variants"""
    print("\n🧪 Variant Definition Example")
    print("=" * 40)
    
    try:
        # Different types of variants
        print("🧬 Creating different variant types...")
        
        # SNP (Single Nucleotide Polymorphism)
        snp = modules['genome'].Variant(
            chromosome='chr22',
            position=36201698,  # 1-indexed position
            reference_bases='A',
            alternate_bases='C',
        )
        
        # Insertion
        insertion = modules['genome'].Variant(
            chromosome='chr1',
            position=1000000,
            reference_bases='G',
            alternate_bases='GTT',
        )
        
        # Deletion
        deletion = modules['genome'].Variant(
            chromosome='chr1',
            position=1000010,
            reference_bases='ATG',
            alternate_bases='A',
        )
        
        print(f"🔸 SNP: {snp}")
        print(f"🔸 Insertion: {insertion}")
        print(f"🔸 Deletion: {deletion}")
        
        # Show variant properties
        print(f"\n📊 Variant properties:")
        print(f"SNP type: {snp.variant_type}")
        print(f"SNP start (0-indexed): {snp.start()}")
        print(f"SNP end (0-indexed): {snp.end()}")
        print(f"Insertion length: {len(insertion.alternate_bases) - len(insertion.reference_bases)}")
        print(f"Deletion length: {len(deletion.reference_bases) - len(deletion.alternate_bases)}")
        
        return snp, insertion, deletion
        
    except Exception as e:
        print(f"❌ Error in variant definition: {e}")
        return None, None, None

def basic_prediction_example(modules, model, interval):
    """Basic prediction example"""
    print("\n🔮 Basic Prediction Example")
    print("=" * 40)
    
    if not model or not interval:
        print("❌ Skipping: model or interval not available")
        return None
    
    try:
        print("🧬 Making basic genomic predictions...")
        print(f"📍 Region: {interval}")
        
        # Make predictions for multiple output types
        print("⏱️ This may take a moment...")
        
        outputs = model.predict(
            interval=interval,
            ontology_terms=['UBERON:0001157'],  # liver tissue
            requested_outputs=[
                modules['dna_client'].OutputType.RNA_SEQ,
                modules['dna_client'].OutputType.ATAC_SEQ,
            ],
        )
        
        print("✅ Predictions completed!")
        
        # Analyze outputs
        print(f"\n📊 Output Analysis:")
        print(f"🧬 RNA-seq data shape: {outputs.rna_seq.values.shape}")
        print(f"🧬 ATAC-seq data shape: {outputs.atac_seq.values.shape}")
        
        # Basic statistics
        rna_stats = {
            'mean': outputs.rna_seq.values.mean(),
            'std': outputs.rna_seq.values.std(),
            'min': outputs.rna_seq.values.min(),
            'max': outputs.rna_seq.values.max()
        }
        
        atac_stats = {
            'mean': outputs.atac_seq.values.mean(),
            'std': outputs.atac_seq.values.std(),
            'min': outputs.atac_seq.values.min(),
            'max': outputs.atac_seq.values.max()
        }
        
        print(f"\n📈 RNA-seq Statistics:")
        for stat, value in rna_stats.items():
            print(f"  {stat}: {value:.6f}")
        
        print(f"\n📈 ATAC-seq Statistics:")
        for stat, value in atac_stats.items():
            print(f"  {stat}: {value:.6f}")
        
        # Track information
        print(f"\n🏷️ Track Information:")
        print(f"RNA-seq tracks: {len(outputs.rna_seq.values.shape) > 1 and outputs.rna_seq.values.shape[1] or 'N/A'}")
        print(f"ATAC-seq tracks: {len(outputs.atac_seq.values.shape) > 1 and outputs.atac_seq.values.shape[1] or 'N/A'}")
        
        return outputs
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return None

def variant_prediction_example(modules, model, variant):
    """Variant effect prediction example"""
    print("\n🎯 Variant Effect Prediction Example")
    print("=" * 40)
    
    if not model or not variant:
        print("❌ Skipping: model or variant not available")
        return None
    
    try:
        print("🧪 Making variant effect predictions...")
        print(f"🔬 Variant: {variant}")
        
        # Create a suitable interval around the variant
        interval = modules['genome'].Interval(
            chromosome=variant.chromosome,
            start=variant.position - 8192,  # 8KB upstream
            end=variant.position + 8192     # 8KB downstream
        ).resize(16384)  # Resize to nearest supported length
        
        print(f"📍 Analysis region: {interval}")
        print(f"📏 Region size: {interval.end - interval.start:,} bp")
        
        print("⏱️ This may take a moment...")
        
        # Make variant predictions
        outputs = model.predict_variant(
            interval=interval,
            variant=variant,
            ontology_terms=['UBERON:0001157'],  # liver tissue
            requested_outputs=[modules['dna_client'].OutputType.RNA_SEQ],
        )
        
        print("✅ Variant predictions completed!")
        
        # Analyze the results
        print(f"\n📊 Variant Effect Analysis:")
        print(f"🧬 Reference RNA-seq shape: {outputs.reference.rna_seq.values.shape}")
        print(f"🧬 Alternate RNA-seq shape: {outputs.alternate.rna_seq.values.shape}")
        
        # Calculate differences
        ref_data = outputs.reference.rna_seq.values
        alt_data = outputs.alternate.rna_seq.values
        diff = alt_data - ref_data
        
        print(f"\n📈 Effect Statistics:")
        print(f"Reference mean: {ref_data.mean():.6f}")
        print(f"Alternate mean: {alt_data.mean():.6f}")
        print(f"Mean difference: {diff.mean():.6f}")
        print(f"Max absolute difference: {abs(diff).max():.6f}")
        print(f"Standard deviation of difference: {diff.std():.6f}")
        
        # Interpretation
        if abs(diff.mean()) > 0.001:
            effect = "increases" if diff.mean() > 0 else "decreases"
            print(f"🎯 The variant {effect} RNA expression on average")
        else:
            print("🎯 The variant has minimal average effect on RNA expression")
        
        return outputs
        
    except Exception as e:
        print(f"❌ Variant prediction error: {e}")
        return None

def variant_scoring_example(modules, model, variant_outputs):
    """Variant scoring example"""
    print("\n⚖️ Variant Scoring Example")
    print("=" * 40)
    
    if not variant_outputs:
        print("❌ Skipping: variant outputs not available")
        return None
    
    try:
        print("🔢 Computing variant effect scores...")
        
        # Initialize different scorers
        scorers = {
            'Gene Expression': modules['variant_scorers'].GeneExpressionScorer(),
            # Add more scorers as available
        }
        
        results = {}
        
        for scorer_name, scorer in scorers.items():
            print(f"📊 Running {scorer_name} scorer...")
            try:
                scores = scorer.score(variant_outputs)
                results[scorer_name] = scores
                
                print(f"✅ {scorer_name} scoring completed")
                print(f"  📈 Number of scores: {len(scores.raw_score)}")
                print(f"  📈 Score range: {scores.raw_score.min():.6f} to {scores.raw_score.max():.6f}")
                
                # Show top scores
                if len(scores.raw_score) > 0:
                    top_scores = scores.raw_score.nlargest(3)
                    print(f"  🏆 Top 3 scores:")
                    for idx, score in top_scores.items():
                        print(f"    Track {idx}: {score:.6f}")
                
            except Exception as e:
                print(f"⚠️ {scorer_name} scoring failed: {e}")
        
        return results
        
    except Exception as e:
        print(f"❌ Scoring error: {e}")
        return None

def visualization_example(modules, outputs, variant=None):
    """Visualization example"""
    print("\n📈 Visualization Example")
    print("=" * 40)
    
    if not outputs:
        print("❌ Skipping: outputs not available")
        return False
    
    try:
        print("🎨 Creating visualizations...")
        
        # Set up matplotlib for saving
        modules['plt'].ioff()  # Turn off interactive mode
        
        if hasattr(outputs, 'reference') and hasattr(outputs, 'alternate'):
            # Variant comparison plot
            print("📊 Creating variant comparison plot...")
            
            modules['plot_components'].plot(
                [
                    modules['plot_components'].OverlaidTracks(
                        tdata={
                            'REF': outputs.reference.rna_seq,
                            'ALT': outputs.alternate.rna_seq,
                        },
                        colors={'REF': 'dimgrey', 'ALT': 'red'},
                    ),
                ],
                interval=outputs.reference.rna_seq.interval.resize(2**15),
                annotations=[modules['plot_components'].VariantAnnotation([variant], alpha=0.8)] if variant else [],
            )
            
            modules['plt'].title('AlphaGenome Variant Effect Prediction\nRNA-seq in Liver Tissue')
            modules['plt'].savefig('variant_effect.png', dpi=150, bbox_inches='tight')
            print("💾 Variant effect plot saved as 'variant_effect.png'")
            
        elif hasattr(outputs, 'rna_seq'):
            # Basic prediction plot
            print("📊 Creating basic prediction plot...")
            
            modules['plot_components'].plot(
                [
                    modules['plot_components'].Track(outputs.rna_seq, color='blue')
                ],
                interval=outputs.rna_seq.interval,
            )
            
            modules['plt'].title('AlphaGenome Genomic Prediction\nRNA-seq in Liver Tissue')
            modules['plt'].savefig('genomic_prediction.png', dpi=150, bbox_inches='tight')
            print("💾 Genomic prediction plot saved as 'genomic_prediction.png'")
        
        modules['plt'].close('all')  # Clean up
        print("✅ Visualizations completed")
        return True
        
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")
        print("This is normal in some environments")
        return False

def main():
    """Main notebook execution"""
    print("🧬 AlphaGenome Notebook-Style Example")
    print("=" * 60)
    print("Complete workflow based on official documentation")
    print("=" * 60)
    
    # Cell 1: Installation check
    if not install_check():
        return False
    
    # Cell 2: Imports
    modules = imports_cell()
    if not modules:
        return False
    
    # Cell 3: Setup client
    model = setup_client(modules)
    if not model:
        print("⚠️ Continuing with limited functionality (no API calls)")
    
    # Cell 4: Genomic basics
    small_interval, medium_interval = genomic_basics_example(modules, model)
    
    # Cell 5: Variant definition
    snp, insertion, deletion = variant_definition_example(modules)
    
    if model:
        # Cell 6: Basic prediction
        basic_outputs = basic_prediction_example(modules, model, small_interval)
        
        # Cell 7: Variant prediction
        variant_outputs = variant_prediction_example(modules, model, snp)
        
        # Cell 8: Variant scoring
        scoring_results = variant_scoring_example(modules, model, variant_outputs)
        
        # Cell 9: Visualization
        if variant_outputs:
            visualization_example(modules, variant_outputs, snp)
        elif basic_outputs:
            visualization_example(modules, basic_outputs)
    
    print("\n🎉 Notebook example completed!")
    print("\n📚 What was demonstrated:")
    print("✅ AlphaGenome installation and imports")
    print("✅ API client setup")
    print("✅ Genomic interval creation and manipulation")
    print("✅ Variant definition (SNPs, insertions, deletions)")
    if model:
        print("✅ Basic genomic predictions")
        print("✅ Variant effect predictions")
        print("✅ Variant scoring")
        print("✅ Data visualization")
    else:
        print("⏭️ API-dependent features (need API key)")
    
    print("\n🔗 Next Steps:")
    print("1. Get your API key: https://deepmind.google.com/science/alphagenome")
    print("2. Try the interactive tutorials: https://www.alphagenomedocs.com/tutorials/")
    print("3. Explore more output modalities (ChIP-seq, Hi-C, etc.)")
    print("4. Try batch variant analysis")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 