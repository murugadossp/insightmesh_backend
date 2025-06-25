import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import time
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.api_client import APIClient
from components.charts import create_bar_chart, create_line_chart, create_pie_chart
from utils.styling import apply_custom_styling, create_status_indicator, create_pipeline_step

# Set page configuration
st.set_page_config(
    page_title="Monitor - InsightMesh",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Initialize API client
api_client = APIClient(base_url="http://localhost:8000")

# Initialize session state
if 'health_data' not in st.session_state:
    st.session_state.health_data = None
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None

# Page header
st.title("⚙️ System Monitor")
st.markdown("### Monitor system health and agent status")

# Function to load health data
def load_health_data():
    with st.spinner("Loading health data..."):
        # Get health data from API
        health_data = api_client.get_health()
        
        # Update session state
        st.session_state.health_data = health_data
        st.session_state.last_refresh = datetime.now()
        
        return health_data

# Function to load agent status
def load_agent_status():
    with st.spinner("Loading agent status..."):
        # Get agent status from API
        agent_status = api_client.get_agent_status()
        
        # Update session state
        st.session_state.agent_status = agent_status
        
        return agent_status

# Create refresh button
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🔄 Refresh Data"):
        load_health_data()
        load_agent_status()

with col2:
    # Display last refresh time
    if st.session_state.last_refresh:
        st.markdown(f"**Last Refresh:** {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    else:
        st.markdown("**Last Refresh:** Never")

with col3:
    # Auto-refresh checkbox
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
    if auto_refresh:
        # Check if 30 seconds have passed since last refresh
        if (st.session_state.last_refresh is None or 
            datetime.now() - st.session_state.last_refresh > timedelta(seconds=30)):
            load_health_data()
            load_agent_status()
            st.experimental_rerun()

# Load data if not already loaded
if st.session_state.health_data is None:
    health_data = load_health_data()
else:
    health_data = st.session_state.health_data

if st.session_state.agent_status is None:
    agent_status = load_agent_status()
else:
    agent_status = st.session_state.agent_status

# Create tabs for different sections
system_tab, agents_tab, performance_tab, logs_tab = st.tabs([
    "System Health", "Agent Status", "Performance Metrics", "System Logs"
])

# System Health tab
with system_tab:
    st.markdown("## System Health Overview")
    
    # Display system status
    if health_data:
        # Create status indicator
        status = health_data.get("status", "unknown")
        status_type = "success" if status == "healthy" else "warning" if status == "degraded" else "error"
        create_status_indicator(status_type, f"System Status: {status.capitalize()}")
        
        # Create columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Uptime
            uptime_seconds = health_data.get("uptime_seconds", 0)
            uptime_hours = uptime_seconds / 3600
            uptime_days = uptime_hours / 24
            
            if uptime_days >= 1:
                uptime_str = f"{uptime_days:.1f} days"
            elif uptime_hours >= 1:
                uptime_str = f"{uptime_hours:.1f} hours"
            else:
                uptime_str = f"{uptime_seconds:.0f} seconds"
            
            st.metric("Uptime", uptime_str)
            
            # Framework
            st.metric("Framework", health_data.get("framework", "Unknown"))
        
        with col2:
            # Memory usage
            memory_usage = health_data.get("memory_usage_mb", 0)
            st.metric("Memory Usage", f"{memory_usage} MB")
            
            # CPU usage
            cpu_usage = health_data.get("cpu_usage_percent", 0)
            st.metric("CPU Usage", f"{cpu_usage}%")
        
        with col3:
            # API requests
            api_requests_total = health_data.get("api_requests_total", 0)
            st.metric("Total API Requests", f"{api_requests_total:,}")
            
            # API requests last hour
            api_requests_last_hour = health_data.get("api_requests_last_hour", 0)
            st.metric("API Requests (Last Hour)", f"{api_requests_last_hour:,}")
        
        with col4:
            # Reports generated
            reports_generated_total = health_data.get("reports_generated_total", 0)
            st.metric("Total Reports Generated", f"{reports_generated_total:,}")
            
            # Reports generated last day
            reports_generated_last_day = health_data.get("reports_generated_last_day", 0)
            st.metric("Reports Generated (Last Day)", f"{reports_generated_last_day:,}")
        
        # Create system health charts
        st.markdown("### System Health Metrics")
        
        # Create columns for charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Create mock data for CPU usage over time
            st.markdown("#### CPU Usage Over Time")
            
            # Create mock data
            hours = 24
            timestamps = [(datetime.now() - timedelta(hours=i)).strftime("%H:%M") for i in range(hours, 0, -1)]
            cpu_values = [cpu_usage * (0.5 + 0.5 * np.sin(i / 4)) for i in range(hours)]
            
            cpu_df = pd.DataFrame({
                "Timestamp": timestamps,
                "CPU Usage (%)": cpu_values
            })
            
            # Create line chart
            fig = create_line_chart(
                cpu_df,
                x="Timestamp",
                y="CPU Usage (%)",
                title="CPU Usage (Last 24 Hours)"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            # Create mock data for memory usage over time
            st.markdown("#### Memory Usage Over Time")
            
            # Create mock data
            memory_values = [memory_usage * (0.7 + 0.3 * np.sin(i / 6)) for i in range(hours)]
            
            memory_df = pd.DataFrame({
                "Timestamp": timestamps,
                "Memory Usage (MB)": memory_values
            })
            
            # Create line chart
            fig = create_line_chart(
                memory_df,
                x="Timestamp",
                y="Memory Usage (MB)",
                title="Memory Usage (Last 24 Hours)"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        # Create API request charts
        st.markdown("### API Request Metrics")
        
        # Create columns for charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Create mock data for API requests by hour
            st.markdown("#### API Requests by Hour")
            
            # Create mock data
            hourly_requests = [int(api_requests_last_hour * (0.5 + 0.5 * np.sin(i / 3))) for i in range(24)]
            hours_of_day = [f"{i:02d}:00" for i in range(24)]
            
            hourly_df = pd.DataFrame({
                "Hour": hours_of_day,
                "Requests": hourly_requests
            })
            
            # Create bar chart
            fig = create_bar_chart(
                hourly_df,
                x="Hour",
                y="Requests",
                title="API Requests by Hour (Last 24 Hours)"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            # Create mock data for API requests by endpoint
            st.markdown("#### API Requests by Endpoint")
            
            # Create mock data
            endpoints = ["analyze", "reports", "health", "agents/status", "other"]
            endpoint_counts = [50, 25, 10, 10, 5]
            
            endpoint_df = pd.DataFrame({
                "Endpoint": endpoints,
                "Requests": endpoint_counts
            })
            
            # Create pie chart
            fig = create_pie_chart(
                endpoint_df,
                names="Endpoint",
                values="Requests",
                title="API Requests by Endpoint"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Failed to load system health data. Please try refreshing.")

# Agent Status tab
with agents_tab:
    st.markdown("## Agent Status Overview")
    
    # Display agent status
    if agent_status and "agents" in agent_status:
        # Create columns for agent cards
        agent_cols = st.columns(2)
        
        # Display each agent
        for i, agent in enumerate(agent_status["agents"]):
            # Determine which column to use
            col = agent_cols[i % 2]
            
            with col:
                # Create a card for the agent
                st.markdown(f"### {agent['agent_name'].capitalize()} Agent")
                
                # Create status indicator
                status = agent.get("status", "unknown")
                status_type = "success" if status == "ready" else "warning" if status == "busy" else "error"
                create_status_indicator(status_type, f"Status: {status.capitalize()}")
                
                # Display agent info
                st.markdown(f"**Description:** {agent.get('description', 'No description')}")
                
                # Format last execution time
                last_execution = agent.get("last_execution", "Never")
                try:
                    last_exec_date = datetime.fromisoformat(last_execution.replace("Z", "+00:00"))
                    last_exec_str = last_exec_date.strftime("%b %d, %Y %H:%M:%S")
                except:
                    last_exec_str = last_execution
                
                st.markdown(f"**Last Execution:** {last_exec_str}")
                
                # Create columns for metrics
                metric_col1, metric_col2 = st.columns(2)
                
                with metric_col1:
                    st.metric("Executions", f"{agent.get('executions_count', 0):,}")
                
                with metric_col2:
                    st.metric("Avg. Execution Time", f"{agent.get('average_execution_time_ms', 0):.0f} ms")
                
                # Create a mock execution time chart
                st.markdown("#### Execution Time History")
                
                # Create mock data
                executions = 10
                exec_times = [agent.get('average_execution_time_ms', 500) * (0.7 + 0.6 * np.random.random()) for _ in range(executions)]
                exec_ids = [f"Exec {i+1}" for i in range(executions)]
                
                exec_df = pd.DataFrame({
                    "Execution": exec_ids,
                    "Time (ms)": exec_times
                })
                
                # Create bar chart
                fig = create_bar_chart(
                    exec_df,
                    x="Execution",
                    y="Time (ms)",
                    title=f"{agent['agent_name'].capitalize()} Agent Execution Times"
                )
                
                # Display chart
                st.plotly_chart(fig, use_container_width=True)
        
        # Display pipeline visualization
        st.markdown("## Pipeline Visualization")
        
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
    else:
        st.warning("Failed to load agent status data. Please try refreshing.")

# Performance Metrics tab
with performance_tab:
    st.markdown("## System Performance Metrics")
    
    # Create mock performance data
    if health_data:
        # Create columns for time range selection
        time_col1, time_col2 = st.columns([1, 3])
        
        with time_col1:
            # Time range selection
            time_range = st.radio("Time Range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])
        
        with time_col2:
            # Metric selection
            metrics = st.multiselect(
                "Select Metrics",
                ["CPU Usage", "Memory Usage", "API Requests", "Response Time"],
                default=["CPU Usage", "Memory Usage"]
            )
        
        # Create performance charts
        if "CPU Usage" in metrics:
            st.markdown("### CPU Usage")
            
            # Create mock data
            if time_range == "Last 24 Hours":
                hours = 24
                timestamps = [(datetime.now() - timedelta(hours=i)).strftime("%H:%M") for i in range(hours, 0, -1)]
                cpu_values = [health_data.get("cpu_usage_percent", 15) * (0.5 + 0.5 * np.sin(i / 4)) for i in range(hours)]
            elif time_range == "Last 7 Days":
                days = 7
                timestamps = [(datetime.now() - timedelta(days=i)).strftime("%m-%d") for i in range(days, 0, -1)]
                cpu_values = [health_data.get("cpu_usage_percent", 15) * (0.5 + 0.5 * np.sin(i / 2)) for i in range(days)]
            else:  # Last 30 Days
                days = 30
                timestamps = [(datetime.now() - timedelta(days=i)).strftime("%m-%d") for i in range(days, 0, -1)]
                cpu_values = [health_data.get("cpu_usage_percent", 15) * (0.5 + 0.5 * np.sin(i / 5)) for i in range(days)]
            
            cpu_df = pd.DataFrame({
                "Timestamp": timestamps,
                "CPU Usage (%)": cpu_values
            })
            
            # Create line chart
            fig = create_line_chart(
                cpu_df,
                x="Timestamp",
                y="CPU Usage (%)",
                title=f"CPU Usage ({time_range})"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        if "Memory Usage" in metrics:
            st.markdown("### Memory Usage")
            
            # Create mock data
            if time_range == "Last 24 Hours":
                hours = 24
                timestamps = [(datetime.now() - timedelta(hours=i)).strftime("%H:%M") for i in range(hours, 0, -1)]
                memory_values = [health_data.get("memory_usage_mb", 512) * (0.7 + 0.3 * np.sin(i / 6)) for i in range(hours)]
            elif time_range == "Last 7 Days":
                days = 7
                timestamps = [(datetime.now() - timedelta(days=i)).strftime("%m-%d") for i in range(days, 0, -1)]
                memory_values = [health_data.get("memory_usage_mb", 512) * (0.7 + 0.3 * np.sin(i / 3)) for i in range(days)]
            else:  # Last 30 Days
                days = 30
                timestamps = [(datetime.now() - timedelta(days=i)).strftime("%m-%d") for i in range(days, 0, -1)]
                memory_values = [health_data.get("memory_usage_mb", 512) * (0.7 + 0.3 * np.sin(i / 7)) for i in range(days)]
            
            memory_df = pd.DataFrame({
                "Timestamp": timestamps,
                "Memory Usage (MB)": memory_values
            })
            
            # Create line chart
            fig = create_line_chart(
                memory_df,
                x="Timestamp",
                y="Memory Usage (MB)",
                title=f"Memory Usage ({time_range})"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        if "API Requests" in metrics:
            st.markdown("### API Requests")
            
            # Create mock data
            if time_range == "Last 24 Hours":
                hours = 24
                timestamps = [(datetime.now() - timedelta(hours=i)).strftime("%H:%M") for i in range(hours, 0, -1)]
                request_values = [health_data.get("api_requests_last_hour", 45) * (0.5 + 0.5 * np.sin(i / 3)) for i in range(hours)]
            elif time_range == "Last 7 Days":
                days = 7
                timestamps = [(datetime.now() - timedelta(days=i)).strftime("%m-%d") for i in range(days, 0, -1)]
                request_values = [health_data.get("api_requests_last_hour", 45) * 24 * (0.5 + 0.5 * np.sin(i / 2)) for i in range(days)]
            else:  # Last 30 Days
                days = 30
                timestamps = [(datetime.now() - timedelta(days=i)).strftime("%m-%d") for i in range(days, 0, -1)]
                request_values = [health_data.get("api_requests_last_hour", 45) * 24 * (0.5 + 0.5 * np.sin(i / 5)) for i in range(days)]
            
            request_df = pd.DataFrame({
                "Timestamp": timestamps,
                "API Requests": request_values
            })
            
            # Create line chart
            fig = create_line_chart(
                request_df,
                x="Timestamp",
                y="API Requests",
                title=f"API Requests ({time_range})"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
        
        if "Response Time" in metrics:
            st.markdown("### API Response Time")
            
            # Create mock data
            if time_range == "Last 24 Hours":
                hours = 24
                timestamps = [(datetime.now() - timedelta(hours=i)).strftime("%H:%M") for i in range(hours, 0, -1)]
                response_values = [100 * (0.7 + 0.3 * np.sin(i / 4)) for i in range(hours)]
            elif time_range == "Last 7 Days":
                days = 7
                timestamps = [(datetime.now() - timedelta(days=i)).strftime("%m-%d") for i in range(days, 0, -1)]
                response_values = [100 * (0.7 + 0.3 * np.sin(i / 2)) for i in range(days)]
            else:  # Last 30 Days
                days = 30
                timestamps = [(datetime.now() - timedelta(days=i)).strftime("%m-%d") for i in range(days, 0, -1)]
                response_values = [100 * (0.7 + 0.3 * np.sin(i / 6)) for i in range(days)]
            
            response_df = pd.DataFrame({
                "Timestamp": timestamps,
                "Response Time (ms)": response_values
            })
            
            # Create line chart
            fig = create_line_chart(
                response_df,
                x="Timestamp",
                y="Response Time (ms)",
                title=f"API Response Time ({time_range})"
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Failed to load performance data. Please try refreshing.")

# System Logs tab
with logs_tab:
    st.markdown("## System Logs")
    
    # Create mock log data
    log_levels = st.multiselect(
        "Log Levels",
        ["INFO", "WARNING", "ERROR", "DEBUG"],
        default=["INFO", "WARNING", "ERROR"]
    )
    
    # Create mock logs
    logs = []
    
    # INFO logs
    if "INFO" in log_levels:
        logs.extend([
            {"timestamp": "2025-06-23 19:30:15", "level": "INFO", "message": "Server started successfully"},
            {"timestamp": "2025-06-23 19:25:32", "level": "INFO", "message": "Processed sample_sales_data.csv"},
            {"timestamp": "2025-06-23 19:20:47", "level": "INFO", "message": "Generated report sample_sales_data_20250623_190858.html"},
            {"timestamp": "2025-06-23 19:15:10", "level": "INFO", "message": "User uploaded new dataset"},
            {"timestamp": "2025-06-23 19:10:05", "level": "INFO", "message": "Cleaner agent processed dataset with 95% quality score"}
        ])
    
    # WARNING logs
    if "WARNING" in log_levels:
        logs.extend([
            {"timestamp": "2025-06-23 19:18:22", "level": "WARNING", "message": "Dataset contains 5% missing values"},
            {"timestamp": "2025-06-23 19:05:17", "level": "WARNING", "message": "Memory usage approaching 80% threshold"},
            {"timestamp": "2025-06-23 18:55:30", "level": "WARNING", "message": "API request rate increased by 30% in the last hour"}
        ])
    
    # ERROR logs
    if "ERROR" in log_levels:
        logs.extend([
            {"timestamp": "2025-06-23 18:45:12", "level": "ERROR", "message": "Failed to process malformed CSV file"},
            {"timestamp": "2025-06-23 18:30:05", "level": "ERROR", "message": "Database connection timeout after 30 seconds"}
        ])
    
    # DEBUG logs
    if "DEBUG" in log_levels:
        logs.extend([
            {"timestamp": "2025-06-23 19:29:55", "level": "DEBUG", "message": "Ingestor agent initialized with config: {batch_size: 1000}"},
            {"timestamp": "2025-06-23 19:28:42", "level": "DEBUG", "message": "API request received: GET /health"},
            {"timestamp": "2025-06-23 19:27:30", "level": "DEBUG", "message": "Cleaner agent processing row 500/1000"},
            {"timestamp": "2025-06-23 19:26:15", "level": "DEBUG", "message": "Cache hit ratio: 0.85"},
            {"timestamp": "2025-06-23 19:25:03", "level": "DEBUG", "message": "Memory usage: 512MB, CPU usage: 15%"}
        ])
    
    # Sort logs by timestamp (newest first)
    logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Create DataFrame
    logs_df = pd.DataFrame(logs)
    
    # Apply styling to logs
    def color_logs(val):
        if val == "ERROR":
            return "background-color: #ffcccc"
        elif val == "WARNING":
            return "background-color: #fff2cc"
        elif val == "INFO":
            return "background-color: #e6f2ff"
        elif val == "DEBUG":
            return "background-color: #e6ffe6"
        return ""
    
    # Display logs
    st.dataframe(logs_df.style.applymap(color_logs, subset=["level"]), use_container_width=True)
    
    # Log statistics
    st.markdown("### Log Statistics")
    
    # Count logs by level
    level_counts = {}
    for level in ["INFO", "WARNING", "ERROR", "DEBUG"]:
        level_counts[level] = len([log for log in logs if log["level"] == level])
    
    # Create DataFrame
    level_df = pd.DataFrame({
        "Level": list(level_counts.keys()),
        "Count": list(level_counts.values())
    })
    
    # Create columns for charts
    log_col1, log_col2 = st.columns(2)
    
    with log_col1:
        # Create bar chart
        fig = create_bar_chart(
            level_df,
            x="Level",
            y="Count",
            title="Log Entries by Level"
        )
        
        # Display chart
        st.plotly_chart(fig, use_container_width=True)
    
    with log_col2:
        # Create pie chart
        fig = create_pie_chart(
            level_df,
            names="Level",
            values="Count",
            title="Log Distribution"
        )
        
        # Display chart
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>System monitoring powered by Google's Agentic Development Kit (ADK).</p>
</div>
""", unsafe_allow_html=True)
