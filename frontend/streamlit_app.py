import streamlit as st
import pandas as pd
import os
import sys
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from components.api_client import APIClient
from components.charts import create_bar_chart, create_line_chart, create_pie_chart
from components.metrics import display_metrics, display_data_summary
from utils.styling import apply_custom_styling, create_insight_box, create_status_indicator, create_pipeline_step
from utils.data_processing import load_csv, detect_column_types, calculate_summary_statistics, create_sample_datasets_info

# Set page configuration
st.set_page_config(
    page_title="InsightMesh - Data Analysis Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Initialize API client
api_client = APIClient(base_url="http://localhost:8000")

# Page header
st.title("🔍 InsightMesh")
st.markdown("### AI-Powered Data Analysis Platform")

# Create columns for intro
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    Welcome to InsightMesh, an intelligent data analysis platform powered by Google's Agentic Development Kit (ADK).
    
    InsightMesh transforms your data into actionable insights through a pipeline of specialized AI agents:
    
    1. **Ingestor Agent** - Loads and prepares your data
    2. **Cleaner Agent** - Handles missing values and outliers
    3. **Analyzer Agent** - Performs statistical analysis
    4. **Summarizer Agent** - Generates insights and recommendations
    
    Upload your data or select a sample dataset to get started!
    """)
    
    # Create quick start buttons
    st.markdown("### Quick Start")
    
    # Create columns for buttons
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/01_📊_Dashboard.py")
    
    with btn_col2:
        if st.button("📈 Analytics", use_container_width=True):
            st.switch_page("pages/02_📈_Analytics.py")
    
    with btn_col3:
        if st.button("📄 Reports", use_container_width=True):
            st.switch_page("pages/03_📄_Reports.py")

with col2:
    # Display platform status
    st.markdown("### Platform Status")
    
    # Get health data
    health_data = api_client.get_health()
    
    if health_data:
        # Create status indicator
        status = health_data.get("status", "unknown")
        status_type = "success" if status == "healthy" else "warning" if status == "degraded" else "error"
        create_status_indicator(status_type, f"System Status: {status.capitalize()}")
        
        # Display metrics
        st.metric("API Uptime", f"{health_data.get('uptime_seconds', 0) / 3600:.1f} hours")
        st.metric("Reports Generated", f"{health_data.get('reports_generated_total', 0):,}")
    else:
        create_status_indicator("error", "System Status: Offline")
        st.warning("Unable to connect to the API. Please check if the server is running.")

# Display sample datasets
st.markdown("### Sample Datasets")

# Get sample datasets info
sample_datasets = create_sample_datasets_info()

# Create tabs for dataset categories
categories = list(set(info["category"] for info in sample_datasets.values()))
tabs = st.tabs(categories)

# Display datasets by category
for i, category in enumerate(categories):
    with tabs[i]:
        # Filter datasets by category
        category_datasets = {filename: info for filename, info in sample_datasets.items() 
                            if info["category"] == category}
        
        # Create columns for dataset cards
        cols = st.columns(3)
        
        # Display datasets in cards
        for j, (filename, info) in enumerate(category_datasets.items()):
            # Determine which column to use
            col = cols[j % 3]
            
            with col:
                # Create a card for the dataset
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                    <h4>{info['name']}</h4>
                    <p>{info['description']}</p>
                    <p><strong>Size:</strong> {info['rows']} rows, {info['columns']} columns</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add a button to analyze the dataset
                if st.button(f"Analyze {info['name']}", key=f"analyze_{filename}"):
                    # Redirect to dashboard with selected dataset
                    st.session_state.selected_sample = filename
                    st.switch_page("pages/01_📊_Dashboard.py")

# Display features
st.markdown("### Key Features")

# Create columns for features
feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    #### 🤖 AI-Powered Analysis
    
    - Intelligent data cleaning
    - Automated statistical analysis
    - Natural language insights
    - Actionable recommendations
    """)

with feat_col2:
    st.markdown("""
    #### 📊 Interactive Visualizations
    
    - Dynamic charts and graphs
    - Correlation analysis
    - Time series forecasting
    - Outlier detection
    """)

with feat_col3:
    st.markdown("""
    #### 📱 User-Friendly Interface
    
    - Intuitive dashboard
    - Customizable reports
    - Real-time processing
    - Multi-page navigation
    """)

# Display pipeline visualization
st.markdown("### How It Works")

# Create a container for the pipeline
pipeline_container = st.container()

with pipeline_container:
    # Create a visual representation of the pipeline
    st.markdown("""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-top: 15px;">
        <h3 style="margin-top: 0;">Data Processing Pipeline</h3>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #4285F4; color: white; display: flex; justify-content: center; align-items: center; margin: 0 auto;">1</div>
                <div style="margin-top: 10px;">Ingestor</div>
            </div>
            <div style="flex-grow: 1; height: 2px; background-color: #ddd; margin: 0 10px;"></div>
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #34A853; color: white; display: flex; justify-content: center; align-items: center; margin: 0 auto;">2</div>
                <div style="margin-top: 10px;">Cleaner</div>
            </div>
            <div style="flex-grow: 1; height: 2px; background-color: #ddd; margin: 0 10px;"></div>
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #FBBC05; color: white; display: flex; justify-content: center; align-items: center; margin: 0 auto;">3</div>
                <div style="margin-top: 10px;">Analyzer</div>
            </div>
            <div style="flex-grow: 1; height: 2px; background-color: #ddd; margin: 0 10px;"></div>
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #EA4335; color: white; display: flex; justify-content: center; align-items: center; margin: 0 auto;">4</div>
                <div style="margin-top: 10px;">Summarizer</div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 20px;">
            <div style="text-align: center; width: 22%;">
                <div style="font-weight: bold;">Data Ingestion</div>
                <div>Loads CSV data into structured format</div>
            </div>
            <div style="text-align: center; width: 22%;">
                <div style="font-weight: bold;">Data Cleaning</div>
                <div>Handles missing values and outliers</div>
            </div>
            <div style="text-align: center; width: 22%;">
                <div style="font-weight: bold;">Data Analysis</div>
                <div>Performs statistical analysis</div>
            </div>
            <div style="text-align: center; width: 22%;">
                <div style="font-weight: bold;">Insight Generation</div>
                <div>Creates reports with insights</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>InsightMesh is powered by Google's Agentic Development Kit (ADK).</p>
    <p>© 2025 InsightMesh. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
