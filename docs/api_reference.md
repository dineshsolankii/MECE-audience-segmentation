# API Reference

Complete reference for the MECE Audience Segmentation System classes and methods.

## MECESegmentationSystem

Main class for performing MECE audience segmentation.

### Constructor

```python
MECESegmentationSystem(min_segment_size=500, max_segment_size=20000)
```

**Parameters:**
- `min_segment_size` (int): Minimum number of users per segment
- `max_segment_size` (int): Maximum number of users per segment

### Methods

#### generate_mock_data

```python
generate_mock_data(n_users=50000) -> pd.DataFrame
```

Generates synthetic data for testing and demonstration.

**Parameters:**
- `n_users` (int): Number of users to generate

**Returns:**
- `pd.DataFrame`: Generated dataset with user data

**Columns:**
- `user_id`: Unique user identifier
- `cart_abandoned_date`: Date of cart abandonment
- `last_order_date`: Date of last order (can be None)
- `avg_order_value`: Average order value
- `sessions_last_30d`: Sessions in last 30 days
- `num_cart_items`: Number of items in cart
- `engagement_score`: Engagement score (0-1)
- `profitability_score`: Profitability score (0-1)

#### define_universe

```python
define_universe(df) -> pd.DataFrame
```

Defines the analysis universe (users who abandoned carts in last 7 days).

**Parameters:**
- `df` (pd.DataFrame): Input dataset

**Returns:**
- `pd.DataFrame`: Filtered dataset

#### calculate_recency_score

```python
calculate_recency_score(df) -> pd.Series
```

Calculates recency score based on cart abandonment date.

**Parameters:**
- `df` (pd.DataFrame): Dataset with cart_abandoned_date column

**Returns:**
- `pd.Series`: Recency scores (0-1, higher for more recent)

#### create_mece_segments

```python
create_mece_segments(df) -> pd.DataFrame
```

Creates MECE segments using decision tree approach.

**Parameters:**
- `df` (pd.DataFrame): Universe dataset

**Returns:**
- `pd.DataFrame`: Dataset with segment assignments

**Segments Created:**
- `Premium_Engaged`: High AOV + High Engagement
- `Premium_Profitable`: High AOV + High Profitability
- `Premium_Other`: High AOV + Other conditions
- `Mid_Value_Champions`: Medium AOV + High Engagement + High Profitability
- `Mid_Value_Engaged`: Medium AOV + High Engagement
- `Mid_Value_Active`: Medium AOV + High Activity
- `Mid_Value_Other`: Medium AOV + Other conditions
- `Low_Value_High_Engagement`: Low AOV + High Engagement
- `Low_Value_Moderate_Engaged`: Low AOV + Moderate Engagement
- `Low_Value_Other`: Low AOV + Other conditions

#### apply_size_constraints

```python
apply_size_constraints(df) -> pd.DataFrame
```

Applies minimum and maximum segment size constraints.

**Parameters:**
- `df` (pd.DataFrame): Segmented dataset

**Returns:**
- `pd.DataFrame`: Dataset with size constraints applied

#### calculate_segment_scores

```python
calculate_segment_scores(df) -> pd.DataFrame
```

Calculates weighted scores for each segment.

**Parameters:**
- `df` (pd.DataFrame): Segmented dataset

**Returns:**
- `pd.DataFrame`: Segment summary with scores

**Score Columns:**
- `conversion_potential`: Engagement × Recency (0-1)
- `lift_vs_control`: Expected performance improvement (0-1)
- `size_score`: Normalized segment size (0-1)
- `profitability`: Revenue potential (0-1)
- `strategic_fit`: Business value alignment (0-1)
- `overall_score`: Weighted combination (0-1)

#### run_complete_analysis

```python
run_complete_analysis(n_users=50000) -> Tuple[pd.DataFrame, pd.DataFrame]
```

Runs the complete MECE segmentation analysis.

**Parameters:**
- `n_users` (int): Number of users to analyze

**Returns:**
- `Tuple[pd.DataFrame, pd.DataFrame]`: (segmented_data, segment_strategy)

#### export_results

```python
export_results(segment_summary, filename_prefix="mece_segments") -> Tuple[str, str]
```

Exports results to CSV and JSON files.

**Parameters:**
- `segment_summary` (pd.DataFrame): Segment summary data
- `filename_prefix` (str): Prefix for output files

**Returns:**
- `Tuple[str, str]`: (csv_filename, json_filename)

### Private Methods

#### _validate_mece

```python
_validate_mece(df) -> None
```

Validates MECE properties (Mutually Exclusive, Collectively Exhaustive).

**Parameters:**
- `df` (pd.DataFrame): Segmented dataset

**Raises:**
- `ValueError`: If MECE properties are violated

#### _get_segment_rules

```python
_get_segment_rules(segment) -> str
```

Returns human-readable rules for a segment.

**Parameters:**
- `segment` (str): Segment name

**Returns:**
- `str`: Human-readable rules

## Config

Configuration management class.

### Class Methods

#### get_segmentation_config

```python
get_segmentation_config() -> Dict[str, Any]
```

Returns segmentation configuration parameters.

**Returns:**
- `Dict[str, Any]`: Configuration dictionary

#### get_data_config

```python
get_data_config() -> Dict[str, Any]
```

Returns data generation configuration.

**Returns:**
- `Dict[str, Any]`: Data configuration dictionary

#### validate_config

```python
validate_config() -> bool
```

Validates configuration parameters.

**Returns:**
- `bool`: True if valid

**Raises:**
- `ValueError`: If configuration is invalid

## Configuration Parameters

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_SEGMENT_SIZE` | 500 | Minimum users per segment |
| `MAX_SEGMENT_SIZE` | 20000 | Maximum users per segment |
| `DEFAULT_N_USERS` | 50000 | Default number of users to generate |
| `AOV_HIGH_PERCENTILE` | 80 | High AOV threshold percentile |
| `AOV_MEDIUM_PERCENTILE` | 50 | Medium AOV threshold percentile |
| `ENGAGEMENT_HIGH_THRESHOLD` | 0.7 | High engagement threshold |
| `ENGAGEMENT_MEDIUM_THRESHOLD` | 0.4 | Medium engagement threshold |
| `PROFITABILITY_HIGH_THRESHOLD` | 0.7 | High profitability threshold |
| `OUTPUT_DIR` | outputs | Output directory |
| `LOG_LEVEL` | INFO | Logging level |

## Data Types

### User Data Schema

```python
{
    'user_id': str,                    # Unique identifier
    'cart_abandoned_date': datetime,   # Cart abandonment date
    'last_order_date': datetime,       # Last order date (nullable)
    'avg_order_value': float,          # Average order value
    'sessions_last_30d': int,          # Sessions in last 30 days
    'num_cart_items': int,             # Items in abandoned cart
    'engagement_score': float,         # Engagement score (0-1)
    'profitability_score': float       # Profitability score (0-1)
}
```

### Segment Summary Schema

```python
{
    'segment_name': str,               # Segment identifier
    'rules_applied': str,              # Human-readable rules
    'size': int,                       # Number of users
    'conversion_potential': float,     # Conversion potential (0-1)
    'lift_vs_control': float,         # Expected lift (0-1)
    'size_score': float,              # Size score (0-1)
    'profitability': float,           # Profitability score (0-1)
    'strategic_fit': float,           # Strategic fit (0-1)
    'overall_score': float,           # Overall score (0-1)
    'valid': str,                     # Validation status
    'avg_aov': float,                 # Average AOV
    'avg_engagement': float,          # Average engagement
    'avg_sessions': float             # Average sessions
}
```

## Error Handling

### Common Exceptions

- `ValueError`: Configuration validation errors, MECE violations
- `KeyError`: Missing required columns in input data
- `TypeError`: Incorrect data types
- `FileNotFoundError`: Missing configuration files

### Example Error Handling

```python
try:
    system = MECESegmentationSystem()
    segmented_data, segment_strategy = system.run_complete_analysis()
except ValueError as e:
    print(f"Configuration error: {e}")
except KeyError as e:
    print(f"Missing required column: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Considerations

### Memory Usage

- Each 10,000 users requires approximately 1MB of memory
- Large datasets should be processed in chunks
- Consider using `dtype` optimization for large datasets

### Processing Time

- 10,000 users: ~1-2 seconds
- 100,000 users: ~10-20 seconds
- 1,000,000 users: ~2-5 minutes

### Optimization Tips

1. Use appropriate data types
2. Process data in chunks for large datasets
3. Cache intermediate results when possible
4. Use parallel processing for multiple datasets
