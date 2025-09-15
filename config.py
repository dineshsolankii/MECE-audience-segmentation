"""
Configuration management for MECE Audience Segmentation System
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the MECE segmentation system"""
    
    # Data Configuration
    MIN_SEGMENT_SIZE = int(os.getenv('MIN_SEGMENT_SIZE', '500'))
    MAX_SEGMENT_SIZE = int(os.getenv('MAX_SEGMENT_SIZE', '20000'))
    DEFAULT_N_USERS = int(os.getenv('DEFAULT_N_USERS', '50000'))
    
    # Analysis Configuration
    AOV_HIGH_PERCENTILE = int(os.getenv('AOV_HIGH_PERCENTILE', '80'))
    AOV_MEDIUM_PERCENTILE = int(os.getenv('AOV_MEDIUM_PERCENTILE', '50'))
    ENGAGEMENT_HIGH_THRESHOLD = float(os.getenv('ENGAGEMENT_HIGH_THRESHOLD', '0.7'))
    ENGAGEMENT_MEDIUM_THRESHOLD = float(os.getenv('ENGAGEMENT_MEDIUM_THRESHOLD', '0.4'))
    PROFITABILITY_HIGH_THRESHOLD = float(os.getenv('PROFITABILITY_HIGH_THRESHOLD', '0.7'))
    
    # Output Configuration
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'outputs')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Database Configuration (for future use)
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    
    # API Configuration (for future use)
    API_KEY = os.getenv('API_KEY', '')
    API_BASE_URL = os.getenv('API_BASE_URL', '')
    
    @classmethod
    def get_segmentation_config(cls) -> Dict[str, Any]:
        """Get configuration for segmentation parameters"""
        return {
            'min_segment_size': cls.MIN_SEGMENT_SIZE,
            'max_segment_size': cls.MAX_SEGMENT_SIZE,
            'aov_high_percentile': cls.AOV_HIGH_PERCENTILE,
            'aov_medium_percentile': cls.AOV_MEDIUM_PERCENTILE,
            'engagement_high_threshold': cls.ENGAGEMENT_HIGH_THRESHOLD,
            'engagement_medium_threshold': cls.ENGAGEMENT_MEDIUM_THRESHOLD,
            'profitability_high_threshold': cls.PROFITABILITY_HIGH_THRESHOLD
        }
    
    @classmethod
    def get_data_config(cls) -> Dict[str, Any]:
        """Get configuration for data generation"""
        return {
            'default_n_users': cls.DEFAULT_N_USERS,
            'output_dir': cls.OUTPUT_DIR
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration parameters"""
        errors = []
        
        if cls.MIN_SEGMENT_SIZE <= 0:
            errors.append("MIN_SEGMENT_SIZE must be positive")
        
        if cls.MAX_SEGMENT_SIZE <= cls.MIN_SEGMENT_SIZE:
            errors.append("MAX_SEGMENT_SIZE must be greater than MIN_SEGMENT_SIZE")
        
        if not (0 <= cls.ENGAGEMENT_HIGH_THRESHOLD <= 1):
            errors.append("ENGAGEMENT_HIGH_THRESHOLD must be between 0 and 1")
        
        if not (0 <= cls.ENGAGEMENT_MEDIUM_THRESHOLD <= 1):
            errors.append("ENGAGEMENT_MEDIUM_THRESHOLD must be between 0 and 1")
        
        if not (0 <= cls.PROFITABILITY_HIGH_THRESHOLD <= 1):
            errors.append("PROFITABILITY_HIGH_THRESHOLD must be between 0 and 1")
        
        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
        
        return True

# Create global config instance
config = Config()

# Validate configuration on import
config.validate_config()
