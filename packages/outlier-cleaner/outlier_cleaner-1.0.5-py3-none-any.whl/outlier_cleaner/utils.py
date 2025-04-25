"""
Utility functions for outlier visualization and plotting.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Union, Optional

def plot_outliers(data: Union[pd.Series, np.ndarray], 
                 outliers: Union[pd.Series, np.ndarray],
                 title: Optional[str] = None,
                 figsize: tuple = (10, 6)) -> None:
    """
    Plot data points highlighting the outliers.
    
    Parameters
    ----------
    data : Union[pd.Series, np.ndarray]
        The original data points
    outliers : Union[pd.Series, np.ndarray]
        Boolean mask or indices indicating outlier points
    title : Optional[str]
        Title for the plot
    figsize : tuple
        Figure size as (width, height)
    """
    plt.figure(figsize=figsize)
    
    # Convert data to numpy array if it's a pandas Series
    if isinstance(data, pd.Series):
        data = data.values
    if isinstance(outliers, pd.Series):
        outliers = outliers.values
    
    # Create index array for x-axis
    x = np.arange(len(data))
    
    # Plot all points
    plt.scatter(x[~outliers], data[~outliers], c='blue', label='Normal Points')
    plt.scatter(x[outliers], data[outliers], c='red', label='Outliers')
    
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title(title or 'Outlier Detection Results')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_distribution(data: Union[pd.Series, np.ndarray],
                     outliers: Optional[Union[pd.Series, np.ndarray]] = None,
                     title: Optional[str] = None,
                     figsize: tuple = (10, 6)) -> None:
    """
    Plot the distribution of data points with optional outlier highlighting.
    
    Parameters
    ----------
    data : Union[pd.Series, np.ndarray]
        The data points to plot
    outliers : Optional[Union[pd.Series, np.ndarray]]
        Boolean mask or indices indicating outlier points
    title : Optional[str]
        Title for the plot
    figsize : tuple
        Figure size as (width, height)
    """
    plt.figure(figsize=figsize)
    
    # Convert to numpy arrays if needed
    if isinstance(data, pd.Series):
        data = data.values
    if isinstance(outliers, pd.Series):
        outliers = outliers.values if outliers is not None else None
    
    if outliers is not None:
        # Plot separate distributions for normal points and outliers
        sns.kdeplot(data[~outliers], label='Normal Points', color='blue')
        sns.kdeplot(data[outliers], label='Outliers', color='red')
        plt.legend()
    else:
        # Plot single distribution if no outliers specified
        sns.kdeplot(data, color='blue')
    
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title(title or 'Data Distribution')
    plt.grid(True, alpha=0.3)
    plt.show() 