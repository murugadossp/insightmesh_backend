import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Union, Optional

def display_metrics(
    metrics: Dict[str, Union[int, float, str]],
    columns: int = 3,
    format_func: Dict[str, callable] = None
) -> None:
    """
    Display a set of metrics in a grid layout.
    
    Args:
        metrics (Dict[str, Union[int, float, str]]): Dictionary of metric names and values
        columns (int, optional): Number of columns in the grid
        format_func (Dict[str, callable], optional): Dictionary of formatting functions for each metric
    """
    # Create columns
    cols = st.columns(columns)
    
    # Display metrics
    for i, (name, value) in enumerate(metrics.items()):
        # Determine which column to use
        col = cols[i % columns]
        
        # Format value if format function is provided
        if format_func and name in format_func:
            formatted_value = format_func[name](value)
        elif isinstance(value, int):
            formatted_value = f"{value:,}"
        elif isinstance(value, float):
            formatted_value = f"{value:,.2f}"
        else:
            formatted_value = value
        
        # Display metric
        with col:
            st.metric(name, formatted_value)

def display_data_summary(df: pd.DataFrame) -> None:
    """
    Display a summary of a DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to summarize
    """
    # Calculate summary statistics
    summary = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": df.isna().sum().sum(),
        "Duplicate Rows": df.duplicated().sum()
    }
    
    # Calculate missing values percentage
    if len(df) > 0:
        missing_pct = summary["Missing Values"] / (summary["Rows"] * summary["Columns"]) * 100
        summary["Missing Values"] = f"{summary['Missing Values']:,} ({missing_pct:.2f}%)"
    
    # Calculate duplicate rows percentage
    if len(df) > 0:
        duplicate_pct = summary["Duplicate Rows"] / summary["Rows"] * 100
        summary["Duplicate Rows"] = f"{summary['Duplicate Rows']:,} ({duplicate_pct:.2f}%)"
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Display metrics
    col1.metric("Rows", f"{summary['Rows']:,}")
    col2.metric("Columns", f"{summary['Columns']:,}")
    col3.metric("Missing Values", summary["Missing Values"])
    col4.metric("Duplicate Rows", summary["Duplicate Rows"])
    
    # Display memory usage
    memory_usage = df.memory_usage(deep=True).sum()
    if memory_usage < 1024:
        memory_str = f"{memory_usage} bytes"
    elif memory_usage < 1024 * 1024:
        memory_str = f"{memory_usage / 1024:.2f} KB"
    elif memory_usage < 1024 * 1024 * 1024:
        memory_str = f"{memory_usage / (1024 * 1024):.2f} MB"
    else:
        memory_str = f"{memory_usage / (1024 * 1024 * 1024):.2f} GB"
    
    st.markdown(f"**Memory Usage:** {memory_str}")

def display_numeric_summary(df: pd.DataFrame, column: str) -> None:
    """
    Display a summary of a numeric column.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column
        column (str): The name of the column to summarize
    """
    # Check if column is numeric
    if not pd.api.types.is_numeric_dtype(df[column]):
        st.warning(f"Column '{column}' is not numeric.")
        return
    
    # Calculate summary statistics
    stats = df[column].describe()
    
    # Calculate additional statistics
    additional_stats = {
        "Missing Values": df[column].isna().sum(),
        "Missing %": df[column].isna().sum() / len(df) * 100 if len(df) > 0 else 0,
        "Zeros": (df[column] == 0).sum(),
        "Negative Values": (df[column] < 0).sum(),
        "Skewness": df[column].skew(),
        "Kurtosis": df[column].kurtosis(),
        "IQR": stats["75%"] - stats["25%"],
        "Range": stats["max"] - stats["min"],
        "Coefficient of Variation": stats["std"] / stats["mean"] * 100 if stats["mean"] != 0 else np.nan
    }
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Display basic statistics
    col1.metric("Count", f"{stats['count']:,.0f}")
    col1.metric("Min", f"{stats['min']:,.2f}")
    col1.metric("Max", f"{stats['max']:,.2f}")
    
    col2.metric("Mean", f"{stats['mean']:,.2f}")
    col2.metric("Median", f"{stats['50%']:,.2f}")
    col2.metric("Std Dev", f"{stats['std']:,.2f}")
    
    col3.metric("25th Percentile", f"{stats['25%']:,.2f}")
    col3.metric("75th Percentile", f"{stats['75%']:,.2f}")
    col3.metric("IQR", f"{additional_stats['IQR']:,.2f}")
    
    col4.metric("Missing Values", f"{additional_stats['Missing Values']:,} ({additional_stats['Missing %']:.2f}%)")
    col4.metric("Skewness", f"{additional_stats['Skewness']:.2f}")
    col4.metric("Kurtosis", f"{additional_stats['Kurtosis']:.2f}")
    
    # Display additional statistics
    st.markdown("### Additional Statistics")
    
    # Create columns for additional metrics
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Range", f"{additional_stats['Range']:,.2f}")
    col1.metric("Zeros", f"{additional_stats['Zeros']:,}")
    
    col2.metric("Negative Values", f"{additional_stats['Negative Values']:,}")
    col2.metric("Coefficient of Variation", f"{additional_stats['Coefficient of Variation']:.2f}%" if not np.isnan(additional_stats['Coefficient of Variation']) else "N/A")
    
    # Calculate quartiles
    quartiles = {
        "Q1 (25%)": stats["25%"],
        "Q2 (50%)": stats["50%"],
        "Q3 (75%)": stats["75%"]
    }
    
    # Calculate deciles
    deciles = {}
    for i in range(1, 10):
        decile = i * 10
        deciles[f"D{i} ({decile}%)"] = df[column].quantile(decile / 100)
    
    # Display percentiles
    with st.expander("View Percentiles"):
        # Create columns for percentiles
        col1, col2 = st.columns(2)
        
        # Display quartiles
        col1.markdown("#### Quartiles")
        for name, value in quartiles.items():
            col1.markdown(f"**{name}:** {value:,.2f}")
        
        # Display deciles
        col2.markdown("#### Deciles")
        for name, value in deciles.items():
            col2.markdown(f"**{name}:** {value:,.2f}")

def display_categorical_summary(df: pd.DataFrame, column: str, top_n: int = 10) -> None:
    """
    Display a summary of a categorical column.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column
        column (str): The name of the column to summarize
        top_n (int, optional): Number of top categories to display
    """
    # Calculate summary statistics
    value_counts = df[column].value_counts()
    value_counts_pct = df[column].value_counts(normalize=True) * 100
    
    # Calculate additional statistics
    stats = {
        "Unique Values": df[column].nunique(),
        "Missing Values": df[column].isna().sum(),
        "Missing %": df[column].isna().sum() / len(df) * 100 if len(df) > 0 else 0,
        "Mode": df[column].mode()[0] if not df[column].mode().empty else None,
        "Mode Count": value_counts.iloc[0] if not value_counts.empty else 0,
        "Mode %": value_counts_pct.iloc[0] if not value_counts_pct.empty else 0
    }
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    # Display basic statistics
    col1.metric("Count", f"{len(df):,}")
    col1.metric("Unique Values", f"{stats['Unique Values']:,}")
    
    col2.metric("Missing Values", f"{stats['Missing Values']:,} ({stats['Missing %']:.2f}%)")
    col2.metric("Mode", f"{stats['Mode']}")
    
    col3.metric("Mode Count", f"{stats['Mode Count']:,}")
    col3.metric("Mode %", f"{stats['Mode %']:.2f}%")
    
    # Display top categories
    st.markdown(f"### Top {min(top_n, len(value_counts))} Categories")
    
    # Create DataFrame for display
    top_categories = pd.DataFrame({
        "Category": value_counts.index[:top_n],
        "Count": value_counts.values[:top_n],
        "Percentage": value_counts_pct.values[:top_n]
    })
    
    # Display DataFrame
    st.dataframe(top_categories, use_container_width=True)
    
    # Display category distribution
    if len(value_counts) > top_n:
        other_count = value_counts.iloc[top_n:].sum()
        other_pct = value_counts_pct.iloc[top_n:].sum()
        
        st.markdown(f"**Other Categories:** {len(value_counts) - top_n:,} categories with {other_count:,} values ({other_pct:.2f}%)")

def display_correlation_summary(df: pd.DataFrame, threshold: float = 0.7) -> None:
    """
    Display a summary of correlations in a DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
        threshold (float, optional): Correlation threshold for highlighting
    """
    # Get numeric columns
    numeric_df = df.select_dtypes(include=['number'])
    
    if len(numeric_df.columns) < 2:
        st.warning("Not enough numeric columns for correlation analysis.")
        return
    
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Get pairs with high correlation
    high_corr_pairs = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            corr = corr_matrix.iloc[i, j]
            
            if abs(corr) >= threshold:
                high_corr_pairs.append({
                    "Column 1": col1,
                    "Column 2": col2,
                    "Correlation": corr
                })
    
    # Sort by absolute correlation
    high_corr_pairs.sort(key=lambda x: abs(x["Correlation"]), reverse=True)
    
    # Display high correlation pairs
    if high_corr_pairs:
        st.markdown(f"### High Correlation Pairs (|r| ≥ {threshold})")
        
        # Create DataFrame for display
        high_corr_df = pd.DataFrame(high_corr_pairs)
        
        # Display DataFrame
        st.dataframe(high_corr_df, use_container_width=True)
    else:
        st.info(f"No column pairs with correlation above {threshold} threshold.")
    
    # Display correlation statistics
    st.markdown("### Correlation Statistics")
    
    # Calculate correlation statistics
    corr_values = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)]
    
    stats = {
        "Mean Correlation": np.mean(np.abs(corr_values)),
        "Median Correlation": np.median(np.abs(corr_values)),
        "Max Correlation": np.max(np.abs(corr_values)),
        "Min Correlation": np.min(np.abs(corr_values)),
        "Std Dev": np.std(corr_values)
    }
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    # Display statistics
    col1.metric("Mean |r|", f"{stats['Mean Correlation']:.4f}")
    col1.metric("Median |r|", f"{stats['Median Correlation']:.4f}")
    
    col2.metric("Max |r|", f"{stats['Max Correlation']:.4f}")
    col2.metric("Min |r|", f"{stats['Min Correlation']:.4f}")
    
    col3.metric("Std Dev", f"{stats['Std Dev']:.4f}")
    col3.metric("Pairs Analyzed", f"{len(corr_values):,}")

def display_missing_values_summary(df: pd.DataFrame) -> None:
    """
    Display a summary of missing values in a DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze
    """
    # Calculate missing values
    missing = df.isna().sum()
    missing_pct = df.isna().sum() / len(df) * 100 if len(df) > 0 else pd.Series(0, index=df.columns)
    
    # Create DataFrame for display
    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values,
        "Missing %": missing_pct.values
    })
    
    # Sort by missing percentage
    missing_df = missing_df.sort_values("Missing %", ascending=False)
    
    # Calculate overall statistics
    total_cells = df.size
    missing_cells = missing.sum()
    missing_cells_pct = missing_cells / total_cells * 100 if total_cells > 0 else 0
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    # Display overall statistics
    col1.metric("Total Cells", f"{total_cells:,}")
    col1.metric("Missing Cells", f"{missing_cells:,}")
    
    col2.metric("Missing %", f"{missing_cells_pct:.2f}%")
    col2.metric("Columns with Missing Values", f"{(missing > 0).sum():,}")
    
    col3.metric("Complete Columns", f"{(missing == 0).sum():,}")
    col3.metric("Complete Rows", f"{(df.isna().sum(axis=1) == 0).sum():,}")
    
    # Display missing values by column
    st.markdown("### Missing Values by Column")
    
    # Display DataFrame
    st.dataframe(missing_df, use_container_width=True)
    
    # Display columns with no missing values
    complete_columns = missing_df[missing_df["Missing Values"] == 0]["Column"].tolist()
    
    if complete_columns:
        with st.expander("Columns with No Missing Values"):
            st.write(", ".join(complete_columns))

def display_outlier_summary(df: pd.DataFrame, column: str, method: str = 'iqr', threshold: float = 1.5) -> None:
    """
    Display a summary of outliers in a numeric column.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column
        column (str): The name of the column to analyze
        method (str, optional): Method to detect outliers ('iqr' or 'zscore')
        threshold (float, optional): Threshold for outlier detection
    """
    # Check if column is numeric
    if not pd.api.types.is_numeric_dtype(df[column]):
        st.warning(f"Column '{column}' is not numeric.")
        return
    
    # Get column data
    data = df[column].dropna()
    
    # Detect outliers
    if method == 'iqr':
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        outliers = (data < lower_bound) | (data > upper_bound)
    else:  # zscore
        from scipy import stats
        z_scores = np.abs(stats.zscore(data))
        outliers = z_scores > threshold
    
    # Count outliers
    outlier_count = outliers.sum()
    outlier_pct = outlier_count / len(data) * 100 if len(data) > 0 else 0
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    # Display outlier statistics
    col1.metric("Total Values", f"{len(data):,}")
    col1.metric("Outliers", f"{outlier_count:,}")
    
    col2.metric("Outlier %", f"{outlier_pct:.2f}%")
    if method == 'iqr':
        col2.metric("IQR", f"{iqr:.2f}")
    
    col3.metric("Method", f"{method.upper()}")
    col3.metric("Threshold", f"{threshold}")
    
    # Display bounds
    if method == 'iqr':
        st.markdown("### Outlier Bounds")
        
        # Create columns for bounds
        bound_col1, bound_col2 = st.columns(2)
        
        # Display bounds
        bound_col1.metric("Lower Bound", f"{lower_bound:.2f}")
        bound_col2.metric("Upper Bound", f"{upper_bound:.2f}")
        
        # Display outlier values
        if outlier_count > 0:
            st.markdown("### Outlier Values")
            
            # Get outlier values
            outlier_values = data[outliers]
            
            # Display statistics
            outlier_stats = {
                "Min": outlier_values.min(),
                "Max": outlier_values.max(),
                "Mean": outlier_values.mean(),
                "Median": outlier_values.median(),
                "Std Dev": outlier_values.std()
            }
            
            # Create columns for statistics
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            
            # Display statistics
            stat_col1.metric("Min", f"{outlier_stats['Min']:.2f}")
            stat_col1.metric("Max", f"{outlier_stats['Max']:.2f}")
            
            stat_col2.metric("Mean", f"{outlier_stats['Mean']:.2f}")
            stat_col2.metric("Median", f"{outlier_stats['Median']:.2f}")
            
            stat_col3.metric("Std Dev", f"{outlier_stats['Std Dev']:.2f}")
            
            # Display histogram of outliers
            if len(outlier_values) > 1:
                import plotly.express as px
                
                fig = px.histogram(
                    outlier_values,
                    nbins=min(20, len(outlier_values)),
                    title=f"Distribution of Outliers in {column}"
                )
                
                st.plotly_chart(fig, use_container_width=True)
