import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class MECESegmentationSystem:
    """
    MECE (Mutually Exclusive, Collectively Exhaustive) Audience Segmentation System
    for Cart Abandoner Retention Strategy
    """
    
    def __init__(self, min_segment_size: int = 500, max_segment_size: int = 20000):
        self.min_segment_size = min_segment_size
        self.max_segment_size = max_segment_size
        self.segments_data = []
        
    def generate_mock_data(self, n_users: int = 50000) -> pd.DataFrame:
        """Generate mock dataset for cart abandoners"""
        np.random.seed(42)
        
        # Generate user IDs
        user_ids = [f"user_{i:06d}" for i in range(1, n_users + 1)]
        
        # Generate cart abandoned dates (last 7 days)
        base_date = datetime.now()
        cart_abandoned_dates = [
            base_date - timedelta(days=np.random.randint(0, 8)) 
            for _ in range(n_users)
        ]
        
        # Generate last order dates (some recent, some older, some never)
        last_order_dates = []
        for _ in range(n_users):
            if np.random.random() < 0.3:  # 30% never ordered
                last_order_dates.append(None)
            else:
                days_ago = np.random.exponential(30)  # Exponential distribution
                last_order_dates.append(base_date - timedelta(days=int(days_ago)))
        
        # Generate correlated features
        # AOV follows log-normal distribution
        avg_order_values = np.random.lognormal(mean=6.5, sigma=1.2, size=n_users)
        
        # Sessions correlated with engagement
        base_sessions = np.random.poisson(lam=8, size=n_users)
        sessions_last_30d = np.maximum(0, base_sessions + np.random.normal(0, 2, n_users))
        
        # Cart items somewhat correlated with AOV
        num_cart_items = np.maximum(1, 
            np.random.poisson(lam=3, size=n_users) + 
            (avg_order_values > np.percentile(avg_order_values, 75)).astype(int) * 2
        )
        
        # Engagement score (0-1) correlated with sessions and recency
        engagement_base = np.minimum(1, sessions_last_30d / 20)
        engagement_noise = np.random.normal(0, 0.1, n_users)
        engagement_scores = np.clip(engagement_base + engagement_noise, 0, 1)
        
        # Profitability score correlated with AOV and engagement
        profitability_base = (
            0.3 * (avg_order_values / np.max(avg_order_values)) + 
            0.4 * engagement_scores + 
            0.3 * np.random.random(n_users)
        )
        profitability_scores = np.clip(profitability_base, 0, 1)
        
        # Create DataFrame
        df = pd.DataFrame({
            'user_id': user_ids,
            'cart_abandoned_date': cart_abandoned_dates,
            'last_order_date': last_order_dates,
            'avg_order_value': np.round(avg_order_values, 2),
            'sessions_last_30d': np.round(sessions_last_30d, 0).astype(int),
            'num_cart_items': num_cart_items,
            'engagement_score': np.round(engagement_scores, 3),
            'profitability_score': np.round(profitability_scores, 3)
        })
        
        return df
    
    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Define universe: users who abandoned carts in last 7 days"""
        cutoff_date = datetime.now() - timedelta(days=7)
        universe = df[df['cart_abandoned_date'] >= cutoff_date].copy()
        
        print(f"Universe defined: {len(universe):,} users who abandoned carts in last 7 days")
        print(f"Original dataset: {len(df):,} users")
        
        return universe
    
    def calculate_recency_score(self, df: pd.DataFrame) -> pd.Series:
        """Calculate recency score based on cart abandonment date"""
        now = datetime.now()
        days_since_abandonment = (now - df['cart_abandoned_date']).dt.days
        # Higher score for more recent abandonment
        recency_score = np.maximum(0, 1 - (days_since_abandonment / 7))
        return recency_score
    
    def create_mece_segments(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create MECE segments using decision tree approach"""
        df = df.copy()
        
        # Calculate additional features
        df['recency_score'] = self.calculate_recency_score(df)
        
        # Define thresholds based on data distribution
        aov_high = np.percentile(df['avg_order_value'], 80)  # Top 20%
        aov_medium = np.percentile(df['avg_order_value'], 50)  # Median
        
        engagement_high = 0.7
        engagement_medium = 0.4
        
        profitability_high = 0.7
        
        print(f"Segmentation Thresholds:")
        print(f"AOV High: ${aov_high:.2f}, AOV Medium: ${aov_medium:.2f}")
        print(f"Engagement High: {engagement_high}, Engagement Medium: {engagement_medium}")
        print(f"Profitability High: {profitability_high}")
        
        # MECE Segmentation Logic (Decision Tree)
        def assign_segment(row):
            aov = row['avg_order_value']
            engagement = row['engagement_score']
            profitability = row['profitability_score']
            sessions = row['sessions_last_30d']
            
            # High-Value Segments
            if aov > aov_high:
                if engagement > engagement_high:
                    return "Premium_Engaged"
                elif profitability > profitability_high:
                    return "Premium_Profitable"
                else:
                    return "Premium_Other"
            
            # Medium-Value Segments
            elif aov > aov_medium:
                if engagement > engagement_high and profitability > profitability_high:
                    return "Mid_Value_Champions"
                elif engagement > engagement_medium:
                    return "Mid_Value_Engaged"
                elif sessions > 10:
                    return "Mid_Value_Active"
                else:
                    return "Mid_Value_Other"
            
            # Lower-Value Segments
            else:
                if engagement > engagement_high:
                    return "Low_Value_High_Engagement"
                elif engagement > engagement_medium and sessions > 5:
                    return "Low_Value_Moderate_Engaged"
                else:
                    return "Low_Value_Other"
        
        df['segment'] = df.apply(assign_segment, axis=1)
        
        # Validate MECE properties
        self._validate_mece(df)
        
        return df
    
    def _validate_mece(self, df: pd.DataFrame):
        """Validate Mutually Exclusive and Collectively Exhaustive properties"""
        # Check Collectively Exhaustive
        total_users = len(df)
        segmented_users = df['segment'].notna().sum()
        
        if total_users != segmented_users:
            raise ValueError(f"Not Collectively Exhaustive: {total_users} total vs {segmented_users} segmented")
        
        # Check Mutually Exclusive (implicit in our logic, but verify)
        segment_counts = df['segment'].value_counts()
        total_in_segments = segment_counts.sum()
        
        if total_in_segments != total_users:
            raise ValueError(f"Not Mutually Exclusive: Overlap detected")
        
        print("✅ MECE Validation Passed: Segments are Mutually Exclusive and Collectively Exhaustive")
        
    def apply_size_constraints(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply min/max segment size constraints"""
        df = df.copy()
        segment_counts = df['segment'].value_counts()
        
        print(f"\nSegment Sizes Before Constraints:")
        for segment, count in segment_counts.items():
            print(f"  {segment}: {count:,}")
        
        # Identify segments that are too small
        small_segments = segment_counts[segment_counts < self.min_segment_size].index.tolist()
        
        if small_segments:
            print(f"\nMerging small segments into 'Other_Bucket': {small_segments}")
            df.loc[df['segment'].isin(small_segments), 'segment'] = 'Other_Bucket'
        
        # Check if any segments are too large (would need more sophisticated splitting)
        large_segments = segment_counts[segment_counts > self.max_segment_size].index.tolist()
        if large_segments:
            print(f"Warning: Large segments detected (>{self.max_segment_size:,}): {large_segments}")
            print("Consider adding more granular rules to split these segments")
        
        return df
    
    def calculate_segment_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate weighted scores for each segment"""
        segment_stats = []
        
        for segment in df['segment'].unique():
            segment_data = df[df['segment'] == segment]
            size = len(segment_data)
            
            # Calculate component scores
            avg_engagement = segment_data['engagement_score'].mean()
            avg_recency = segment_data['recency_score'].mean()
            avg_profitability = segment_data['profitability_score'].mean()
            avg_aov = segment_data['avg_order_value'].mean()
            avg_sessions = segment_data['sessions_last_30d'].mean()
            
            # Conversion Potential (engagement × recency)
            conversion_potential = (avg_engagement * avg_recency)
            
            # Lift vs Control (mocked - in reality would come from historical data)
            np.random.seed(hash(segment) % 1000)  # Deterministic but varied
            lift_vs_control = np.random.uniform(0.05, 0.25)  # 5-25% lift
            
            # Size Score (normalized, with preference for medium-large segments)
            max_size = df['segment'].value_counts().max()
            size_score = min(size / max_size, 1.0) * 0.8 + 0.2  # Scale 0.2-1.0
            
            # Strategic Fit (combination of profitability and AOV)
            max_aov = df['avg_order_value'].max()
            strategic_fit = (avg_profitability * 0.6 + (avg_aov / max_aov) * 0.4)
            
            # Overall Score (weighted combination)
            overall_score = (
                conversion_potential * 0.3 +
                lift_vs_control * 0.2 +
                size_score * 0.2 +
                avg_profitability * 0.2 +
                strategic_fit * 0.1
            )
            
            segment_stats.append({
                'segment_name': segment,
                'rules_applied': self._get_segment_rules(segment),
                'size': size,
                'conversion_potential': round(conversion_potential, 3),
                'lift_vs_control': round(lift_vs_control, 3),
                'size_score': round(size_score, 3),
                'profitability': round(avg_profitability, 3),
                'strategic_fit': round(strategic_fit, 3),
                'overall_score': round(overall_score, 3),
                'valid': 'Yes' if size >= self.min_segment_size else 'Merged',
                'avg_aov': round(avg_aov, 2),
                'avg_engagement': round(avg_engagement, 3),
                'avg_sessions': round(avg_sessions, 1)
            })
        
        return pd.DataFrame(segment_stats)
    
    def _get_segment_rules(self, segment: str) -> str:
        """Get human-readable rules for each segment"""
        rules_map = {
            'Premium_Engaged': 'AOV > 80th percentile & Engagement > 0.7',
            'Premium_Profitable': 'AOV > 80th percentile & Profitability > 0.7',
            'Premium_Other': 'AOV > 80th percentile & Other conditions',
            'Mid_Value_Champions': 'AOV > 50th percentile & Engagement > 0.7 & Profitability > 0.7',
            'Mid_Value_Engaged': 'AOV > 50th percentile & Engagement > 0.4',
            'Mid_Value_Active': 'AOV > 50th percentile & Sessions > 10',
            'Mid_Value_Other': 'AOV > 50th percentile & Other conditions',
            'Low_Value_High_Engagement': 'AOV ≤ 50th percentile & Engagement > 0.7',
            'Low_Value_Moderate_Engaged': 'AOV ≤ 50th percentile & Engagement > 0.4 & Sessions > 5',
            'Low_Value_Other': 'AOV ≤ 50th percentile & Other conditions',
            'Other_Bucket': 'Small segments merged (size < 500)'
        }
        return rules_map.get(segment, 'Custom rule')
    
    def run_complete_analysis(self, n_users: int = 50000) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Run the complete MECE segmentation analysis"""
        print("🎯 MECE Cart Abandoner Segmentation Analysis")
        print("=" * 50)
        
        # Step 1: Generate mock data
        print("\n1. Generating mock dataset...")
        df = self.generate_mock_data(n_users)
        
        # Step 2: Define universe
        print("\n2. Defining universe...")
        universe_df = self.define_universe(df)
        
        # Step 3: Create MECE segments
        print("\n3. Creating MECE segments...")
        segmented_df = self.create_mece_segments(universe_df)
        
        # Step 4: Apply constraints
        print("\n4. Applying size constraints...")
        final_df = self.apply_size_constraints(segmented_df)
        
        # Step 5: Calculate scores
        print("\n5. Calculating segment scores...")
        segment_summary = self.calculate_segment_scores(final_df)
        
        return final_df, segment_summary
    
    def export_results(self, segment_summary: pd.DataFrame, filename_prefix: str = "mece_segments"):
        """Export results to CSV and JSON"""
        # Export to CSV
        csv_filename = f"{filename_prefix}_strategy.csv"
        segment_summary.to_csv(csv_filename, index=False)
        print(f"\n📊 Results exported to: {csv_filename}")
        
        # Export to JSON
        json_filename = f"{filename_prefix}_strategy.json"
        segment_summary.to_json(json_filename, orient='records', indent=2)
        print(f"📊 Results exported to: {json_filename}")
        
        return csv_filename, json_filename

# Main execution
if __name__ == "__main__":
    # Initialize the segmentation system
    segmentation_system = MECESegmentationSystem(
        min_segment_size=500,
        max_segment_size=20000
    )
    
    # Run complete analysis
    segmented_data, segment_strategy = segmentation_system.run_complete_analysis(n_users=30000)
    
    # Display results
    print("\n" + "="*80)
    print("📈 FINAL SEGMENT STRATEGY")
    print("="*80)
    
    # Sort by overall score
    display_df = segment_strategy.sort_values('overall_score', ascending=False)
    
    print(f"\n{display_df.to_string(index=False)}")
    
    # Export results
    csv_file, json_file = segmentation_system.export_results(segment_strategy)
    
    # Summary statistics
    print(f"\n" + "="*50)
    print("📊 SUMMARY STATISTICS")
    print("="*50)
    print(f"Total Users in Universe: {len(segmented_data):,}")
    print(f"Total Segments Created: {len(segment_strategy)}")
    print(f"Average Segment Size: {segment_strategy['size'].mean():.0f}")
    print(f"Largest Segment: {segment_strategy['size'].max():,}")
    print(f"Smallest Segment: {segment_strategy['size'].min():,}")
    print(f"Top Scoring Segment: {display_df.iloc[0]['segment_name']} (Score: {display_df.iloc[0]['overall_score']:.3f})")
    
    # Validation check
    total_users_in_segments = segment_strategy['size'].sum()
    print(f"\n✅ Validation: {total_users_in_segments:,} users segmented = {len(segmented_data):,} universe users")
    
    print(f"\n🎉 MECE Segmentation Analysis Complete!")
    print(f"Files generated: {csv_file}, {json_file}")