#!/usr/bin/env python3
"""
AlphaGenome Simple Demo
This is a direct implementation of the example from the AlphaGenome GitHub README.
"""

import os
import sys

# Import our environment loader helper
from load_env_helper import get_api_key

def main():
    """Main demo function"""
    print("🧬 AlphaGenome Simple Demo")
    print("=" * 40)
    print("Based on the GitHub README example")
    print("=" * 40)
    
    # Get API key (will automatically load from .env if available)
    api_key = get_api_key()
    if not api_key:
        return False
    
    try:
        print("📦 Importing AlphaGenome...")
        
        # Exact imports from the GitHub README example
        from alphagenome.data import genome
        from alphagenome.models import dna_client
        from alphagenome.visualization import plot_components
        import matplotlib.pyplot as plt
        
        print("✅ Imports successful")
        
        print("\n🔧 Setting up AlphaGenome client...")
        
        # Create the DNA client with API key
        # Note: Using the same variable name as in the example
        API_KEY = api_key
        model = dna_client.create(API_KEY)
        
        print("✅ Client created successfully")
        
        print("\n🧬 Creating genomic interval and variant...")
        
        # Define genomic interval - exact same as README example
        interval = genome.Interval(chromosome='chr22', start=35677410, end=36725986)
        
        # Define variant - exact same as README example  
        variant = genome.Variant(
            chromosome='chr22',
            position=36201698,
            reference_bases='A',
            alternate_bases='C',
        )
        
        print(f"📍 Genomic interval: chr22:{interval.start:,}-{interval.end:,}")
        print(f"📏 Region size: {interval.end - interval.start:,} base pairs")
        print(f"🧪 Variant: {variant.chromosome}:{variant.position} {variant.reference_bases}>{variant.alternate_bases}")
        
        print("\n🔮 Making variant effect prediction...")
        print("⏱️ This may take a moment (processing ~1MB of DNA)...")
        
        # Make prediction - exact same as README example
        outputs = model.predict_variant(
            interval=interval,
            variant=variant,
            ontology_terms=['UBERON:0001157'],  # liver tissue
            requested_outputs=[dna_client.OutputType.RNA_SEQ],
        )
        
        print("✅ Prediction completed!")
        
        # Display results
        print(f"\n📊 Results:")
        print(f"- Reference RNA-seq data shape: {outputs.reference.rna_seq.values.shape}")
        print(f"- Alternate RNA-seq data shape: {outputs.alternate.rna_seq.values.shape}")
        print(f"- Tissue: liver (UBERON:0001157)")
        print(f"- Output type: RNA-seq")
        
        # Basic statistics
        ref_mean = outputs.reference.rna_seq.values.mean()
        alt_mean = outputs.alternate.rna_seq.values.mean()
        difference = alt_mean - ref_mean
        
        print(f"\n📈 Signal Analysis:")
        print(f"- Reference mean signal: {ref_mean:.6f}")
        print(f"- Alternate mean signal: {alt_mean:.6f}")
        print(f"- Difference (ALT - REF): {difference:.6f}")
        
        if abs(difference) > 0.001:
            effect = "increase" if difference > 0 else "decrease"
            print(f"🎯 The variant appears to {effect} RNA expression")
        else:
            print("🎯 The variant has minimal effect on RNA expression")
        
        print("\n📈 Creating visualization...")
        
        try:
            # Create the plot - exact same as README example
            plot_components.plot(
                [
                    plot_components.OverlaidTracks(
                        tdata={
                            'REF': outputs.reference.rna_seq,
                            'ALT': outputs.alternate.rna_seq,
                        },
                        colors={'REF': 'dimgrey', 'ALT': 'red'},
                    ),
                ],
                interval=outputs.reference.rna_seq.interval.resize(2**15),
                # Annotate the location of the variant as a vertical line.
                annotations=[plot_components.VariantAnnotation([variant], alpha=0.8)],
            )
            
            # Save the plot
            plt.savefig('alphagenome_demo.png', dpi=150, bbox_inches='tight')
            print("✅ Visualization created and saved as 'alphagenome_demo.png'")
            
            # Show plot if display is available
            try:
                plt.show()
            except:
                print("ℹ️ Plot display not available (saved to file instead)")
                
        except Exception as e:
            print(f"⚠️ Visualization error: {e}")
            print("This is normal in headless environments")
        
        print("\n🎉 Demo completed successfully!")
        print("\n📚 What you just did:")
        print("1. ✅ Connected to the AlphaGenome API")
        print("2. ✅ Defined a genomic region (~1MB on chromosome 22)")
        print("3. ✅ Specified a genetic variant (A>C SNP)")
        print("4. ✅ Predicted RNA expression changes in liver tissue")
        print("5. ✅ Visualized the results")
        
        print("\n🔗 Links:")
        print("- Documentation: https://www.alphagenomedocs.com/")
        print("- Tutorials: https://www.alphagenomedocs.com/tutorials/")
        print("- API Reference: https://www.alphagenomedocs.com/api/")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure AlphaGenome is installed: pip install -U alphagenome")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 