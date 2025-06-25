import pandas as pd
import numpy as np
from datetime import datetime
import re
import os

def load_csv(file_path_or_buffer, **kwargs):
    """
    Load a CSV file into a pandas DataFrame.
    
    Args:
        file_path_or_buffer: Path to the CSV file or file-like object
        **kwargs: Additional arguments to pass to pd.read_csv
        
    Returns:
        pd.DataFrame: The loaded DataFrame
    """
    try:
        df = pd.read_csv(file_path_or_buffer, **kwargs)
        return df
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        return None

def detect_column_types(df):
    """
    Detect the types of columns in a DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
        
    Returns:
        dict: Dictionary mapping column names to detected types
    """
    column_types = {}
    
    for column in df.columns:
        # Get the pandas dtype
        dtype = df[column].dtype
        
        # Check if column is numeric
        if pd.api.types.is_numeric_dtype(dtype):
            # Check if it's an integer or float
            if pd.api.types.is_integer_dtype(dtype):
                column_types[column] = "integer"
            else:
                column_types[column] = "float"
        
        # Check if column is datetime
        elif pd.api.types.is_datetime64_dtype(dtype):
            column_types[column] = "datetime"
        
        # Check if column is boolean
        elif pd.api.types.is_bool_dtype(dtype):
            column_types[column] = "boolean"
        
        # Check if column is categorical
        elif pd.api.types.is_categorical_dtype(dtype):
            column_types[column] = "categorical"
        
        # Otherwise, it's a string/object
        else:
            # Try to infer if it's a date
            if df[column].dtype == 'object':
                # Check if it looks like a date
                date_pattern = r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}$'
                sample = df[column].dropna().head(10)
                if all(isinstance(x, str) and re.match(date_pattern, x) for x in sample):
                    column_types[column] = "date"
                else:
                    # Check if it's a categorical with few unique values
                    unique_count = df[column].nunique()
                    if unique_count <= 20 or (unique_count / len(df) < 0.05 and unique_count <= 100):
                        column_types[column] = "categorical"
                    else:
                        column_types[column] = "text"
            else:
                column_types[column] = "text"
    
    return column_types

def calculate_summary_statistics(df, column):
    """
    Calculate summary statistics for a numeric column.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column
        column (str): The name of the column to analyze
        
    Returns:
        dict: Dictionary of summary statistics
    """
    # Check if column is numeric
    if not pd.api.types.is_numeric_dtype(df[column]):
        return None
    
    # Calculate basic statistics
    stats = {
        "count": df[column].count(),
        "mean": df[column].mean(),
        "median": df[column].median(),
        "std": df[column].std(),
        "min": df[column].min(),
        "max": df[column].max(),
        "q1": df[column].quantile(0.25),
        "q3": df[column].quantile(0.75),
        "iqr": df[column].quantile(0.75) - df[column].quantile(0.25),
        "skew": df[column].skew(),
        "kurtosis": df[column].kurtosis()
    }
    
    # Calculate additional statistics
    stats["range"] = stats["max"] - stats["min"]
    stats["cv"] = stats["std"] / stats["mean"] if stats["mean"] != 0 else np.nan
    
    # Calculate outlier bounds
    stats["lower_bound"] = stats["q1"] - 1.5 * stats["iqr"]
    stats["upper_bound"] = stats["q3"] + 1.5 * stats["iqr"]
    
    # Count outliers
    outliers = df[(df[column] < stats["lower_bound"]) | (df[column] > stats["upper_bound"])][column]
    stats["outlier_count"] = len(outliers)
    stats["outlier_pct"] = stats["outlier_count"] / stats["count"] if stats["count"] > 0 else 0
    
    return stats

def calculate_categorical_statistics(df, column):
    """
    Calculate statistics for a categorical column.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column
        column (str): The name of the column to analyze
        
    Returns:
        dict: Dictionary of categorical statistics
    """
    # Get value counts
    value_counts = df[column].value_counts()
    
    # Calculate statistics
    stats = {
        "count": df[column].count(),
        "unique_count": df[column].nunique(),
        "missing_count": df[column].isna().sum(),
        "mode": df[column].mode()[0] if not df[column].mode().empty else None,
        "mode_count": value_counts.iloc[0] if not value_counts.empty else 0,
        "mode_pct": value_counts.iloc[0] / df[column].count() if not value_counts.empty and df[column].count() > 0 else 0,
        "entropy": calculate_entropy(df[column])
    }
    
    # Calculate missing percentage
    stats["missing_pct"] = stats["missing_count"] / len(df) if len(df) > 0 else 0
    
    # Get top categories
    top_n = min(10, len(value_counts))
    stats["top_categories"] = {
        "categories": value_counts.index[:top_n].tolist(),
        "counts": value_counts.values[:top_n].tolist(),
        "percentages": (value_counts.values[:top_n] / df[column].count() * 100).tolist() if df[column].count() > 0 else []
    }
    
    return stats

def calculate_entropy(series):
    """
    Calculate the entropy of a categorical series.
    
    Args:
        series (pd.Series): The series to calculate entropy for
        
    Returns:
        float: The entropy value
    """
    # Get value counts and probabilities
    value_counts = series.value_counts(normalize=True)
    
    # Calculate entropy
    entropy = -np.sum(value_counts * np.log2(value_counts))
    
    return entropy

def calculate_correlations(df, method='pearson'):
    """
    Calculate correlations between numeric columns in a DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
        method (str, optional): Correlation method ('pearson', 'spearman', or 'kendall')
        
    Returns:
        pd.DataFrame: Correlation matrix
    """
    # Get numeric columns
    numeric_df = df.select_dtypes(include=['number'])
    
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr(method=method)
    
    return corr_matrix

def prepare_data_for_visualization(df, x_col, y_col=None, color_col=None, size_col=None):
    """
    Prepare data for visualization by handling missing values and converting types.
    
    Args:
        df (pd.DataFrame): The DataFrame to prepare
        x_col (str): Column name for x-axis
        y_col (str, optional): Column name for y-axis
        color_col (str, optional): Column name for color encoding
        size_col (str, optional): Column name for size encoding
        
    Returns:
        pd.DataFrame: The prepared DataFrame
    """
    # Create a copy of the DataFrame
    prepared_df = df.copy()
    
    # List of columns to check
    cols_to_check = [col for col in [x_col, y_col, color_col, size_col] if col is not None]
    
    # Handle missing values
    for col in cols_to_check:
        if col in prepared_df.columns:
            # For numeric columns, replace missing values with median
            if pd.api.types.is_numeric_dtype(prepared_df[col]):
                prepared_df[col] = prepared_df[col].fillna(prepared_df[col].median())
            # For categorical columns, replace missing values with mode
            else:
                mode_value = prepared_df[col].mode()[0] if not prepared_df[col].mode().empty else "Unknown"
                prepared_df[col] = prepared_df[col].fillna(mode_value)
    
    # Filter out rows with missing values in the specified columns
    prepared_df = prepared_df.dropna(subset=[col for col in cols_to_check if col in prepared_df.columns])
    
    return prepared_df

def detect_date_columns(df):
    """
    Detect columns that contain date values.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
        
    Returns:
        list: List of column names that contain dates
    """
    date_columns = []
    
    for column in df.columns:
        # Check if column is already a datetime
        if pd.api.types.is_datetime64_dtype(df[column]):
            date_columns.append(column)
        # Check if column is a string and might be a date
        elif df[column].dtype == 'object':
            # Try to convert to datetime
            try:
                pd.to_datetime(df[column], errors='raise')
                date_columns.append(column)
            except:
                # Check if column name suggests it's a date
                if any(date_term in column.lower() for date_term in ['date', 'time', 'day', 'month', 'year']):
                    # Try with a sample
                    sample = df[column].dropna().head(10)
                    if all(isinstance(x, str) and re.search(r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}', x) for x in sample):
                        date_columns.append(column)
    
    return date_columns

def convert_to_datetime(df, column):
    """
    Convert a column to datetime format.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column
        column (str): The name of the column to convert
        
    Returns:
        pd.Series: The converted datetime series
    """
    try:
        return pd.to_datetime(df[column])
    except:
        return df[column]

def group_by_time_period(df, date_column, time_period='day'):
    """
    Group a DataFrame by a time period.
    
    Args:
        df (pd.DataFrame): The DataFrame to group
        date_column (str): The name of the date column
        time_period (str, optional): Time period to group by ('day', 'week', 'month', 'quarter', 'year')
        
    Returns:
        pd.DataFrame: The grouped DataFrame
    """
    # Convert date column to datetime if it's not already
    if not pd.api.types.is_datetime64_dtype(df[date_column]):
        df[date_column] = convert_to_datetime(df, date_column)
    
    # Group by time period
    if time_period == 'day':
        return df.groupby(df[date_column].dt.date)
    elif time_period == 'week':
        return df.groupby(pd.Grouper(key=date_column, freq='W'))
    elif time_period == 'month':
        return df.groupby(pd.Grouper(key=date_column, freq='M'))
    elif time_period == 'quarter':
        return df.groupby(pd.Grouper(key=date_column, freq='Q'))
    elif time_period == 'year':
        return df.groupby(pd.Grouper(key=date_column, freq='Y'))
    else:
        return df.groupby(df[date_column].dt.date)

def detect_outliers(df, column, method='iqr', threshold=1.5):
    """
    Detect outliers in a numeric column.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column
        column (str): The name of the column to analyze
        method (str, optional): Method to detect outliers ('iqr' or 'zscore')
        threshold (float, optional): Threshold for outlier detection
        
    Returns:
        pd.Series: Boolean series indicating outliers
    """
    # Get column data
    data = df[column].dropna()
    
    # Detect outliers
    if method == 'iqr':
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    else:  # zscore
        z_scores = np.abs(stats.zscore(data))
        outliers = pd.Series(False, index=df.index)
        outliers.loc[data.index] = z_scores > threshold
    
    return outliers

def create_sample_datasets_info():
    """
    Create information about the sample datasets.
    
    Returns:
        dict: Dictionary of sample dataset information
    """
    sample_datasets = {
        "sample_sales_data.csv": {
            "name": "Sample Sales Data",
            "description": "Retail sales transactions with product, customer, and location information.",
            "rows": 1000,
            "columns": 15,
            "category": "Sales"
        },
        "customer_analytics.csv": {
            "name": "Customer Analytics",
            "description": "Customer behavior and demographic data with engagement metrics.",
            "rows": 50,
            "columns": 20,
            "category": "Customer"
        },
        "financial_performance.csv": {
            "name": "Financial Performance",
            "description": "Daily financial metrics by department, region, and product line.",
            "rows": 59,
            "columns": 21,
            "category": "Financial"
        },
        "marketing_campaigns.csv": {
            "name": "Marketing Campaigns",
            "description": "Campaign performance metrics across different channels and audiences.",
            "rows": 50,
            "columns": 25,
            "category": "Marketing"
        },
        "employee_satisfaction.csv": {
            "name": "Employee Satisfaction",
            "description": "HR survey results with employee satisfaction scores across various dimensions.",
            "rows": 50,
            "columns": 40,
            "category": "HR"
        },
        "product_inventory.csv": {
            "name": "Product Inventory",
            "description": "Product catalog with inventory levels, pricing, and supplier information.",
            "rows": 50,
            "columns": 45,
            "category": "Inventory"
        },
        "website_traffic.csv": {
            "name": "Website Traffic",
            "description": "Web analytics data with page views, conversion rates, and user behavior.",
            "rows": 70,
            "columns": 35,
            "category": "Web"
        }
    }
    
    return sample_datasets
