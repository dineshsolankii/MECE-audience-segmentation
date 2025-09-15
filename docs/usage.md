# Usage Guide

This guide explains how to use the MECE Audience Segmentation System effectively.

## Quick Start

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

For a faster test run:

```bash
python setup.py
```

## Configuration

### Environment Variables

Configure the system using environment variables in your `.env` file:

```bash
# Data Configuration
MIN_SEGMENT_SIZE=500
MAX_SEGMENT_SIZE=20000
DEFAULT_N_USERS=50000

# Analysis Configuration
AOV_HIGH_PERCENTILE=80
AOV_MEDIUM_PERCENTILE=50
ENGAGEMENT_HIGH_THRESHOLD=0.7
ENGAGEMENT_MEDIUM_THRESHOLD=0.4
PROFITABILITY_HIGH_THRESHOLD=0.7
```

### Programmatic Configuration

```python
from config import config

# Get current configuration
seg_config = config.get_segmentation_config()
print(seg_config)

# Validate configuration
config.validate_config()
```

## Data Input

### Using Mock Data

The system includes mock data generation for testing:

```python
system = MECESegmentationSystem()
df = system.generate_mock_data(n_users=10000)
```

### Using Your Own Data

To use your own data, ensure your DataFrame has these columns:

- `user_id`: Unique identifier for each user
- `cart_abandoned_date`: Date when cart was abandoned
- `last_order_date`: Date of last order (can be None)
- `avg_order_value`: Average order value
- `sessions_last_30d`: Number of sessions in last 30 days
- `num_cart_items`: Number of items in abandoned cart
- `engagement_score`: Engagement score (0-1)
- `profitability_score`: Profitability score (0-1)

```python
# Load your data
import pandas as pd
df = pd.read_csv('your_data.csv')

# Ensure proper data types
df['cart_abandoned_date'] = pd.to_datetime(df['cart_abandoned_date'])
df['last_order_date'] = pd.to_datetime(df['last_order_date'])

# Run segmentation
universe = system.define_universe(df)
segmented_data = system.create_mece_segments(universe)
```

## Segmentation Process

### Step-by-Step Workflow

1. **Define Universe**: Filter users who abandoned carts in the last 7 days
2. **Create Segments**: Apply MECE segmentation logic
3. **Apply Constraints**: Ensure segment size requirements
4. **Calculate Scores**: Generate performance metrics
5. **Export Results**: Save to CSV and JSON

```python
# Step 1: Define universe
universe = system.define_universe(df)

# Step 2: Create segments
segmented_df = system.create_mece_segments(universe)

# Step 3: Apply constraints
final_df = system.apply_size_constraints(segmented_df)

# Step 4: Calculate scores
segment_summary = system.calculate_segment_scores(final_df)

# Step 5: Export results
csv_file, json_file = system.export_results(segment_summary)
```

## Understanding Outputs

### Segment Summary

The system generates a detailed segment summary with:

- **segment_name**: Name of the segment
- **size**: Number of users in segment
- **conversion_potential**: Engagement × Recency score
- **lift_vs_control**: Expected performance improvement
- **size_score**: Normalized segment size
- **profitability**: Revenue potential
- **strategic_fit**: Business value alignment
- **overall_score**: Weighted combination of all factors

### Interpreting Scores

- **Overall Score**: Higher is better (0-1 scale)
- **Conversion Potential**: Likelihood of conversion (0-1 scale)
- **Lift vs Control**: Expected improvement over baseline (0-1 scale)
- **Size Score**: Segment size relative to largest segment (0-1 scale)

## Customization

### Adding New Segments

Modify the segmentation logic in `create_mece_segments()`:

```python
def assign_segment(row):
    # Your custom logic here
    if row['custom_condition']:
        return "Custom_Segment"
    # ... existing logic
```

### Adjusting Scoring

Modify the scoring weights in `calculate_segment_scores()`:

```python
# Adjust weights for different priorities
overall_score = (
    conversion_potential * 0.4 +  # Increased weight
    lift_vs_control * 0.2 +
    size_score * 0.2 +
    avg_profitability * 0.1 +     # Decreased weight
    strategic_fit * 0.1
)
```

### Custom Data Sources

Replace mock data generation with your data loading:

```python
def load_real_data(self, data_source):
    # Your data loading logic
    return pd.DataFrame(...)
```

## Advanced Usage

### Batch Processing

Process multiple datasets:

```python
datasets = ['dataset1.csv', 'dataset2.csv', 'dataset3.csv']
results = []

for dataset in datasets:
    df = pd.read_csv(dataset)
    segmented_data, segment_strategy = system.run_complete_analysis(df)
    results.append((dataset, segment_strategy))
```

### Custom Constraints

Apply custom business rules:

```python
def apply_custom_constraints(self, df):
    # Your custom constraint logic
    df = df[df['custom_field'] > threshold]
    return df
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_segmentation.py
```

## Performance Optimization

### Large Datasets

For large datasets (>100k users):

```python
# Use chunking for memory efficiency
chunk_size = 10000
results = []

for chunk in pd.read_csv('large_dataset.csv', chunksize=chunk_size):
    segmented_chunk = system.create_mece_segments(chunk)
    results.append(segmented_chunk)

final_df = pd.concat(results, ignore_index=True)
```

### Parallel Processing

```python
from multiprocessing import Pool

def process_chunk(chunk):
    return system.create_mece_segments(chunk)

# Process chunks in parallel
with Pool() as pool:
    results = pool.map(process_chunk, data_chunks)
```

## Troubleshooting

### Common Issues

**Issue**: Segments are too small
- **Solution**: Decrease `min_segment_size` or adjust segmentation logic

**Issue**: Memory errors with large datasets
- **Solution**: Use chunking or increase available memory

**Issue**: Poor segment quality
- **Solution**: Adjust thresholds or add more segmentation dimensions

### Debug Mode

Enable debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run analysis with debug output
segmented_data, segment_strategy = system.run_complete_analysis(n_users=1000)
```

## Best Practices

1. **Start Small**: Begin with smaller datasets to test your configuration
2. **Validate Results**: Always check that segments meet MECE requirements
3. **Monitor Performance**: Track processing time and memory usage
4. **Document Changes**: Keep track of customizations and their impact
5. **Test Thoroughly**: Run the test suite after making changes
