import streamlit as st

def apply_custom_styling():
    """
    Apply custom styling to the Streamlit app.
    This includes custom CSS for various components.
    """
    # Define custom CSS
    custom_css = """
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #4285F4;
            --secondary-color: #34A853;
            --accent-color: #EA4335;
            --background-color: #FFFFFF;
            --text-color: #202124;
            --light-gray: #F8F9FA;
            --medium-gray: #DADCE0;
            --dark-gray: #5F6368;
        }
        
        /* Main container styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Header styling */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-color);
            font-weight: 600;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: var(--primary-color);
        }
        
        h2 {
            font-size: 2rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--medium-gray);
            padding-bottom: 0.5rem;
        }
        
        h3 {
            font-size: 1.5rem;
            margin-top: 1.2rem;
            margin-bottom: 0.8rem;
            color: var(--secondary-color);
        }
        
        /* Metric styling */
        [data-testid="stMetric"] {
            background-color: var(--light-gray);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1rem;
            font-weight: 600;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary-color);
        }
        
        /* Card styling */
        .stCard {
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            background-color: white;
        }
        
        /* Button styling */
        .stButton button {
            border-radius: 4px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: var(--light-gray);
        }
        
        /* Dataframe styling */
        .dataframe {
            border-collapse: collapse;
            width: 100%;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .dataframe th {
            background-color: var(--primary-color);
            color: white;
            font-weight: 600;
            text-align: left;
            padding: 0.75rem;
        }
        
        .dataframe td {
            padding: 0.75rem;
            border-bottom: 1px solid var(--medium-gray);
        }
        
        .dataframe tr:nth-child(even) {
            background-color: var(--light-gray);
        }
        
        /* Custom insight box */
        .insight-box {
            background-color: #E8F0FE;
            border-left: 4px solid var(--primary-color);
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
        }
        
        /* Status indicators */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .status-indicator-success {
            background-color: rgba(52, 168, 83, 0.15);
            color: #34A853;
        }
        
        .status-indicator-warning {
            background-color: rgba(251, 188, 5, 0.15);
            color: #F9AB00;
        }
        
        .status-indicator-error {
            background-color: rgba(234, 67, 53, 0.15);
            color: #EA4335;
        }
        
        .status-indicator-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-indicator-success .status-indicator-dot {
            background-color: #34A853;
        }
        
        .status-indicator-warning .status-indicator-dot {
            background-color: #F9AB00;
        }
        
        .status-indicator-error .status-indicator-dot {
            background-color: #EA4335;
        }
        
        /* Pipeline step */
        .pipeline-step {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            padding: 0.75rem;
            border-radius: 8px;
            background-color: var(--light-gray);
        }
        
        .pipeline-step-icon {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            margin-right: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .pipeline-step-completed .pipeline-step-icon {
            background-color: #34A853;
        }
        
        .pipeline-step-in-progress .pipeline-step-icon {
            background-color: #4285F4;
        }
        
        .pipeline-step-pending .pipeline-step-icon {
            background-color: #5F6368;
        }
        
        .pipeline-step-error .pipeline-step-icon {
            background-color: #EA4335;
        }
        
        .pipeline-step-content {
            flex: 1;
        }
        
        .pipeline-step-title {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        
        .pipeline-step-status {
            font-size: 0.85rem;
            color: var(--dark-gray);
        }
        
        /* Chart container */
        .chart-container {
            background-color: white;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        }
    </style>
    """
    
    # Inject custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

def create_insight_box(content):
    """
    Create a styled box for displaying insights.
    
    Args:
        content (str): The content to display in the insight box
    """
    insight_html = f"""
    <div class="insight-box">
        <p>{content}</p>
    </div>
    """
    
    st.markdown(insight_html, unsafe_allow_html=True)

def create_status_indicator(status_type, text):
    """
    Create a status indicator with the specified type and text.
    
    Args:
        status_type (str): The type of status ('success', 'warning', or 'error')
        text (str): The text to display in the status indicator
    """
    status_html = f"""
    <div class="status-indicator status-indicator-{status_type}">
        <div class="status-indicator-dot"></div>
        <div>{text}</div>
    </div>
    """
    
    st.markdown(status_html, unsafe_allow_html=True)

def create_pipeline_step(title, status, description=None):
    """
    Create a pipeline step with the specified title, status, and description.
    
    Args:
        title (str): The title of the pipeline step
        status (str): The status of the pipeline step ('completed', 'in-progress', 'pending', or 'error')
        description (str, optional): A description of the pipeline step
    """
    # Determine status text and icon
    if status == 'completed':
        status_text = "Completed"
        icon = "✓"
    elif status == 'in-progress':
        status_text = "In Progress"
        icon = "⟳"
    elif status == 'error':
        status_text = "Error"
        icon = "✗"
    else:  # pending
        status_text = "Pending"
        icon = "⋯"
    
    # Create description text if provided
    description_html = f"<div>{description}</div>" if description else ""
    
    # Create pipeline step HTML
    pipeline_step_html = f"""
    <div class="pipeline-step pipeline-step-{status}">
        <div class="pipeline-step-icon">{icon}</div>
        <div class="pipeline-step-content">
            <div class="pipeline-step-title">{title}</div>
            <div class="pipeline-step-status">{status_text}</div>
            {description_html}
        </div>
    </div>
    """
    
    st.markdown(pipeline_step_html, unsafe_allow_html=True)

def create_chart_container(chart_function, *args, **kwargs):
    """
    Create a container for a chart with consistent styling.
    
    Args:
        chart_function (callable): The function to call to create the chart
        *args: Positional arguments to pass to the chart function
        **kwargs: Keyword arguments to pass to the chart function
    """
    # Create container
    container_html = """
    <div class="chart-container">
    """
    
    st.markdown(container_html, unsafe_allow_html=True)
    
    # Create chart
    chart = chart_function(*args, **kwargs)
    
    # Display chart
    st.plotly_chart(chart, use_container_width=True)
    
    # Close container
    st.markdown("</div>", unsafe_allow_html=True)
