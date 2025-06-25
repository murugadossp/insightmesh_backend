# InsightMesh Frontend

A Streamlit-based frontend for the InsightMesh data analysis platform, powered by Google's Agentic Development Kit (ADK).

## Overview

The InsightMesh frontend provides a user-friendly interface for interacting with the InsightMesh backend, allowing users to:

- Upload and analyze datasets
- Explore pre-loaded sample datasets
- View interactive visualizations and statistics
- Generate and download analysis reports
- Monitor system health and agent status

## Directory Structure

```
frontend/
├── components/             # Reusable UI components
│   ├── api_client.py       # API communication layer
│   ├── charts.py           # Chart generation functions
│   └── metrics.py          # Metric display components
├── pages/                  # Multi-page app structure
│   ├── 01_📊_Dashboard.py  # Main analysis dashboard
│   ├── 02_📈_Analytics.py  # Advanced analytics
│   ├── 03_📄_Reports.py    # Report management
│   └── 04_⚙️_Monitor.py    # System monitoring
├── utils/                  # Frontend utilities
│   ├── data_processing.py  # Data transformation
│   └── styling.py          # Custom CSS/styling
├── streamlit_app.py        # Main Streamlit application
├── requirements.txt        # Frontend dependencies
└── run_app.sh              # Script to run the application
```

## Installation

1. Ensure you have Python 3.8+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

You can run the application using the provided script:

```bash
./run_app.sh
```

Or directly with Streamlit:

```bash
streamlit run streamlit_app.py
```

The application will be available at http://localhost:8501 by default.

## Features

### Dashboard

The main dashboard provides an overview of the data analysis process:

- File upload with drag-and-drop
- Sample dataset selection
- Real-time analysis progress
- Key metrics display
- Interactive charts
- AI insights panel

### Analytics

The analytics page offers advanced statistical analysis:

- Detailed statistical breakdowns
- Correlation matrices
- Trend analysis
- Predictive insights
- Custom visualizations

### Reports

The reports page allows you to manage generated reports:

- List all generated reports
- View HTML reports in iframe
- Download functionality
- Report comparison

### Monitor

The system monitor page provides insights into system health:

- Google ADK agent status
- API health monitoring
- Processing pipeline visualization
- Performance metrics

## API Communication

The frontend communicates with the InsightMesh backend API using the `APIClient` class in `components/api_client.py`. The API client handles:

- Authentication
- Request/response formatting
- Error handling
- Mock responses for development

## Development

To contribute to the frontend development:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## Dependencies

The frontend relies on the following key libraries:

- Streamlit: Web application framework
- Pandas: Data manipulation
- Plotly: Interactive visualizations
- NumPy: Numerical computing
- Requests: API communication

See `requirements.txt` for a complete list of dependencies.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
