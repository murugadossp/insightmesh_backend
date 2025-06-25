import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import time
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.api_client import APIClient
from components.charts import create_bar_chart, create_line_chart, create_pie_chart, create_scatter_plot
from components.metrics import display_metrics, display_data_summary
from utils.styling import apply_custom_styling, create_insight_box, create_status_indicator, create_pipeline_step
from utils.data_processing import load_csv, detect_column_types, calculate_summary_statistics, create_sample_datasets_info

# Set page configuration
st.set_page_config(
    page_title="Dashboard - InsightMesh",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Initialize API client
api_client = APIClient(base_url="http://localhost:8000")

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_dataset' not in st.session_state:
    st.session_state.current_dataset = None
if 'current_dataset_name' not in st.session_state:
    st.session_state.current_dataset_name = None
if 'processing_status' not in st.session_state:
    st.session_state.processing_status = None
if 'selected_sample' not in st.session_state:
    st.session_state.selected_sample = None

# Page header
st.title("📊 Dashboard")
st.markdown("### Upload your data or select a sample dataset for analysis")

# Create tabs for upload and sample selection
upload_tab, sample_tab = st.tabs(["Upload Data", "Sample Datasets"])

# Upload tab content
with upload_tab:
    st.markdown("### Upload your CSV file")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    # Upload options
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            delimiter = st.selectbox("Delimiter", [",", ";", "\t", "|"], index=0)
            encoding = st.selectbox("Encoding", ["utf-8", "latin-1", "iso-8859-1", "cp1252"], index=0)
        
        with col2:
            header = st.selectbox("Header Row", ["First Row", "No Header"], index=0)
            skip_rows = st.number_input("Skip Rows", min_value=0, value=0)
        
        # Preview data
        st.markdown("### Data Preview")
        
        # Load data with options
        header_option = 0 if header == "First Row" else None
        preview_df = load_csv(
            uploaded_file, 
            sep=delimiter, 
            encoding=encoding, 
            header=header_option, 
            skiprows=skip_rows,
            nrows=5
        )
        
        if preview_df is not None:
            st.dataframe(preview_df, use_container_width=True)
            
            # Analyze button
            if st.button("Analyze Data", key="analyze_upload"):
                with st.spinner("Analyzing data..."):
                    # Reset file pointer
                    uploaded_file.seek(0)
                    
                    # Update session state
                    st.session_state.processing_status = "processing"
                    st.session_state.current_dataset_name = uploaded_file.name
                    
                    # Call API to analyze file
                    analysis_results = api_client.analyze_file(uploaded_file)
                    
                    # Update session state
                    st.session_state.analysis_results = analysis_results
                    st.session_state.processing_status = "completed"
                    
                    # Reload the page to show results
                    st.experimental_rerun()
        else:
            st.error("Error loading file. Please check the file format and options.")

# Sample datasets tab content
with sample_tab:
    st.markdown("### Select a sample dataset")
    
    # Get sample datasets info
    sample_datasets = create_sample_datasets_info()
    
    # Create columns for sample dataset cards
    col1, col2, col3 = st.columns(3)
    
    # Display sample datasets in cards
    for i, (filename, info) in enumerate(sample_datasets.items()):
        # Determine which column to use
        col = col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3
        
        with col:
            # Create a card for the dataset
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                <h4>{info['name']}</h4>
                <p>{info['description']}</p>
                <p><strong>Category:</strong> {info['category']}</p>
                <p><strong>Size:</strong> {info['rows']} rows, {info['columns']} columns</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a button to select the dataset
            if st.button(f"Select {info['name']}", key=f"select_{filename}"):
                st.session_state.selected_sample = filename
                st.session_state.processing_status = "processing"
                st.session_state.current_dataset_name = info['name']
                
                # Call API to analyze sample
                with st.spinner(f"Analyzing {info['name']}..."):
                    analysis_results = api_client.analyze_sample(filename)
                    
                    # Update session state
                    st.session_state.analysis_results = analysis_results
                    st.session_state.processing_status = "completed"
                    
                    # Reload the page to show results
                    st.experimental_rerun()

# Display analysis results if available
if st.session_state.processing_status == "completed" and st.session_state.analysis_results is not None:
    st.markdown("---")
    st.markdown(f"## Analysis Results: {st.session_state.current_dataset_name}")
    
    # Get analysis results
    results = st.session_state.analysis_results
    
    # Display success message
    st.success(results['message'])
    
    # Create tabs for different sections
    overview_tab, insights_tab, visualizations_tab, report_tab = st.tabs([
        "Overview", "Insights", "Visualizations", "Report"
    ])
    
    # Overview tab
    with overview_tab:
        # Display data info
        st.markdown("### Dataset Information")
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Rows", f"{results['insights']['data_info']['rows']:,}")
            st.metric("Framework", results['insights']['framework'])
        
        with col2:
            st.metric("Columns", f"{results['insights']['data_info']['columns']:,}")
            st.metric("Pipeline Status", results['insights']['pipeline_execution'])
        
        with col3:
            # Calculate data quality score (mock)
            quality_score = 95  # This would come from the API in a real implementation
            st.metric("Data Quality Score", f"{quality_score}%")
            
            # Calculate processing time (mock)
            processing_time = 2.5  # This would come from the API in a real implementation
            st.metric("Processing Time", f"{processing_time:.1f} seconds")
        
        # Display pipeline steps
        st.markdown("### Processing Pipeline")
        
        # Create columns for pipeline steps
        col1, col2 = st.columns(2)
        
        with col1:
            # Display pipeline steps
            for step in results['processing_steps']:
                create_pipeline_step(
                    title=f"{step['step'].capitalize()} Agent",
                    status="completed" if step['status'] == "completed" else "error",
                    description=f"Processed {results['insights']['data_info']['rows']} rows and {results['insights']['data_info']['columns']} columns"
                )
        
        with col2:
            # Display cleaning info if available
            if 'cleaning_info' in results['insights']:
                st.markdown("### Data Cleaning Summary")
                
                # Display null summary
                null_summary = results['insights']['cleaning_info']['null_summary']
                
                # Count columns with missing values
                cols_with_nulls = sum(1 for count in null_summary.values() if count > 0)
                
                # Display metrics
                st.metric("Columns with Missing Values", cols_with_nulls)
                
                # Display suggestions
                if 'suggestions' in results['insights']['cleaning_info']:
                    st.markdown("#### Cleaning Suggestions")
                    for suggestion in results['insights']['cleaning_info']['suggestions']:
                        st.markdown(f"- {suggestion}")
    
    # Insights tab
    with insights_tab:
        st.markdown("### Key Insights")
        
        # Display summary
        create_insight_box(results['summary'])
        
        # Display analysis results if available
        if 'analysis_results' in results['insights']:
            st.markdown("### Statistical Analysis")
            
            # Get analysis results
            analysis_results = results['insights']['analysis_results']
            
            # Display analysis for each column
            for column, stats in analysis_results.items():
                with st.expander(f"{column} Analysis"):
                    # Create columns for metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Count", f"{stats['count']:,.0f}")
                    
                    with col2:
                        st.metric("Mean", f"{stats['mean']:,.2f}")
                    
                    with col3:
                        st.metric("Min", f"{stats['min']:,.2f}")
                    
                    with col4:
                        st.metric("Max", f"{stats['max']:,.2f}")
    
    # Visualizations tab
    with visualizations_tab:
        st.markdown("### Data Visualizations")
        
        # Create mock visualizations based on the dataset
        # In a real implementation, these would be generated based on the actual data
        
        # Create columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Create a bar chart
            st.markdown("#### Distribution by Category")
            
            # Create mock data
            mock_data = pd.DataFrame({
                'Category': ['A', 'B', 'C', 'D', 'E'],
                'Value': [25, 40, 30, 50, 45]
            })
            
            # Create chart
            fig = create_bar_chart(
                mock_data,
                x='Category',
                y='Value',
                title='Distribution by Category'
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create a pie chart
            st.markdown("#### Proportion by Segment")
            
            # Create mock data
            mock_data = pd.DataFrame({
                'Segment': ['Segment 1', 'Segment 2', 'Segment 3', 'Segment 4'],
                'Value': [35, 25, 20, 20]
            })
            
            # Create chart
            fig = create_pie_chart(
                mock_data,
                names='Segment',
                values='Value',
                title='Proportion by Segment'
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        # Create another row of charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Create a line chart
            st.markdown("#### Trend Over Time")
            
            # Create mock data
            dates = pd.date_range(start='2025-01-01', periods=12, freq='M')
            mock_data = pd.DataFrame({
                'Date': dates,
                'Value': [100, 120, 115, 130, 145, 160, 155, 170, 185, 190, 210, 200]
            })
            
            # Create chart
            fig = create_line_chart(
                mock_data,
                x='Date',
                y='Value',
                title='Trend Over Time'
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create a scatter plot
            st.markdown("#### Correlation Analysis")
            
            # Create mock data
            np.random.seed(42)
            x = np.random.normal(0, 1, 100)
            y = 0.8 * x + 0.2 * np.random.normal(0, 1, 100)
            mock_data = pd.DataFrame({
                'X': x,
                'Y': y
            })
            
            # Create chart
            fig = create_scatter_plot(
                mock_data,
                x='X',
                y='Y',
                title='Correlation Analysis',
                trendline='ols'
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
    
    # Report tab
    with report_tab:
        st.markdown("### Analysis Report")
        
        # Display report info
        if 'html_report' in results['insights']:
            report_id = results['insights']['html_report']['report_id']
            report_url = results['insights']['html_report']['report_url']
            
            st.markdown(f"#### Report ID: {report_id}")
            
            # Create columns for buttons
            col1, col2 = st.columns(2)
            
            with col1:
                # View report button
                if st.button("View Report", key="view_report"):
                    # In a real implementation, this would open the report in a new tab
                    st.markdown(f"Opening report at {report_url}...")
                    
                    # For demo purposes, display a mock report
                    st.markdown("### Sample Report Preview")
                    st.markdown("""
                    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-top: 15px;">
                        <h3>Data Analysis Report</h3>
                        <p><strong>Dataset:</strong> Sample Dataset</p>
                        <p><strong>Generated:</strong> June 23, 2025</p>
                        <p><strong>Summary:</strong> This report contains the analysis results for the sample dataset.</p>
                        <hr>
                        <h4>Key Findings</h4>
                        <ul>
                            <li>Finding 1: The data shows strong performance in certain areas, with a 15% increase in key metrics compared to baseline.</li>
                            <li>Finding 2: Category A is the top performer, contributing 45% of total value.</li>
                            <li>Finding 3: There's an opportunity to improve performance in underperforming areas, which are below targets by 12%.</li>
                        </ul>
                        <h4>Recommendations</h4>
                        <ul>
                            <li>Consider reallocating resources to boost performance in underperforming areas.</li>
                            <li>Focus on expanding the high-performing categories given their strong results.</li>
                            <li>Implement a monitoring system to track performance over time.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Download report button
                if st.button("Download Report", key="download_report"):
                    # In a real implementation, this would download the report
                    st.markdown(f"Downloading report {report_id}...")
                    
                    # For demo purposes, display a success message
                    st.success("Report downloaded successfully!")

# Display processing status if processing
elif st.session_state.processing_status == "processing":
    st.markdown("---")
    st.markdown(f"## Processing: {st.session_state.current_dataset_name}")
    
    # Display spinner
    with st.spinner("Processing data..."):
        # In a real implementation, this would be handled by the API
        # For demo purposes, simulate processing time
        progress_bar = st.progress(0)
        
        for i in range(100):
            # Update progress bar
            progress_bar.progress(i + 1)
            
            # Simulate processing time
            time.sleep(0.02)
        
        # Update session state
        st.session_state.processing_status = "completed"
        
        # Reload the page to show results
        st.experimental_rerun()
