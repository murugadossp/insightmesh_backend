import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.api_client import APIClient
from components.charts import (
    create_bar_chart, create_line_chart, create_pie_chart, create_scatter_plot,
    create_heatmap, create_histogram, create_box_plot, create_distribution_chart
)
from components.metrics import (
    display_metrics, display_data_summary, display_numeric_summary,
    display_categorical_summary, display_correlation_summary, display_missing_values_summary,
    display_outlier_summary
)
from utils.styling import apply_custom_styling, create_insight_box, create_status_indicator
from utils.data_processing import (
    load_csv, detect_column_types, calculate_summary_statistics,
    calculate_categorical_statistics, calculate_correlations, prepare_data_for_visualization,
    detect_date_columns, convert_to_datetime, group_by_time_period, detect_outliers,
    create_sample_datasets_info
)

# Set page configuration
st.set_page_config(
    page_title="Analytics - InsightMesh",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Initialize API client
api_client = APIClient(base_url="http://localhost:8000")

# Initialize session state
if 'current_dataset' not in st.session_state:
    st.session_state.current_dataset = None
if 'current_dataset_name' not in st.session_state:
    st.session_state.current_dataset_name = None
if 'column_types' not in st.session_state:
    st.session_state.column_types = None

# Page header
st.title("📈 Analytics")
st.markdown("### Advanced statistical analysis and interactive visualizations")

# Sidebar for dataset selection and options
with st.sidebar:
    st.header("Dataset Selection")
    
    # Get sample datasets info
    sample_datasets = create_sample_datasets_info()
    
    # Create dataset selection
    dataset_options = ["Select a dataset..."] + list(sample_datasets.keys())
    selected_dataset = st.selectbox("Choose a dataset", dataset_options)
    
    if selected_dataset != "Select a dataset...":
        # Load dataset if not already loaded
        if st.session_state.current_dataset is None or st.session_state.current_dataset_name != selected_dataset:
            with st.spinner(f"Loading {selected_dataset}..."):
                # Load dataset
                dataset_path = os.path.join("../sample_data", selected_dataset)
                df = load_csv(dataset_path)
                
                if df is not None:
                    # Update session state
                    st.session_state.current_dataset = df
                    st.session_state.current_dataset_name = selected_dataset
                    
                    # Detect column types
                    st.session_state.column_types = detect_column_types(df)
                    
                    st.success(f"Loaded {selected_dataset} successfully!")
                else:
                    st.error(f"Error loading {selected_dataset}. Please try again.")
        
        # Display dataset info
        if st.session_state.current_dataset is not None:
            df = st.session_state.current_dataset
            
            st.markdown("### Dataset Info")
            st.markdown(f"**Name:** {selected_dataset}")
            st.markdown(f"**Rows:** {len(df):,}")
            st.markdown(f"**Columns:** {len(df.columns):,}")
            
            # Display column types
            if st.session_state.column_types is not None:
                st.markdown("### Column Types")
                
                # Count column types
                type_counts = {}
                for col_type in st.session_state.column_types.values():
                    type_counts[col_type] = type_counts.get(col_type, 0) + 1
                
                # Display counts
                for col_type, count in type_counts.items():
                    st.markdown(f"- **{col_type.capitalize()}:** {count}")
    
    # Analysis options
    if st.session_state.current_dataset is not None:
        st.header("Analysis Options")
        
        # Create analysis type selection
        analysis_types = [
            "Overview",
            "Univariate Analysis",
            "Bivariate Analysis",
            "Correlation Analysis",
            "Time Series Analysis",
            "Missing Values Analysis",
            "Outlier Analysis"
        ]
        
        selected_analysis = st.radio("Analysis Type", analysis_types)
        
        # Additional options based on analysis type
        if selected_analysis == "Univariate Analysis":
            # Get column options
            column_options = list(st.session_state.current_dataset.columns)
            
            # Create column selection
            selected_column = st.selectbox("Select Column", column_options)
            
            # Store in session state
            st.session_state.selected_column = selected_column
            
            # Get column type
            column_type = st.session_state.column_types.get(selected_column, "unknown")
            
            # Additional options based on column type
            if column_type in ["integer", "float"]:
                # Bin options for histograms
                bin_count = st.slider("Bin Count", min_value=5, max_value=100, value=30)
                st.session_state.bin_count = bin_count
                
                # Outlier detection method
                outlier_method = st.radio("Outlier Detection Method", ["IQR", "Z-Score"])
                st.session_state.outlier_method = outlier_method.lower()
                
                # Outlier threshold
                if outlier_method == "IQR":
                    threshold = st.slider("IQR Multiplier", min_value=0.5, max_value=3.0, value=1.5, step=0.1)
                else:  # Z-Score
                    threshold = st.slider("Z-Score Threshold", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
                
                st.session_state.outlier_threshold = threshold
            
            elif column_type in ["categorical", "text"]:
                # Top N categories
                top_n = st.slider("Top Categories", min_value=5, max_value=50, value=10)
                st.session_state.top_n = top_n
        
        elif selected_analysis == "Bivariate Analysis":
            # Get column options
            column_options = list(st.session_state.current_dataset.columns)
            
            # Create column selections
            selected_x = st.selectbox("Select X-Axis Column", column_options)
            selected_y = st.selectbox("Select Y-Axis Column", column_options, index=min(1, len(column_options)-1))
            
            # Store in session state
            st.session_state.selected_x = selected_x
            st.session_state.selected_y = selected_y
            
            # Get column types
            x_type = st.session_state.column_types.get(selected_x, "unknown")
            y_type = st.session_state.column_types.get(selected_y, "unknown")
            
            # Chart type selection based on column types
            chart_options = []
            
            if x_type in ["integer", "float"] and y_type in ["integer", "float"]:
                chart_options = ["Scatter Plot", "Hexbin Plot", "Bubble Chart"]
            elif (x_type in ["categorical", "text"] and y_type in ["integer", "float"]) or \
                 (y_type in ["categorical", "text"] and x_type in ["integer", "float"]):
                chart_options = ["Bar Chart", "Box Plot", "Violin Plot"]
            elif x_type in ["categorical", "text"] and y_type in ["categorical", "text"]:
                chart_options = ["Heatmap", "Grouped Bar Chart", "Stacked Bar Chart"]
            elif x_type == "date" or y_type == "date":
                chart_options = ["Line Chart", "Area Chart", "Bar Chart"]
            
            if chart_options:
                selected_chart = st.radio("Chart Type", chart_options)
                st.session_state.selected_chart = selected_chart
        
        elif selected_analysis == "Correlation Analysis":
            # Correlation method
            correlation_method = st.radio("Correlation Method", ["Pearson", "Spearman", "Kendall"])
            st.session_state.correlation_method = correlation_method.lower()
            
            # Correlation threshold
            correlation_threshold = st.slider("Correlation Threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
            st.session_state.correlation_threshold = correlation_threshold
        
        elif selected_analysis == "Time Series Analysis":
            # Detect date columns
            date_columns = detect_date_columns(st.session_state.current_dataset)
            
            if date_columns:
                # Create date column selection
                selected_date = st.selectbox("Select Date Column", date_columns)
                
                # Store in session state
                st.session_state.selected_date = selected_date
                
                # Get numeric columns
                numeric_columns = [col for col, col_type in st.session_state.column_types.items() 
                                  if col_type in ["integer", "float"]]
                
                if numeric_columns:
                    # Create value column selection
                    selected_value = st.selectbox("Select Value Column", numeric_columns)
                    
                    # Store in session state
                    st.session_state.selected_value = selected_value
                    
                    # Time period selection
                    time_period = st.radio("Time Period", ["Day", "Week", "Month", "Quarter", "Year"])
                    st.session_state.time_period = time_period.lower()
                    
                    # Moving average window
                    ma_window = st.slider("Moving Average Window", min_value=1, max_value=30, value=7)
                    st.session_state.ma_window = ma_window
                else:
                    st.warning("No numeric columns found for time series analysis.")
            else:
                st.warning("No date columns detected in the dataset.")
        
        elif selected_analysis == "Missing Values Analysis":
            # Missing values threshold
            missing_threshold = st.slider("Missing Values Threshold (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
            st.session_state.missing_threshold = missing_threshold / 100.0
        
        elif selected_analysis == "Outlier Analysis":
            # Get numeric columns
            numeric_columns = [col for col, col_type in st.session_state.column_types.items() 
                              if col_type in ["integer", "float"]]
            
            if numeric_columns:
                # Create column selection
                selected_column = st.selectbox("Select Column", numeric_columns)
                
                # Store in session state
                st.session_state.selected_column = selected_column
                
                # Outlier detection method
                outlier_method = st.radio("Outlier Detection Method", ["IQR", "Z-Score"])
                st.session_state.outlier_method = outlier_method.lower()
                
                # Outlier threshold
                if outlier_method == "IQR":
                    threshold = st.slider("IQR Multiplier", min_value=0.5, max_value=3.0, value=1.5, step=0.1)
                else:  # Z-Score
                    threshold = st.slider("Z-Score Threshold", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
                
                st.session_state.outlier_threshold = threshold
            else:
                st.warning("No numeric columns found for outlier analysis.")

# Main content
if st.session_state.current_dataset is not None:
    df = st.session_state.current_dataset
    
    # Get selected analysis type
    selected_analysis = st.session_state.get("selected_analysis", "Overview")
    
    # Display analysis based on selection
    if selected_analysis == "Overview":
        st.markdown("## Dataset Overview")
        
        # Display data summary
        display_data_summary(df)
        
        # Display sample data
        st.markdown("### Sample Data")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Display column information
        st.markdown("### Column Information")
        
        # Create DataFrame with column info
        column_info = []
        for column in df.columns:
            col_type = st.session_state.column_types.get(column, "unknown")
            non_null = df[column].count()
            null_count = df[column].isna().sum()
            null_pct = null_count / len(df) * 100
            unique_count = df[column].nunique()
            unique_pct = unique_count / len(df) * 100 if len(df) > 0 else 0
            
            column_info.append({
                "Column": column,
                "Type": col_type.capitalize(),
                "Non-Null Count": f"{non_null:,}",
                "Null Count": f"{null_count:,}",
                "Null %": f"{null_pct:.2f}%",
                "Unique Values": f"{unique_count:,}",
                "Unique %": f"{unique_pct:.2f}%"
            })
        
        # Create DataFrame
        column_info_df = pd.DataFrame(column_info)
        
        # Display DataFrame
        st.dataframe(column_info_df, use_container_width=True)
        
        # Display data quality summary
        st.markdown("### Data Quality Summary")
        
        # Calculate data quality metrics
        total_cells = df.size
        missing_cells = df.isna().sum().sum()
        missing_pct = missing_cells / total_cells * 100 if total_cells > 0 else 0
        duplicate_rows = df.duplicated().sum()
        duplicate_pct = duplicate_rows / len(df) * 100 if len(df) > 0 else 0
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Cells", f"{total_cells:,}")
            st.metric("Missing Cells", f"{missing_cells:,} ({missing_pct:.2f}%)")
        
        with col2:
            st.metric("Total Rows", f"{len(df):,}")
            st.metric("Duplicate Rows", f"{duplicate_rows:,} ({duplicate_pct:.2f}%)")
        
        with col3:
            # Calculate data quality score (mock)
            quality_score = 100 - (missing_pct + duplicate_pct) / 2
            quality_score = max(0, min(100, quality_score))
            st.metric("Data Quality Score", f"{quality_score:.1f}%")
            
            # Calculate completeness score
            completeness_score = 100 - missing_pct
            completeness_score = max(0, min(100, completeness_score))
            st.metric("Completeness Score", f"{completeness_score:.1f}%")
    
    elif selected_analysis == "Univariate Analysis":
        # Get selected column
        selected_column = st.session_state.get("selected_column")
        
        if selected_column:
            st.markdown(f"## Univariate Analysis: {selected_column}")
            
            # Get column type
            column_type = st.session_state.column_types.get(selected_column, "unknown")
            
            # Display analysis based on column type
            if column_type in ["integer", "float"]:
                # Display numeric summary
                display_numeric_summary(df, selected_column)
                
                # Create columns for charts
                col1, col2 = st.columns(2)
                
                with col1:
                    # Create histogram
                    st.markdown("### Histogram")
                    
                    # Get bin count
                    bin_count = st.session_state.get("bin_count", 30)
                    
                    # Create histogram
                    fig = create_histogram(
                        df,
                        x=selected_column,
                        title=f"Distribution of {selected_column}",
                        nbins=bin_count
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Create box plot
                    st.markdown("### Box Plot")
                    
                    # Create box plot
                    fig = create_box_plot(
                        df,
                        y=selected_column,
                        title=f"Box Plot of {selected_column}"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                # Create distribution chart
                st.markdown("### Distribution Chart")
                
                # Create distribution chart
                fig = create_distribution_chart(
                    df,
                    column=selected_column,
                    title=f"Distribution of {selected_column}"
                )
                
                # Display chart
                st.plotly_chart(fig, use_container_width=True)
                
                # Display outlier analysis
                st.markdown("### Outlier Analysis")
                
                # Get outlier method and threshold
                outlier_method = st.session_state.get("outlier_method", "iqr")
                outlier_threshold = st.session_state.get("outlier_threshold", 1.5)
                
                # Display outlier summary
                display_outlier_summary(df, selected_column, method=outlier_method, threshold=outlier_threshold)
            
            elif column_type in ["categorical", "text"]:
                # Display categorical summary
                top_n = st.session_state.get("top_n", 10)
                display_categorical_summary(df, selected_column, top_n=top_n)
                
                # Create pie chart
                st.markdown("### Pie Chart")
                
                # Get value counts
                value_counts = df[selected_column].value_counts().head(top_n)
                
                # Create DataFrame for pie chart
                pie_data = pd.DataFrame({
                    "Category": value_counts.index,
                    "Count": value_counts.values
                })
                
                # Create pie chart
                fig = create_pie_chart(
                    pie_data,
                    names="Category",
                    values="Count",
                    title=f"Distribution of {selected_column}"
                )
                
                # Display chart
                st.plotly_chart(fig, use_container_width=True)
            
            elif column_type == "date":
                # Display date summary
                st.markdown("### Date Summary")
                
                # Convert to datetime
                date_series = convert_to_datetime(df, selected_column)
                
                # Calculate date range
                min_date = date_series.min()
                max_date = date_series.max()
                date_range = (max_date - min_date).days
                
                # Create columns for metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Minimum Date", min_date.strftime("%Y-%m-%d"))
                    st.metric("Date Range", f"{date_range} days")
                
                with col2:
                    st.metric("Maximum Date", max_date.strftime("%Y-%m-%d"))
                    st.metric("Unique Dates", f"{date_series.nunique():,}")
                
                with col3:
                    st.metric("Missing Dates", f"{date_series.isna().sum():,}")
                    st.metric("Complete %", f"{date_series.count() / len(df) * 100:.2f}%")
                
                # Create time series chart
                st.markdown("### Time Series")
                
                # Group by date
                date_counts = df.groupby(date_series.dt.date).size().reset_index()
                date_counts.columns = [selected_column, "Count"]
                
                # Create line chart
                fig = create_line_chart(
                    date_counts,
                    x=selected_column,
                    y="Count",
                    title=f"Frequency of {selected_column}"
                )
                
                # Display chart
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.warning(f"Unsupported column type: {column_type}")
        else:
            st.warning("Please select a column for univariate analysis.")
    
    elif selected_analysis == "Bivariate Analysis":
        # Get selected columns
        selected_x = st.session_state.get("selected_x")
        selected_y = st.session_state.get("selected_y")
        
        if selected_x and selected_y:
            st.markdown(f"## Bivariate Analysis: {selected_x} vs {selected_y}")
            
            # Get column types
            x_type = st.session_state.column_types.get(selected_x, "unknown")
            y_type = st.session_state.column_types.get(selected_y, "unknown")
            
            # Get selected chart type
            selected_chart = st.session_state.get("selected_chart")
            
            # Display analysis based on column types and chart selection
            if x_type in ["integer", "float"] and y_type in ["integer", "float"]:
                # Numeric vs Numeric
                
                # Calculate correlation
                correlation = df[[selected_x, selected_y]].corr().iloc[0, 1]
                
                # Display correlation
                st.metric("Correlation", f"{correlation:.4f}")
                
                if selected_chart == "Scatter Plot":
                    # Create scatter plot
                    fig = create_scatter_plot(
                        df,
                        x=selected_x,
                        y=selected_y,
                        title=f"{selected_x} vs {selected_y}",
                        trendline="ols"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_chart == "Hexbin Plot":
                    # Create hexbin plot using plotly
                    import plotly.express as px
                    
                    fig = px.density_heatmap(
                        df,
                        x=selected_x,
                        y=selected_y,
                        title=f"{selected_x} vs {selected_y}",
                        marginal_x="histogram",
                        marginal_y="histogram"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_chart == "Bubble Chart":
                    # Get numeric columns for size
                    numeric_columns = [col for col, col_type in st.session_state.column_types.items() 
                                      if col_type in ["integer", "float"] and col not in [selected_x, selected_y]]
                    
                    if numeric_columns:
                        # Create column selection for size
                        selected_size = st.selectbox("Select Size Column", numeric_columns)
                        
                        # Create bubble chart
                        fig = create_scatter_plot(
                            df,
                            x=selected_x,
                            y=selected_y,
                            title=f"{selected_x} vs {selected_y} (Size: {selected_size})",
                            size=selected_size
                        )
                        
                        # Display chart
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No additional numeric columns available for bubble size.")
            
            elif (x_type in ["categorical", "text"] and y_type in ["integer", "float"]) or \
                 (y_type in ["categorical", "text"] and x_type in ["integer", "float"]):
                # Categorical vs Numeric
                
                # Determine which is categorical and which is numeric
                if x_type in ["categorical", "text"]:
                    cat_col = selected_x
                    num_col = selected_y
                else:
                    cat_col = selected_y
                    num_col = selected_x
                
                if selected_chart == "Bar Chart":
                    # Group by categorical column
                    grouped = df.groupby(cat_col)[num_col].mean().reset_index()
                    
                    # Sort by numeric value
                    grouped = grouped.sort_values(num_col, ascending=False)
                    
                    # Limit to top 15 categories
                    if len(grouped) > 15:
                        grouped = grouped.head(15)
                    
                    # Create bar chart
                    fig = create_bar_chart(
                        grouped,
                        x=cat_col,
                        y=num_col,
                        title=f"Average {num_col} by {cat_col}"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_chart == "Box Plot":
                    # Create box plot
                    fig = create_box_plot(
                        df,
                        x=cat_col,
                        y=num_col,
                        title=f"Distribution of {num_col} by {cat_col}"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_chart == "Violin Plot":
                    # Create violin plot using plotly
                    import plotly.express as px
                    
                    fig = px.violin(
                        df,
                        x=cat_col,
                        y=num_col,
                        title=f"Distribution of {num_col} by {cat_col}",
                        box=True,
                        points="all"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
            
            elif x_type in ["categorical", "text"] and y_type in ["categorical", "text"]:
                # Categorical vs Categorical
                
                if selected_chart == "Heatmap":
                    # Create crosstab
                    crosstab = pd.crosstab(df[selected_x], df[selected_y], normalize='all') * 100
                    
                    # Create heatmap
                    fig = create_heatmap(
                        crosstab,
                        title=f"{selected_x} vs {selected_y} (%)",
                        colorscale="Blues",
                        zmin=0,
                        zmax=100
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_chart == "Grouped Bar Chart":
                    # Create crosstab
                    crosstab = pd.crosstab(df[selected_x], df[selected_y])
                    
                    # Convert to long format
                    long_df = crosstab.reset_index().melt(id_vars=selected_x, var_name=selected_y, value_name="Count")
                    
                    # Create grouped bar chart
                    import plotly.express as px
                    
                    fig = px.bar(
                        long_df,
                        x=selected_x,
                        y="Count",
                        color=selected_y,
                        title=f"{selected_x} vs {selected_y}",
                        barmode="group"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_chart == "Stacked Bar Chart":
                    # Create crosstab
                    crosstab = pd.crosstab(df[selected_x], df[selected_y])
                    
                    # Convert to long format
                    long_df = crosstab.reset_index().melt(id_vars=selected_x, var_name=selected_y, value_name="Count")
                    
                    # Create stacked bar chart
                    import plotly.express as px
                    
                    fig = px.bar(
                        long_df,
                        x=selected_x,
                        y="Count",
                        color=selected_y,
                        title=f"{selected_x} vs {selected_y}",
                        barmode="stack"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
            
            elif x_type == "date" or y_type == "date":
                # Date vs Other
                
                # Determine which is date
                if x_type == "date":
                    date_col = selected_x
                    value_col = selected_y
                else:
                    date_col = selected_y
                    value_col = selected_x
                
                # Convert to datetime
                date_series = convert_to_datetime(df, date_col)
                
                if selected_chart == "Line Chart":
                    # Group by date
                    if st.session_state.column_types.get(value_col) in ["integer", "float"]:
                        # For numeric columns, calculate mean
                        date_values = df.groupby(date_series.dt.date)[value_col].mean().reset_index()
                    else:
                        # For categorical columns, calculate count
                        date_values = df.groupby(date_series.dt.date)[value_col].count().reset_index()
                    
                    # Create line chart
                    fig = create_line_chart(
                        date_values,
                        x=date_col,
                        y=value_col,
                        title=f"{value_col} Over Time"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_chart == "Area Chart":
                    # Group by date
                    if st.session_state.column_types.get(value_col) in ["integer", "float"]:
                        # For numeric columns, calculate mean
                        date_values = df.groupby(date_series.dt.date)[value_col].mean().reset_index()
                    else:
                        # For categorical columns, calculate count
                        date_values = df.groupby(date_series.dt.date)[value_col].count().reset_index()
                    
                    # Create area chart
                    import plotly.express as px
                    
                    fig = px.area(
                        date_values,
                        x=date_col,
                        y=value_col,
                        title=f"{value_col} Over Time"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_chart == "Bar Chart":
                    # Group by date
                    if st.session_state.column_types.get(value_col) in ["integer", "float"]:
                        # For numeric columns, calculate mean
                        date_values = df.groupby(date_series.dt.date)[value_col].mean().reset_index()
                    else:
                        # For categorical columns, calculate count
                        date_values = df.groupby(date_series.dt.date)[value_col].count().reset_index()
                    
                    # Create bar chart
                    fig = create_bar_chart(
                        date_values,
                        x=date_col,
                        y=value_col,
                        title=f"{value_col} Over Time"
                    )
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.warning(f"Unsupported column types: {x_type} and {y_type}")
        else:
            st.warning("Please select columns for bivariate analysis.")
    
    elif selected_analysis == "Correlation Analysis":
        st.markdown("## Correlation Analysis")
        
        # Get correlation method and threshold
        correlation_method = st.session_state.get("correlation_method", "pearson")
        correlation_threshold = st.session_state.get("correlation_threshold", 0.7)
        
        # Display correlation summary
        display_correlation_summary(df, threshold=correlation_threshold)
        
        # Calculate correlation matrix
        corr_matrix = calculate_correlations(df, method=correlation_method)
        
        # Create heatmap
        fig = create_heatmap(
            corr_matrix,
            title=f"Correlation Matrix ({correlation_method.capitalize()})",
            colorscale="RdBu_r",
            zmin=-1,
            zmax=1
        )
        
        # Display chart
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Time Series Analysis":
        # Get selected date and value columns
        selected_date = st.session_state.get("selected_date")
        selected_value = st.session_state.get("selected_value")
        
        if selected_date and selected_value:
            st.markdown(f"## Time Series Analysis: {selected_value} Over Time")
            
            # Convert to datetime
            date_series = convert_to_datetime(df, selected_date)
            
            # Get time period
            time_period = st.session_state.get("time_period", "day")
            
            # Group by time period
            if time_period == "day":
                grouped = df.groupby(date_series.dt.date)[selected_value].mean().reset_index()
                grouped.columns = [selected_date, selected_value]
            else:
                # Create a copy of the DataFrame with the datetime column
                temp_df = df.copy()
                temp_df[selected_date] = date_series
                
                # Group by time period
                grouped = group_by_time_period(temp_df, selected_date, time_period=time_period)[selected_value].mean().reset_index()
            
            # Create line chart
            fig = create_line_chart(
                grouped,
                x=selected_date,
                y=selected_value,
                title=f"{selected_value} Over Time (by {time_period.capitalize()})"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate moving average
            ma_window = st.session_state.get("ma_window", 7)
            
            if len(grouped) > ma_window:
                # Calculate moving average
                grouped[f"{selected_value}_MA{ma_window}"] = grouped[selected_value].rolling(window=ma_window).mean()
                
                # Create line chart with moving average
                fig = create_line_chart(
                    grouped,
                    x=selected_date,
                    y=[selected_value, f"{selected_value}_MA{ma_window}"],
                    title=f"{selected_value} with {ma_window}-Period Moving Average"
                )
                
                # Display chart
                st.plotly_chart(fig, use_container_width=True)
            
            # Display seasonality analysis if enough data
            if len(grouped) >= 12:
                st.markdown("### Seasonality Analysis")
                
                # Create columns for seasonal charts
                col1, col2 = st.columns(2)
                
                with col1:
                    # Create month-of-year seasonality chart
                    if time_period in ["day", "week", "month"]:
                        # Add month column
                        temp_df = df.copy()
                        temp_df[selected_date] = date_series
                        
                        # Group by month
                        month_grouped = temp_df.groupby(temp_df[selected_date].dt.month)[selected_value].mean().reset_index()
                        month_grouped.columns = ["Month", selected_value]
                        
                        # Add month names
                        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                        month_grouped["Month Name"] = month_grouped["Month"].apply(lambda x: month_names[x-1])
                        
                        # Create bar chart
                        fig = create_bar_chart(
                            month_grouped,
                            x="Month Name",
                            y=selected_value,
                            title=f"{selected_value} by Month"
                        )
                        
                        # Display chart
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Create day-of-week seasonality chart
                    if time_period in ["day"]:
                        # Add day of week column
                        temp_df = df.copy()
                        temp_df[selected_date] = date_series
                        
                        # Group by day of week
                        dow_grouped = temp_df.groupby(temp_df[selected_date].dt.dayofweek)[selected_value].mean().reset_index()
                        dow_grouped.columns = ["Day of Week", selected_value]
                        
                        # Add day names
                        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                        dow_grouped["Day Name"] = dow_grouped["Day of Week"].apply(lambda x: day_names[x])
                        
                        # Create bar chart
                        fig = create_bar_chart(
                            dow_grouped,
                            x="Day Name",
                            y=selected_value,
                            title=f"{selected_value} by Day of Week"
                        )
                        
                        # Display chart
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select date and value columns for time series analysis.")
    
    elif selected_analysis == "Missing Values Analysis":
        st.markdown("## Missing Values Analysis")
        
        # Display missing values summary
        display_missing_values_summary(df)
        
        # Get missing threshold
        missing_threshold = st.session_state.get("missing_threshold", 0.05)
        
        # Get columns with missing values above threshold
        missing_counts = df.isna().sum()
        missing_pcts = missing_counts / len(df)
        high_missing_cols = missing_pcts[missing_pcts > missing_threshold].index.tolist()
        
        if high_missing_cols:
            st.markdown(f"### Columns with >{missing_threshold*100:.1f}% Missing Values")
            
            # Create DataFrame for display
            high_missing_df = pd.DataFrame({
                "Column": high_missing_cols,
                "Missing Count": [missing_counts[col] for col in high_missing_cols],
                "Missing %": [missing_pcts[col] * 100 for col in high_missing_cols]
            })
            
            # Sort by missing percentage
            high_missing_df = high_missing_df.sort_values("Missing %", ascending=False)
            
            # Display DataFrame
            st.dataframe(high_missing_df, use_container_width=True)
            
            # Create bar chart
            fig = create_bar_chart(
                high_missing_df,
                x="Column",
                y="Missing %",
                title="Columns with High Missing Values",
                text="Missing %"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success(f"No columns with missing values above {missing_threshold*100:.1f}% threshold.")
    
    elif selected_analysis == "Outlier Analysis":
        # Get selected column
        selected_column = st.session_state.get("selected_column")
        
        if selected_column:
            st.markdown(f"## Outlier Analysis: {selected_column}")
            
            # Get outlier method and threshold
            outlier_method = st.session_state.get("outlier_method", "iqr")
            outlier_threshold = st.session_state.get("outlier_threshold", 1.5)
            
            # Display outlier summary
            display_outlier_summary(df, selected_column, method=outlier_method, threshold=outlier_threshold)
            
            # Detect outliers
            outliers = detect_outliers(df, selected_column, method=outlier_method, threshold=outlier_threshold)
            
            # Create DataFrame with outliers
            outlier_df = df[outliers].copy()
            
            if len(outlier_df) > 0:
                st.markdown(f"### Outlier Records ({len(outlier_df)} rows)")
                
                # Display outlier records
                st.dataframe(outlier_df, use_container_width=True)
                
                # Create scatter plot with outliers highlighted
                import plotly.express as px
                
                # Create a copy of the DataFrame with outlier flag
                plot_df = df.copy()
                plot_df["is_outlier"] = outliers
                
                # Create scatter plot
                fig = px.scatter(
                    plot_df,
                    x=plot_df.index,
                    y=selected_column,
                    color="is_outlier",
                    color_discrete_map={True: "red", False: "blue"},
                    title=f"Outliers in {selected_column}",
                    labels={"index": "Row Index", selected_column: selected_column, "is_outlier": "Is Outlier"}
                )
                
                # Display chart
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success(f"No outliers detected in {selected_column} using {outlier_method.upper()} method with threshold {outlier_threshold}.")
        else:
            st.warning("Please select a column for outlier analysis.")
else:
    st.info("Please select a dataset from the sidebar to begin analysis.")
