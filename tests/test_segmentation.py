"""
Tests for MECE Segmentation System
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import MECESegmentationSystem
from config import config

class TestMECESegmentationSystem:
    """Test cases for MECE Segmentation System"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.system = MECESegmentationSystem(
            min_segment_size=100,  # Smaller for testing
            max_segment_size=5000
        )
    
    def test_initialization(self):
        """Test system initialization"""
        assert self.system.min_segment_size == 100
        assert self.system.max_segment_size == 5000
        assert len(self.system.segments_data) == 0
    
    def test_mock_data_generation(self):
        """Test mock data generation"""
        df = self.system.generate_mock_data(n_users=1000)
        
        # Check basic structure
        assert len(df) == 1000
        assert 'user_id' in df.columns
        assert 'cart_abandoned_date' in df.columns
        assert 'avg_order_value' in df.columns
        assert 'engagement_score' in df.columns
        
        # Check data types
        assert df['user_id'].dtype == 'object'
        assert df['avg_order_value'].dtype == 'float64'
        assert df['engagement_score'].dtype == 'float64'
        
        # Check value ranges
        assert df['engagement_score'].min() >= 0
        assert df['engagement_score'].max() <= 1
        assert df['avg_order_value'].min() > 0
    
    def test_universe_definition(self):
        """Test universe definition logic"""
        df = self.system.generate_mock_data(n_users=1000)
        universe = self.system.define_universe(df)
        
        # Check that universe only contains recent cart abandoners
        cutoff_date = datetime.now() - timedelta(days=7)
        assert all(universe['cart_abandoned_date'] >= cutoff_date)
        assert len(universe) <= len(df)
    
    def test_recency_score_calculation(self):
        """Test recency score calculation"""
        df = self.system.generate_mock_data(n_users=100)
        recency_scores = self.system.calculate_recency_score(df)
        
        # Check score range
        assert all(recency_scores >= 0)
        assert all(recency_scores <= 1)
        
        # Check that more recent dates get higher scores
        recent_date = datetime.now() - timedelta(days=1)
        old_date = datetime.now() - timedelta(days=6)
        
        recent_df = pd.DataFrame({'cart_abandoned_date': [recent_date, old_date]})
        recent_scores = self.system.calculate_recency_score(recent_df)
        
        assert recent_scores.iloc[0] > recent_scores.iloc[1]
    
    def test_mece_segmentation(self):
        """Test MECE segmentation logic"""
        df = self.system.generate_mock_data(n_users=1000)
        universe = self.system.define_universe(df)
        segmented_df = self.system.create_mece_segments(universe)
        
        # Check that all users are segmented
        assert 'segment' in segmented_df.columns
        assert segmented_df['segment'].notna().all()
        
        # Check that segments are mutually exclusive and collectively exhaustive
        total_users = len(segmented_df)
        segmented_users = segmented_df['segment'].notna().sum()
        assert total_users == segmented_users
    
    def test_size_constraints(self):
        """Test size constraint application"""
        df = self.system.generate_mock_data(n_users=1000)
        universe = self.system.define_universe(df)
        segmented_df = self.system.create_mece_segments(universe)
        constrained_df = self.system.apply_size_constraints(segmented_df)
        
        # Check that no segments are below minimum size
        segment_counts = constrained_df['segment'].value_counts()
        assert all(segment_counts >= self.system.min_segment_size)
    
    def test_segment_scoring(self):
        """Test segment scoring calculation"""
        df = self.system.generate_mock_data(n_users=1000)
        universe = self.system.define_universe(df)
        segmented_df = self.system.create_mece_segments(universe)
        constrained_df = self.system.apply_size_constraints(segmented_df)
        scores_df = self.system.calculate_segment_scores(constrained_df)
        
        # Check required columns
        required_columns = [
            'segment_name', 'size', 'conversion_potential', 
            'lift_vs_control', 'overall_score'
        ]
        for col in required_columns:
            assert col in scores_df.columns
        
        # Check score ranges
        assert all(scores_df['conversion_potential'] >= 0)
        assert all(scores_df['conversion_potential'] <= 1)
        assert all(scores_df['overall_score'] >= 0)
    
    def test_complete_analysis(self):
        """Test complete analysis workflow"""
        segmented_data, segment_strategy = self.system.run_complete_analysis(n_users=1000)
        
        # Check outputs
        assert isinstance(segmented_data, pd.DataFrame)
        assert isinstance(segment_strategy, pd.DataFrame)
        
        # Check that analysis completed successfully
        assert len(segmented_data) > 0
        assert len(segment_strategy) > 0
        
        # Check MECE properties
        total_users = len(segmented_data)
        total_in_segments = segment_strategy['size'].sum()
        assert total_users == total_in_segments

class TestConfig:
    """Test configuration management"""
    
    def test_config_validation(self):
        """Test configuration validation"""
        # This should not raise an exception
        config.validate_config()
    
    def test_get_segmentation_config(self):
        """Test getting segmentation configuration"""
        seg_config = config.get_segmentation_config()
        
        assert 'min_segment_size' in seg_config
        assert 'max_segment_size' in seg_config
        assert 'engagement_high_threshold' in seg_config
        assert isinstance(seg_config['min_segment_size'], int)
        assert isinstance(seg_config['engagement_high_threshold'], float)

if __name__ == "__main__":
    pytest.main([__file__])
