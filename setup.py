# Quick Demo Script for MECE Segmentation
# Run this for a faster demo with fewer users

import sys
import os

# Add the path to import our main module
from app import MECESegmentationSystem

def run_quick_demo():
    """Run a quick demo with fewer users for testing"""
    print("🎯 MECE Segmentation - Quick Demo")
    print("=" * 40)
    
    # Initialize with smaller constraints for demo
    system = MECESegmentationSystem(
        min_segment_size=100,  # Smaller for demo
        max_segment_size=5000
    )
    
    # Run with fewer users for faster execution
    segmented_data, segment_strategy = system.run_complete_analysis(n_users=5000)
    
    # Show top segments
    print("\n🏆 TOP 5 SEGMENTS BY OVERALL SCORE:")
    print("-" * 60)
    top_segments = segment_strategy.sort_values('overall_score', ascending=False).head()
    
    for idx, row in top_segments.iterrows():
        print(f"{row['segment_name']:25} | Size: {row['size']:4,} | Score: {row['overall_score']:.3f}")
    
    # Export demo results
    system.export_results(segment_strategy, "demo_mece_segments")
    
    print("\n✅ Demo completed successfully!")
    print("Check the generated CSV and JSON files for detailed results.")

if __name__ == "__main__":
    run_quick_demo()