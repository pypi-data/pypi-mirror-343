# OutlierCleaner

A Python package for detecting and removing outliers in data using various statistical methods and advanced distribution analysis.

## Features

- Automatic method selection based on data distribution
- Multiple outlier detection methods:
  - IQR (Interquartile Range)
  - Z-score
  - Modified Z-score (robust to non-normal distributions)
- Advanced distribution analysis and method recommendations
- Comprehensive visualization tools
- Progress tracking for batch operations
- Index preservation options
- Outlier tracking and statistics
- Method comparison and agreement analysis
- Robust handling of edge cases (zero MAD, constant columns)

## Installation

```bash
pip install outlier-cleaner
```

## Usage

Here's a comprehensive example using the California Housing dataset:

```python
import pandas as pd
from sklearn.datasets import fetch_california_housing
from outlier_cleaner import OutlierCleaner

# Load California Housing dataset
housing = fetch_california_housing()
df = pd.DataFrame(housing.data, columns=housing.feature_names)
df['PRICE'] = housing.target

# Initialize cleaner with index preservation
cleaner = OutlierCleaner(df, preserve_index=True)

# Analyze distributions and get method recommendations
for column in ['MedInc', 'AveRooms', 'PRICE']:
    analysis = cleaner.analyze_distribution(column)
    print(f"\n{column} Analysis:")
    print(f"- Skewness: {analysis['skewness']:.2f}")
    print(f"- Recommended method: {analysis['recommended_method']}")

# Get outlier statistics
stats = cleaner.get_outlier_stats(['MedInc', 'AveRooms', 'PRICE'])
print(f"\nPotential outliers in MedInc: {stats['MedInc']['iqr']['potential_outliers']}")

# Clean data with automatic method selection
cleaned_df, info = cleaner.clean_columns(
    columns=['MedInc', 'AveRooms', 'PRICE'],
    method='auto',
    show_progress=True
)

# Get outlier indices
outliers = cleaner.get_outlier_indices('MedInc')
print(f"\nOutlier indices for MedInc: {outliers['MedInc'][:5]}")

# Visualize results
figures = cleaner.plot_outlier_analysis(['MedInc', 'AveRooms', 'PRICE'])
# figures['MedInc'].show()  # Display the figure for MedInc

# Compare methods
comparison = cleaner.compare_methods(['MedInc', 'PRICE'])
print(comparison['MedInc']['summary'])
```

## Methods

### analyze_distribution(column)
Analyze the distribution of a column and recommend the best outlier detection method.
- Calculates skewness, kurtosis, and normality tests
- Recommends the most appropriate method and thresholds
- Returns detailed distribution analysis

### clean_columns(columns=None, method='auto', show_progress=True)
Clean multiple columns using the most appropriate method for each column.
- Automatic method selection based on distribution analysis
- Progress bar for tracking cleaning operations
- Returns cleaned DataFrame and outlier information

### remove_outliers_modified_zscore(column, threshold=3.5)
Remove outliers using the Modified Z-score method (robust to non-normal distributions).
- Uses Median Absolute Deviation (MAD) instead of standard deviation
- Automatically handles zero MAD cases
- Returns cleaned DataFrame and outlier information

### get_outlier_indices(column=None)
Get the indices of outliers for specified column(s).
- Returns dictionary mapping columns to outlier indices
- Handles missing columns gracefully by returning empty lists
- Useful for tracking and analyzing removed data points
- Can retrieve indices for a specific column or all processed columns

### get_outlier_stats()
Get comprehensive outlier statistics without removing data points.
- Provides potential outlier counts and percentages
- Calculates bounds and thresholds for each method
- Returns detailed statistics for analysis and comparison

### Additional Methods
- `plot_outlier_analysis()`: Create detailed visualizations
- `compare_methods()`: Compare different detection methods
- `add_zscore_columns()`: Add Z-score columns for analysis
- `clean_zscore_columns()`: Clean using Z-score thresholds
- `remove_outliers_iqr()`: Clean using IQR method
- `remove_outliers_zscore()`: Clean using Z-score method

## Requirements

- numpy>=1.20.0
- pandas>=1.3.0
- matplotlib>=3.4.0
- seaborn>=0.11.0
- scipy>=1.7.0
- scikit-learn>=0.24.0 (for examples)
- tqdm>=4.62.0

## Changelog

### Version 1.0.2
- Enhanced outlier indices tracking in all removal methods
- Improved `get_outlier_indices()` to handle missing columns gracefully
- Optimized outlier statistics calculation
- Removed redundant outlier indices from `get_outlier_stats()` output

### Version 1.0.1
- Fixed author name spelling
- Updated documentation and examples
- Added comprehensive test coverage

### Version 1.0.0
- Initial release with core functionality
- Added distribution analysis and automatic method selection
- Implemented visualization tools and progress tracking

## Author

Subashanan Nair

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License 