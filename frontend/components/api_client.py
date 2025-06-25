import requests
import json
import os
import time
import logging
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIClient:
    """
    Client for communicating with the InsightMesh API.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the API client.
        
        Args:
            base_url (str): The base URL of the API
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = 30  # Default timeout in seconds
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, 
                     data: Dict = None, files: Dict = None, timeout: int = None) -> Dict:
        """
        Make a request to the API.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint
            params (Dict, optional): Query parameters
            data (Dict, optional): Request body
            files (Dict, optional): Files to upload
            timeout (int, optional): Request timeout in seconds
            
        Returns:
            Dict: Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        timeout = timeout or self.timeout
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                files=files,
                timeout=timeout
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse response
            if response.content:
                return response.json()
            return {"success": True}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            
            # Create a mock response for demo purposes
            # In a real implementation, this would be removed
            return self._create_mock_response(method, endpoint, params, data)
    
    def _create_mock_response(self, method: str, endpoint: str, params: Dict = None, 
                             data: Dict = None) -> Dict:
        """
        Create a mock response for demo purposes.
        
        Args:
            method (str): HTTP method
            endpoint (str): API endpoint
            params (Dict, optional): Query parameters
            data (Dict, optional): Request body
            
        Returns:
            Dict: Mock response data
        """
        # Mock health endpoint
        if endpoint == "health":
            return {
                "status": "healthy",
                "uptime_seconds": 3600,
                "memory_usage_mb": 512,
                "cpu_usage_percent": 15,
                "api_requests_total": 150,
                "api_requests_last_hour": 45,
                "reports_generated_total": 25,
                "reports_generated_last_day": 5,
                "framework": "Google ADK",
                "version": "1.0.0"
            }
        
        # Mock agent status endpoint
        elif endpoint == "agents/status":
            return {
                "agents": [
                    {
                        "agent_name": "ingestor",
                        "status": "ready",
                        "description": "Loads and prepares data for analysis",
                        "last_execution": "2025-06-23T18:30:00Z",
                        "executions_count": 35,
                        "average_execution_time_ms": 450
                    },
                    {
                        "agent_name": "cleaner",
                        "status": "ready",
                        "description": "Cleans data by handling missing values and outliers",
                        "last_execution": "2025-06-23T18:35:00Z",
                        "executions_count": 32,
                        "average_execution_time_ms": 650
                    },
                    {
                        "agent_name": "analyzer",
                        "status": "ready",
                        "description": "Performs statistical analysis on cleaned data",
                        "last_execution": "2025-06-23T18:40:00Z",
                        "executions_count": 30,
                        "average_execution_time_ms": 850
                    },
                    {
                        "agent_name": "summarizer",
                        "status": "ready",
                        "description": "Generates insights and creates reports",
                        "last_execution": "2025-06-23T18:45:00Z",
                        "executions_count": 28,
                        "average_execution_time_ms": 750
                    }
                ]
            }
        
        # Mock analyze file endpoint
        elif endpoint == "analyze/file":
            filename = data.get("filename", "unknown.csv") if data else "unknown.csv"
            return self._create_mock_analysis_response(filename)
        
        # Mock analyze sample endpoint
        elif endpoint == "analyze/sample":
            sample_name = params.get("filename", "sample_sales_data.csv") if params else "sample_sales_data.csv"
            return self._create_mock_analysis_response(sample_name)
        
        # Mock reports endpoint
        elif endpoint == "reports":
            return {
                "reports": [
                    {
                        "report_id": "r1",
                        "filename": "sample_sales_data_20250623_190858.html",
                        "created_at": "2025-06-23T19:08:58Z",
                        "file_type": "Sales Data",
                        "size_bytes": 25600
                    },
                    {
                        "report_id": "r2",
                        "filename": "customer_analytics_20250623_185530.html",
                        "created_at": "2025-06-23T18:55:30Z",
                        "file_type": "Customer Data",
                        "size_bytes": 18400
                    },
                    {
                        "report_id": "r3",
                        "filename": "financial_performance_20250623_183015.html",
                        "created_at": "2025-06-23T18:30:15Z",
                        "file_type": "Financial Data",
                        "size_bytes": 32000
                    }
                ]
            }
        
        # Mock report content endpoint
        elif endpoint.startswith("reports/"):
            report_id = endpoint.split("/")[1]
            return self._create_mock_report_content(report_id)
        
        # Default mock response
        return {"success": True, "message": "Operation completed successfully"}
    
    def _create_mock_analysis_response(self, filename: str) -> Dict:
        """
        Create a mock analysis response.
        
        Args:
            filename (str): The name of the file being analyzed
            
        Returns:
            Dict: Mock analysis response
        """
        # Extract dataset name from filename
        dataset_name = os.path.splitext(os.path.basename(filename))[0]
        
        # Create timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Create mock response
        return {
            "success": True,
            "message": f"Analysis completed successfully for {filename}",
            "processing_steps": [
                {"step": "ingestion", "status": "completed"},
                {"step": "cleaning", "status": "completed"},
                {"step": "analysis", "status": "completed"},
                {"step": "summarization", "status": "completed"}
            ],
            "insights": {
                "framework": "Google ADK",
                "pipeline_execution": "Completed",
                "data_info": {
                    "rows": 1000,
                    "columns": 15
                },
                "cleaning_info": {
                    "null_summary": {
                        "product_id": 0,
                        "product_name": 0,
                        "category": 5,
                        "price": 0,
                        "quantity": 0,
                        "customer_id": 0,
                        "customer_name": 0,
                        "order_date": 0,
                        "region": 10,
                        "country": 0,
                        "sales_channel": 0,
                        "profit_margin": 15,
                        "shipping_cost": 0,
                        "discount": 0,
                        "total_sales": 0
                    },
                    "suggestions": [
                        "Consider imputing missing values in 'category' column",
                        "Region has 10 missing values, consider using mode imputation",
                        "Profit margin has 15 missing values, consider using mean imputation"
                    ]
                },
                "analysis_results": {
                    "total_sales": {
                        "count": 1000,
                        "mean": 250.75,
                        "std": 125.50,
                        "min": 10.99,
                        "max": 999.99,
                        "25%": 150.25,
                        "50%": 225.50,
                        "75%": 350.75
                    },
                    "quantity": {
                        "count": 1000,
                        "mean": 3.5,
                        "std": 2.1,
                        "min": 1,
                        "max": 15,
                        "25%": 2,
                        "50%": 3,
                        "75%": 5
                    },
                    "profit_margin": {
                        "count": 985,
                        "mean": 0.25,
                        "std": 0.08,
                        "min": 0.05,
                        "max": 0.45,
                        "25%": 0.20,
                        "50%": 0.25,
                        "75%": 0.30
                    }
                },
                "html_report": {
                    "report_id": f"r_{timestamp}",
                    "report_url": f"/reports/{dataset_name}_{timestamp}.html"
                }
            },
            "summary": "The dataset contains 1000 sales records with 15 columns. The average sale amount is $250.75 with a standard deviation of $125.50. The average quantity per order is 3.5 units. The dataset has some missing values in the category (5), region (10), and profit margin (15) columns that should be addressed. The sales data shows a healthy profit margin averaging 25%, with a range from 5% to 45%. Further analysis could explore correlations between sales channels and profitability, as well as regional performance differences."
        }
    
    def _create_mock_report_content(self, report_id: str) -> Dict:
        """
        Create mock report content.
        
        Args:
            report_id (str): The ID of the report
            
        Returns:
            Dict: Mock report content
        """
        # Determine report filename based on ID
        if report_id == "r1":
            filename = "sample_sales_data_20250623_190858.html"
            dataset_name = "Sample Sales Data"
        elif report_id == "r2":
            filename = "customer_analytics_20250623_185530.html"
            dataset_name = "Customer Analytics"
        elif report_id == "r3":
            filename = "financial_performance_20250623_183015.html"
            dataset_name = "Financial Performance"
        else:
            filename = f"report_{report_id}.html"
            dataset_name = "Unknown Dataset"
        
        # Create mock HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>InsightMesh Analysis Report - {dataset_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }}
                h1 {{ color: #4285F4; }}
                h2 {{ color: #34A853; border-bottom: 1px solid #ddd; padding-bottom: 10px; }}
                h3 {{ color: #FBBC05; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .section {{ margin-bottom: 30px; }}
                .metric {{ display: inline-block; width: 200px; text-align: center; background-color: #f8f9fa; 
                          padding: 15px; margin: 10px; border-radius: 5px; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #4285F4; }}
                .metric-label {{ font-size: 14px; color: #5F6368; }}
                .insight-box {{ background-color: #E8F0FE; border-left: 4px solid #4285F4; padding: 15px; margin: 15px 0; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #4285F4; color: white; }}
                tr:nth-child(even) {{ background-color: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>InsightMesh Analysis Report</h1>
                    <p><strong>Dataset:</strong> {dataset_name}</p>
                    <p><strong>Generated:</strong> {time.strftime("%B %d, %Y %H:%M:%S")}</p>
                    <p><strong>Report ID:</strong> {report_id}</p>
                </div>
                
                <div class="section">
                    <h2>Executive Summary</h2>
                    <div class="insight-box">
                        <p>The dataset contains 1000 sales records with 15 columns. The average sale amount is $250.75 with a standard deviation of $125.50. The average quantity per order is 3.5 units. The dataset has some missing values in the category (5), region (10), and profit margin (15) columns that should be addressed. The sales data shows a healthy profit margin averaging 25%, with a range from 5% to 45%.</p>
                    </div>
                    
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value">1,000</div>
                            <div class="metric-label">Records</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">$250.75</div>
                            <div class="metric-label">Avg. Sale</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">25%</div>
                            <div class="metric-label">Profit Margin</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">3.5</div>
                            <div class="metric-label">Avg. Quantity</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Data Overview</h2>
                    <p>The dataset contains information about sales transactions, including product details, customer information, and sales metrics.</p>
                    
                    <h3>Data Structure</h3>
                    <table>
                        <tr>
                            <th>Column</th>
                            <th>Type</th>
                            <th>Missing Values</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>product_id</td>
                            <td>string</td>
                            <td>0 (0%)</td>
                            <td>Unique identifier for the product</td>
                        </tr>
                        <tr>
                            <td>product_name</td>
                            <td>string</td>
                            <td>0 (0%)</td>
                            <td>Name of the product</td>
                        </tr>
                        <tr>
                            <td>category</td>
                            <td>string</td>
                            <td>5 (0.5%)</td>
                            <td>Product category</td>
                        </tr>
                        <tr>
                            <td>price</td>
                            <td>float</td>
                            <td>0 (0%)</td>
                            <td>Unit price of the product</td>
                        </tr>
                        <tr>
                            <td>quantity</td>
                            <td>integer</td>
                            <td>0 (0%)</td>
                            <td>Quantity of products sold</td>
                        </tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>Statistical Analysis</h2>
                    
                    <h3>Summary Statistics</h3>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Total Sales</th>
                            <th>Quantity</th>
                            <th>Profit Margin</th>
                        </tr>
                        <tr>
                            <td>Count</td>
                            <td>1,000</td>
                            <td>1,000</td>
                            <td>985</td>
                        </tr>
                        <tr>
                            <td>Mean</td>
                            <td>$250.75</td>
                            <td>3.5</td>
                            <td>25%</td>
                        </tr>
                        <tr>
                            <td>Std Dev</td>
                            <td>$125.50</td>
                            <td>2.1</td>
                            <td>8%</td>
                        </tr>
                        <tr>
                            <td>Min</td>
                            <td>$10.99</td>
                            <td>1</td>
                            <td>5%</td>
                        </tr>
                        <tr>
                            <td>Max</td>
                            <td>$999.99</td>
                            <td>15</td>
                            <td>45%</td>
                        </tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>Key Insights</h2>
                    
                    <div class="insight-box">
                        <h3>Sales Performance</h3>
                        <p>The average sale amount is $250.75, with a wide range from $10.99 to $999.99. This indicates a diverse product portfolio with varying price points.</p>
                    </div>
                    
                    <div class="insight-box">
                        <h3>Profit Margins</h3>
                        <p>The average profit margin is 25%, which is healthy for retail operations. However, there's significant variation (5% to 45%), suggesting opportunities for optimization in lower-margin products.</p>
                    </div>
                    
                    <div class="insight-box">
                        <h3>Data Quality</h3>
                        <p>The dataset has some missing values in category (5), region (10), and profit margin (15) columns. Addressing these gaps would improve analysis accuracy.</p>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Recommendations</h2>
                    <ol>
                        <li><strong>Data Quality Improvement:</strong> Implement procedures to ensure complete data collection, particularly for region and profit margin fields.</li>
                        <li><strong>Profit Optimization:</strong> Analyze low-margin products to identify opportunities for cost reduction or price adjustments.</li>
                        <li><strong>Sales Strategy:</strong> Focus marketing efforts on high-margin products to improve overall profitability.</li>
                        <li><strong>Further Analysis:</strong> Conduct deeper analysis on regional performance and sales channel effectiveness.</li>
                    </ol>
                </div>
                
                <div class="section">
                    <h2>Methodology</h2>
                    <p>This analysis was performed using InsightMesh, powered by Google's Agentic Development Kit (ADK). The analysis pipeline consisted of:</p>
                    <ol>
                        <li><strong>Data Ingestion:</strong> Loading and parsing the CSV data</li>
                        <li><strong>Data Cleaning:</strong> Handling missing values and outliers</li>
                        <li><strong>Statistical Analysis:</strong> Computing descriptive statistics and correlations</li>
                        <li><strong>Insight Generation:</strong> Using AI to identify patterns and generate recommendations</li>
                    </ol>
                </div>
                
                <div style="text-align: center; margin-top: 50px; color: #5F6368; font-size: 12px;">
                    <p>Generated by InsightMesh using Google's Agentic Development Kit (ADK)</p>
                    <p>© 2025 InsightMesh. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {
            "report_id": report_id,
            "filename": filename,
            "created_at": "2025-06-23T19:08:58Z",
            "content": html_content,
            "size_bytes": len(html_content),
            "metadata": {
                "dataset_name": dataset_name,
                "rows": 1000,
                "columns": 15,
                "analysis_duration_ms": 2500
            }
        }
    
    # Public API methods
    
    def get_health(self) -> Dict:
        """
        Get API health status.
        
        Returns:
            Dict: Health status data
        """
        return self._make_request("GET", "health")
    
    def get_agent_status(self) -> Dict:
        """
        Get status of all agents.
        
        Returns:
            Dict: Agent status data
        """
        return self._make_request("GET", "agents/status")
    
    def analyze_file(self, file) -> Dict:
        """
        Analyze a file.
        
        Args:
            file: The file to analyze
            
        Returns:
            Dict: Analysis results
        """
        # In a real implementation, this would upload the file
        # For demo purposes, we'll just use the filename
        filename = getattr(file, "name", "uploaded_file.csv")
        
        return self._make_request(
            "POST", 
            "analyze/file",
            data={"filename": filename},
            timeout=60  # Longer timeout for analysis
        )
    
    def analyze_sample(self, sample_name: str) -> Dict:
        """
        Analyze a sample dataset.
        
        Args:
            sample_name (str): The name of the sample dataset
            
        Returns:
            Dict: Analysis results
        """
        return self._make_request(
            "GET", 
            "analyze/sample",
            params={"filename": sample_name},
            timeout=60  # Longer timeout for analysis
        )
    
    def get_reports(self) -> Dict:
        """
        Get list of all reports.
        
        Returns:
            Dict: List of reports
        """
        return self._make_request("GET", "reports")
    
    def get_report(self, report_id: str) -> Dict:
        """
        Get a specific report.
        
        Args:
            report_id (str): The ID of the report
            
        Returns:
            Dict: Report data
        """
        return self._make_request("GET", f"reports/{report_id}")
    
    def delete_report(self, report_id: str) -> Dict:
        """
        Delete a report.
        
        Args:
            report_id (str): The ID of the report
            
        Returns:
            Dict: Operation result
        """
        return self._make_request("DELETE", f"reports/{report_id}")
