"""
outlier_cleaner - A Python package for detecting and removing outliers in data

This package provides tools for identifying and removing outliers using various
statistical methods such as IQR and Z-score.
"""

__version__ = '0.1.0'
__author__ = 'Subashan Annai'

from .cleaner import OutlierCleaner
from .utils import plot_outliers, plot_distribution

__all__ = ['OutlierCleaner', 'plot_outliers', 'plot_distribution'] 