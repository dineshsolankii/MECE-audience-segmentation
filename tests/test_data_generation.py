"""
Tests for data generation functionality
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

class TestDataGeneration:
    """Test cases for data generation"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.system = MECESegmentationSystem()
    
    def test_data_shape(self):
        """Test that generated data has correct shape"""
        df = self.system.generate_mock_data(n_users=1000)
        assert len(df) == 1000
        assert len(df.columns) == 8  # Expected number of columns
    
    def test_user_id_uniqueness(self):
        """Test that user IDs are unique"""
        df = self.system.generate_mock_data(n_users=1000)
        assert df['user_id'].nunique() == len(df)
        assert df['user_id'].duplicated().sum() == 0
    
    def test_date_ranges(self):
        """Test that dates are within expected ranges"""
        df = self.system.generate_mock_data(n_users=1000)
        
        # Cart abandoned dates should be within last 7 days
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        assert all(df['cart_abandoned_date'] >= seven_days_ago)
        assert all(df['cart_abandoned_date'] <= now)
        
        # Last order dates should be in the past or None
        valid_order_dates = df['last_order_date'].dropna()
        if len(valid_order_dates) > 0:
            assert all(valid_order_dates <= now)
    
    def test_numerical_ranges(self):
        """Test that numerical values are within expected ranges"""
        df = self.system.generate_mock_data(n_users=1000)
        
        # AOV should be positive
        assert all(df['avg_order_value'] > 0)
        
        # Sessions should be non-negative integers
        assert all(df['sessions_last_30d'] >= 0)
        assert df['sessions_last_30d'].dtype == 'int64'
        
        # Engagement and profitability scores should be 0-1
        assert all(df['engagement_score'] >= 0)
        assert all(df['engagement_score'] <= 1)
        assert all(df['profitability_score'] >= 0)
        assert all(df['profitability_score'] <= 1)
        
        # Cart items should be positive integers
        assert all(df['num_cart_items'] > 0)
        assert df['num_cart_items'].dtype == 'int64'
    
    def test_data_correlation(self):
        """Test that data shows expected correlations"""
        df = self.system.generate_mock_data(n_users=1000)
        
        # High AOV users should tend to have more cart items
        high_aov = df['avg_order_value'] > df['avg_order_value'].quantile(0.75)
        high_aov_cart_items = df[high_aov]['num_cart_items'].mean()
        low_aov_cart_items = df[~high_aov]['num_cart_items'].mean()
        
        # This is a probabilistic test, so we check for reasonable difference
        assert high_aov_cart_items > low_aov_cart_items * 0.8
        
        # Engagement should correlate with sessions
        engagement_sessions_corr = df['engagement_score'].corr(df['sessions_last_30d'])
        assert engagement_sessions_corr > 0.3  # Positive correlation
    
    def test_reproducibility(self):
        """Test that data generation is reproducible"""
        # Generate two datasets with same seed
        df1 = self.system.generate_mock_data(n_users=100)
        df2 = self.system.generate_mock_data(n_users=100)
        
        # Should be identical due to fixed seed
        pd.testing.assert_frame_equal(df1, df2)
    
    def test_different_sizes(self):
        """Test data generation with different user counts"""
        for n_users in [100, 1000, 5000]:
            df = self.system.generate_mock_data(n_users=n_users)
            assert len(df) == n_users
            assert df['user_id'].nunique() == n_users

if __name__ == "__main__":
    pytest.main([__file__])
