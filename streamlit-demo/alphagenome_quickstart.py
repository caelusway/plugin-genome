#!/usr/bin/env python3
"""
AlphaGenome Quick Start Example
Based on the official AlphaGenome documentation and GitHub repository examples.
This demonstrates the main functionality of the AlphaGenome API.
"""

import os
import sys

# Import our environment loader helper
from load_env_helper import get_api_key

def check_setup():
    """Check if the environment is properly set up"""
    api_key = get_api_key()
    if not api_key:
        print("❌ ALPHA_GENOME_API_KEY environment variable not set")
        print("Please get your API key from: https://deepmind.google.com/science/alphagenome")
        print("Then set it: export ALPHA_GENOME_API_KEY='your-api-key'")
        return False
    print("✅ API key found")
    return True

def import_dependencies():
    """Import all the AlphaGenome dependencies"""
    try:
        print("📦 Importing AlphaGenome modules...")
        
        # Core imports from the quick start guide
        from alphagenome.data import gene_annotation
        from alphagenome.data import genome
        from alphagenome.data import transcript as transcript_utils
        from alphagenome.interpretation import ism
        from alphagenome.models import dna_client
        from alphagenome.models import variant_scorers
        from alphagenome.visualization import plot_components
        import matplotlib.pyplot as plt
        import pandas as pd
        
        print("✅ All imports successful")
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
        print("Make sure AlphaGenome is installed: pip install -U alphagenome")
        return None

def variant_prediction_example(modules):
    """
    Example: Variant Effect Prediction
    Based on the example from the AlphaGenome GitHub repository README
    """
    print("\n🧬 Example 1: Variant Effect Prediction")
    print("=" * 50)
    
    try:
        # Get API key and create client
        API_KEY = get_api_key()
        model = modules['dna_client'].create(API_KEY)
        
        print("🔬 Creating genomic interval and variant...")
        
        # Define a genomic interval (chromosome 22, ~1MB region)
        interval = modules['genome'].Interval(
            chromosome='chr22', 
            start=35677410, 
            end=36725986
        )
        
        # Define a variant (SNP: A->C at position 36201698)
        variant = modules['genome'].Variant(
            chromosome='chr22',
            position=36201698,
            reference_bases='A',
            alternate_bases='C',
        )
        
        print(f"📍 Interval: {interval}")
        print(f"🧪 Variant: {variant}")
        print(f"📏 Region size: {interval.end - interval.start:,} base pairs")
        
        print("\n🔮 Making predictions...")
        print("This may take a moment...")
        
        # Make variant predictions for RNA-seq output
        outputs = model.predict_variant(
            interval=interval,
            variant=variant,
            ontology_terms=['UBERON:0001157'],  # liver tissue
            requested_outputs=[modules['dna_client'].OutputType.RNA_SEQ],
        )
        
        print("✅ Prediction completed!")
        print(f"📊 Reference RNA-seq data shape: {outputs.reference.rna_seq.values.shape}")
        print(f"📊 Alternate RNA-seq data shape: {outputs.alternate.rna_seq.values.shape}")
        
        # Optional: Create visualization (requires matplotlib display capability)
        try:
            print("\n📈 Creating visualization...")
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
                annotations=[modules['plot_components'].VariantAnnotation([variant], alpha=0.8)],
            )
            print("✅ Visualization created (check if display available)")
            
            # Save the plot
            modules['plt'].savefig('variant_prediction.png', dpi=150, bbox_inches='tight')
            print("💾 Plot saved as 'variant_prediction.png'")
        except Exception as e:
            print(f"⚠️ Visualization error (this is normal in headless environments): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def basic_interval_prediction(modules):
    """
    Example: Basic genomic interval prediction
    """
    print("\n🧬 Example 2: Basic Genomic Interval Prediction")
    print("=" * 50)
    
    try:
        API_KEY = get_api_key()
        model = modules['dna_client'].create(API_KEY)
        
        print("🔬 Creating a smaller genomic interval...")
        
        # Create a smaller interval for faster processing
        interval = modules['genome'].Interval(
            chromosome='chr1', 
            start=1000000, 
            end=1002048  # ~2KB region
        )
        
        print(f"📍 Interval: {interval}")
        print(f"📏 Region size: {interval.end - interval.start:,} base pairs")
        
        print("\n🔮 Making basic predictions...")
        
        # Make predictions for multiple output types
        outputs = model.predict(
            interval=interval,
            ontology_terms=['UBERON:0001157'],  # liver tissue
            requested_outputs=[
                modules['dna_client'].OutputType.RNA_SEQ,
                modules['dna_client'].OutputType.ATAC_SEQ,
            ],
        )
        
        print("✅ Prediction completed!")
        print(f"📊 RNA-seq data shape: {outputs.rna_seq.values.shape}")
        print(f"📊 ATAC-seq data shape: {outputs.atac_seq.values.shape}")
        
        # Display some basic statistics
        rna_mean = outputs.rna_seq.values.mean()
        atac_mean = outputs.atac_seq.values.mean()
        
        print(f"📈 RNA-seq mean signal: {rna_mean:.4f}")
        print(f"📈 ATAC-seq mean signal: {atac_mean:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def variant_scoring_example(modules):
    """
    Example: Variant scoring workflow
    """
    print("\n🧬 Example 3: Variant Scoring")
    print("=" * 50)
    
    try:
        API_KEY = get_api_key()
        model = modules['dna_client'].create(API_KEY)
        
        print("🔬 Setting up variant scoring...")
        
        # Define interval and variant
        interval = modules['genome'].Interval(
            chromosome='chr22', 
            start=36200000, 
            end=36202048  # Smaller region for faster processing
        )
        
        variant = modules['genome'].Variant(
            chromosome='chr22',
            position=36201000,
            reference_bases='G',
            alternate_bases='T',
        )
        
        print(f"📍 Interval: {interval}")
        print(f"🧪 Variant: {variant}")
        
        print("\n🔮 Computing variant scores...")
        
        # Use variant scorers for different output types
        rna_scorer = modules['variant_scorers'].GeneExpressionScorer()
        
        # Get variant predictions
        outputs = model.predict_variant(
            interval=interval,
            variant=variant,
            ontology_terms=['UBERON:0001157'],  # liver tissue
            requested_outputs=[modules['dna_client'].OutputType.RNA_SEQ],
        )
        
        # Compute scores
        scores = rna_scorer.score(outputs)
        
        print("✅ Scoring completed!")
        print(f"📊 Number of scores: {len(scores.raw_score)}")
        print(f"📈 Score range: {scores.raw_score.min():.4f} to {scores.raw_score.max():.4f}")
        
        # Display top few scores
        print("\n🏆 Top variant effect scores:")
        top_scores = scores.raw_score.nlargest(5)
        for idx, score in top_scores.items():
            print(f"  Track {idx}: {score:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Scoring error: {e}")
        return False

def run_examples():
    """Run all AlphaGenome examples"""
    print("🧬 AlphaGenome Complete Examples")
    print("=" * 60)
    print("Based on official documentation and GitHub repository")
    print("=" * 60)
    
    # Check setup
    if not check_setup():
        return False
    
    # Import dependencies
    modules = import_dependencies()
    if not modules:
        return False
    
    print(f"\n🎯 AlphaGenome API Capabilities:")
    print(f"- DNA sequences up to 1 million base pairs")
    print(f"- Single base-pair resolution predictions")
    print(f"- Multiple output modalities (RNA-seq, ATAC-seq, ChIP-seq, etc.)")
    print(f"- Variant effect prediction")
    print(f"- Human (hg38) and mouse (mm10) genomes supported")
    
    success_count = 0
    
    # Run examples
    examples = [
        ("Variant Effect Prediction", lambda: variant_prediction_example(modules)),
        ("Basic Interval Prediction", lambda: basic_interval_prediction(modules)),
        ("Variant Scoring", lambda: variant_scoring_example(modules)),
    ]
    
    for name, example_func in examples:
        try:
            if example_func():
                success_count += 1
                print(f"✅ {name} completed successfully!")
            else:
                print(f"❌ {name} failed")
        except Exception as e:
            print(f"❌ {name} failed with error: {e}")
    
    print(f"\n🎉 Completed {success_count}/{len(examples)} examples successfully!")
    
    if success_count > 0:
        print("\n📚 Next Steps:")
        print("1. Try the visualization tutorials: https://www.alphagenomedocs.com/tutorials/")
        print("2. Explore batch variant scoring for multiple variants")
        print("3. Check out different output modalities and tissue types")
        print("4. Read the API documentation for advanced usage")
    
    return success_count > 0

if __name__ == "__main__":
    success = run_examples()
    sys.exit(0 if success else 1) 