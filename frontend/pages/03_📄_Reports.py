import streamlit as st
import pandas as pd
import os
import sys
import time
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.api_client import APIClient
from utils.styling import apply_custom_styling, create_insight_box, create_status_indicator

# Set page configuration
st.set_page_config(
    page_title="Reports - InsightMesh",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Initialize API client
api_client = APIClient(base_url="http://localhost:8000")

# Initialize session state
if 'selected_report' not in st.session_state:
    st.session_state.selected_report = None
if 'report_content' not in st.session_state:
    st.session_state.report_content = None
if 'reports_list' not in st.session_state:
    st.session_state.reports_list = None

# Page header
st.title("📄 Reports")
st.markdown("### View and download generated analysis reports")

# Function to load reports
def load_reports():
    with st.spinner("Loading reports..."):
        # Get reports from API
        reports = api_client.get_reports()
        
        # Update session state
        st.session_state.reports_list = reports
        
        return reports

# Function to load report content
def load_report_content(report_id):
    with st.spinner(f"Loading report {report_id}..."):
        # Get report content from API
        report = api_client.get_report(report_id)
        
        # Update session state
        st.session_state.report_content = report
        st.session_state.selected_report = report_id
        
        return report

# Function to delete report
def delete_report(report_id):
    with st.spinner(f"Deleting report {report_id}..."):
        # Delete report using API
        result = api_client.delete_report(report_id)
        
        # Check if deletion was successful
        if result.get("success", False):
            # Remove from session state
            if st.session_state.selected_report == report_id:
                st.session_state.selected_report = None
                st.session_state.report_content = None
            
            # Reload reports
            load_reports()
            
            return True
        else:
            return False

# Create columns for layout
col1, col2 = st.columns([1, 3])

# Reports list sidebar
with col1:
    st.markdown("### Reports List")
    
    # Refresh button
    if st.button("🔄 Refresh Reports"):
        load_reports()
    
    # Load reports if not already loaded
    if st.session_state.reports_list is None:
        reports = load_reports()
    else:
        reports = st.session_state.reports_list
    
    # Display reports list
    if reports and "reports" in reports and len(reports["reports"]) > 0:
        # Create a container for the reports list
        reports_container = st.container()
        
        with reports_container:
            # Display each report as a selectable card
            for report in reports["reports"]:
                report_id = report["report_id"]
                filename = report["filename"]
                created_at = report["created_at"]
                file_type = report.get("file_type", "Data")
                
                # Format created date
                try:
                    created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    created_str = created_date.strftime("%b %d, %Y %H:%M")
                except:
                    created_str = created_at
                
                # Create a card for the report
                card_html = f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; 
                            background-color: {'#e8f0fe' if st.session_state.selected_report == report_id else 'white'};">
                    <h4 style="margin-top: 0;">{filename}</h4>
                    <p><strong>Type:</strong> {file_type}</p>
                    <p><strong>Created:</strong> {created_str}</p>
                </div>
                """
                
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Create columns for buttons
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    # View button
                    if st.button("View", key=f"view_{report_id}"):
                        load_report_content(report_id)
                
                with btn_col2:
                    # Delete button
                    if st.button("Delete", key=f"delete_{report_id}"):
                        success = delete_report(report_id)
                        if success:
                            st.success(f"Report {filename} deleted successfully!")
                        else:
                            st.error(f"Failed to delete report {filename}.")
    else:
        st.info("No reports found. Generate reports by analyzing datasets in the Dashboard.")

# Report content main area
with col2:
    # Display report content if selected
    if st.session_state.selected_report and st.session_state.report_content:
        report = st.session_state.report_content
        
        # Display report header
        st.markdown(f"## {report['filename']}")
        
        # Create columns for metadata
        meta_col1, meta_col2, meta_col3 = st.columns(3)
        
        with meta_col1:
            st.markdown(f"**Report ID:** {report['report_id']}")
            st.markdown(f"**Created:** {report['created_at']}")
        
        with meta_col2:
            if "metadata" in report:
                st.markdown(f"**Dataset:** {report['metadata'].get('dataset_name', 'Unknown')}")
                st.markdown(f"**Rows:** {report['metadata'].get('rows', 'Unknown')}")
                st.markdown(f"**Columns:** {report['metadata'].get('columns', 'Unknown')}")
        
        with meta_col3:
            if "metadata" in report:
                st.markdown(f"**Analysis Duration:** {report['metadata'].get('analysis_duration_ms', 0)/1000:.2f} seconds")
            st.markdown(f"**Size:** {report['size_bytes']/1024:.1f} KB")
        
        # Create download button
        st.download_button(
            label="📥 Download Report",
            data=report.get("content", "No content available"),
            file_name=report['filename'],
            mime="text/html"
        )
        
        # Display report content
        st.markdown("### Report Preview")
        
        # Create a container with fixed height for the report preview
        report_container = st.container()
        
        with report_container:
            # Display report content in an iframe
            report_content = report.get("content", "<html><body><p>No content available</p></body></html>")
            
            # Create an iframe to display the HTML content
            iframe_height = 600
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 0; height: {iframe_height}px; overflow: hidden;">
                    <iframe srcdoc='{report_content}' style="width: 100%; height: 100%; border: none;"></iframe>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        # Display placeholder
        st.markdown("## Report Viewer")
        st.info("Select a report from the list to view its content.")
        
        # Display sample report structure
        st.markdown("### Sample Report Structure")
        
        # Create a container for the sample report
        sample_container = st.container()
        
        with sample_container:
            st.markdown("""
            InsightMesh reports typically include:
            
            1. **Executive Summary**: Key findings and insights at a glance
            2. **Data Overview**: Information about the dataset analyzed
            3. **Data Quality Assessment**: Analysis of data completeness and quality
            4. **Statistical Analysis**: Detailed statistical breakdowns of key metrics
            5. **Visualizations**: Charts and graphs illustrating important patterns
            6. **Insights & Recommendations**: AI-generated insights and actionable recommendations
            
            Reports are generated in HTML format for rich interactive viewing and can be downloaded for sharing.
            """)
            
            # Display sample report image
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-top: 15px;">
                <h3>Sample Report Preview</h3>
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                    <div style="width: 30%; background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
                        <h4 style="margin-top: 0;">Executive Summary</h4>
                        <p>The analysis reveals strong performance in Category A, with a 15% increase in key metrics compared to baseline.</p>
                    </div>
                    <div style="width: 65%; background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
                        <h4 style="margin-top: 0;">Key Metrics</h4>
                        <div style="display: flex; justify-content: space-between;">
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 24px; font-weight: bold; color: #4285F4;">15%</div>
                                <div>Growth</div>
                            </div>
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 24px; font-weight: bold; color: #34A853;">45%</div>
                                <div>Category A</div>
                            </div>
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 24px; font-weight: bold; color: #EA4335;">12%</div>
                                <div>Below Target</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                    <h4 style="margin-top: 0;">Visualizations</h4>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="width: 48%; height: 150px; background-color: #e8f0fe; border-radius: 5px; display: flex; justify-content: center; align-items: center;">
                            [Bar Chart Placeholder]
                        </div>
                        <div style="width: 48%; height: 150px; background-color: #e8f0fe; border-radius: 5px; display: flex; justify-content: center; align-items: center;">
                            [Line Chart Placeholder]
                        </div>
                    </div>
                </div>
                <div style="background-color: #f8f0fe; padding: 10px; border-radius: 5px;">
                    <h4 style="margin-top: 0;">Recommendations</h4>
                    <ul>
                        <li>Consider reallocating resources to boost performance in underperforming areas.</li>
                        <li>Focus on expanding the high-performing categories given their strong results.</li>
                        <li>Implement a monitoring system to track performance over time.</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>Reports are generated using Google's Agentic Development Kit (ADK) and can be downloaded in HTML format.</p>
</div>
""", unsafe_allow_html=True)
