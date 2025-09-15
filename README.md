# MECE Audience Segmentation System

A comprehensive Python system for creating Mutually Exclusive, Collectively Exhaustive (MECE) audience segments for cart abandoner retention strategies.

## 🎯 Overview

This system implements a sophisticated MECE segmentation approach that:
- Creates mutually exclusive and collectively exhaustive customer segments
- Focuses on cart abandoners for retention campaigns
- Uses multiple behavioral and value-based dimensions
- Applies business constraints for practical implementation
- Provides scoring and prioritization for each segment

## 🚀 Features

- **MECE Compliance**: Ensures segments are mutually exclusive and collectively exhaustive
- **Multi-dimensional Segmentation**: Uses AOV, engagement, profitability, and recency
- **Size Constraints**: Applies minimum and maximum segment size limits
- **Automated Scoring**: Calculates conversion potential, lift, and strategic fit
- **Export Capabilities**: Generates CSV and JSON outputs
- **Mock Data Generation**: Includes realistic synthetic data for testing

## 📁 Project Structure

```
├── app.py                          # Main segmentation system
├── setup.py                        # Quick demo script
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
├── LICENSE                        # MIT License
├── data/                          # Data directory
│   ├── raw/                       # Raw data files
│   ├── processed/                 # Processed data files
│   └── outputs/                   # Generated outputs
├── tests/                         # Test files
│   ├── __init__.py
│   ├── test_segmentation.py
│   └── test_data_generation.py
└── docs/                          # Documentation
    ├── installation.md
    ├── usage.md
    └── api_reference.md
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mece-audience-segmentation
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 🚀 Quick Start

### Basic Usage

```python
from app import MECESegmentationSystem

# Initialize the system
system = MECESegmentationSystem(
    min_segment_size=500,
    max_segment_size=20000
)

# Run complete analysis
segmented_data, segment_strategy = system.run_complete_analysis(n_users=30000)

# Export results
csv_file, json_file = system.export_results(segment_strategy)
```

### Quick Demo

Run the included demo script for a faster test:

```bash
python setup.py
```

## 📊 Segmentation Logic

The system creates segments based on a decision tree approach:

### High-Value Segments (AOV > 80th percentile)
- **Premium_Engaged**: High AOV + High Engagement
- **Premium_Profitable**: High AOV + High Profitability  
- **Premium_Other**: High AOV + Other conditions

### Medium-Value Segments (AOV > 50th percentile)
- **Mid_Value_Champions**: High Engagement + High Profitability
- **Mid_Value_Engaged**: High Engagement
- **Mid_Value_Active**: High Session Activity
- **Mid_Value_Other**: Other conditions

### Low-Value Segments (AOV ≤ 50th percentile)
- **Low_Value_High_Engagement**: High Engagement
- **Low_Value_Moderate_Engaged**: Moderate Engagement + Activity
- **Low_Value_Other**: Other conditions

## 🎯 Scoring Methodology

Each segment receives scores for:

- **Conversion Potential**: Engagement × Recency
- **Lift vs Control**: Expected performance improvement
- **Size Score**: Normalized segment size
- **Profitability**: Revenue potential
- **Strategic Fit**: Business value alignment
- **Overall Score**: Weighted combination of all factors

## 📈 Output Files

The system generates:

- **CSV File**: Detailed segment statistics and scores
- **JSON File**: Machine-readable segment data
- **Console Output**: Real-time analysis progress and results

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## 📚 Configuration

Key parameters can be configured via environment variables or direct initialization:

- `MIN_SEGMENT_SIZE`: Minimum users per segment (default: 500)
- `MAX_SEGMENT_SIZE`: Maximum users per segment (default: 20000)
- `AOV_HIGH_PERCENTILE`: High AOV threshold (default: 80th percentile)
- `ENGAGEMENT_HIGH_THRESHOLD`: High engagement threshold (default: 0.7)

## 🔧 Customization

### Adding New Segments

Modify the `assign_segment` method in `create_mece_segments()` to add new segmentation logic.

### Adjusting Scoring

Update the `calculate_segment_scores()` method to modify scoring weights and calculations.

### Custom Data Sources

Replace `generate_mock_data()` with your data loading logic.

## 📋 Requirements

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.21.0
- scikit-learn >= 1.1.0

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Version History

- **v1.0.0**: Initial release with MECE segmentation system
- Basic scoring and export functionality
- Mock data generation
- Size constraint handling
