import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import os

def generate_html_report(analysis_data: Dict[str, Any], filename: str) -> str:
    """
    Generate a beautiful HTML report from analysis data
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_id = f"{filename.replace('.csv', '')}_{timestamp}"
    
    # Extract data from analysis results
    insights = analysis_data.get("insights", {})
    summary = analysis_data.get("summary", "")
    processing_steps = analysis_data.get("processing_steps", [])
    
    data_info = insights.get("data_info", {})
    cleaning_info = insights.get("cleaning_info", {})
    analysis_results = insights.get("analysis_results", {})
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InsightMesh Analysis Report - {filename}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 40px;
            padding: 25px;
            border-radius: 10px;
            background: #f8f9fa;
            border-left: 5px solid #4285f4;
        }}
        
        .section h2 {{
            color: #4285f4;
            margin-bottom: 20px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
        }}
        
        .section h2::before {{
            content: '';
            width: 8px;
            height: 8px;
            background: #4285f4;
            border-radius: 50%;
            margin-right: 15px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            border-top: 3px solid #34a853;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #34a853;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin: 20px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        
        th {{
            background: #4285f4;
            color: white;
            font-weight: 600;
        }}
        
        tr:hover {{
            background: #f5f5f5;
        }}
        
        .status-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .status-completed {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .summary-box {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            border-left: 5px solid #34a853;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        
        .summary-box h3 {{
            color: #34a853;
            margin-bottom: 15px;
        }}
        
        .summary-text {{
            line-height: 1.8;
            color: #555;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
        }}
        
        .timestamp {{
            font-size: 0.9em;
            color: #888;
            margin-top: 10px;
        }}
        
        .json-container {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            margin: 15px 0;
        }}
        
        .highlight {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
                border-radius: 10px;
            }}
            
            .header {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 InsightMesh Analysis Report</h1>
            <div class="subtitle">Powered by Google Agentic ADK Framework</div>
            <div class="timestamp">Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</div>
        </div>
        
        <div class="content">
            <!-- Executive Summary -->
            <div class="section">
                <h2>📊 Executive Summary</h2>
                <div class="summary-box">
                    <h3>Key Insights</h3>
                    <div class="summary-text">
                        {format_summary_text(summary)}
                    </div>
                </div>
            </div>
            
            <!-- Data Overview -->
            <div class="section">
                <h2>📋 Data Overview</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{data_info.get('rows', 'N/A')}</div>
                        <div class="stat-label">Total Rows</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{data_info.get('columns', 'N/A')}</div>
                        <div class="stat-label">Total Columns</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len(data_info.get('column_names', []))}</div>
                        <div class="stat-label">Data Fields</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len([s for s in processing_steps if s.get('status') == 'completed'])}</div>
                        <div class="stat-label">Completed Steps</div>
                    </div>
                </div>
                
                <div class="highlight">
                    <strong>File:</strong> {filename}<br>
                    <strong>Columns:</strong> {', '.join(data_info.get('column_names', []))}
                </div>
            </div>
            
            <!-- Processing Pipeline -->
            <div class="section">
                <h2>⚙️ Processing Pipeline</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Step</th>
                                <th>Agent</th>
                                <th>Description</th>
                                <th>Status</th>
                                <th>Key Output</th>
                            </tr>
                        </thead>
                        <tbody>
                            {generate_processing_table(processing_steps)}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Data Quality -->
            <div class="section">
                <h2>🧹 Data Quality Analysis</h2>
                {generate_cleaning_section(cleaning_info)}
            </div>
            
            <!-- Statistical Analysis -->
            <div class="section">
                <h2>📈 Statistical Analysis</h2>
                {generate_statistics_section(analysis_results)}
            </div>
            
            <!-- Raw Data Preview -->
            <div class="section">
                <h2>🔍 Technical Details</h2>
                <details>
                    <summary style="cursor: pointer; padding: 10px; background: #e9ecef; border-radius: 5px; margin-bottom: 15px;">
                        <strong>View Raw Analysis Data (JSON)</strong>
                    </summary>
                    <div class="json-container">
                        <pre>{json.dumps(insights, indent=2)}</pre>
                    </div>
                </details>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>InsightMesh</strong> - AI-Powered Data Analysis Platform</p>
            <p>Report ID: {report_id}</p>
            <div class="timestamp">Powered by Google Agentic ADK Framework</div>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content, report_id

def format_summary_text(summary: str) -> str:
    """Format the summary text with proper HTML formatting"""
    if not summary:
        return "<p>No summary available.</p>"
    
    # Convert markdown-style formatting to HTML
    formatted = summary.replace('\n\n', '</p><p>')
    formatted = formatted.replace('\n', '<br>')
    formatted = formatted.replace('**', '<strong>').replace('**', '</strong>')
    formatted = formatted.replace('*', '<em>').replace('*', '</em>')
    
    return f"<p>{formatted}</p>"

def generate_processing_table(processing_steps: List[Dict]) -> str:
    """Generate HTML table rows for processing steps"""
    rows = []
    for step in processing_steps:
        status_class = "status-completed" if step.get('status') == 'completed' else "status-failed"
        
        # Extract key output info
        output = step.get('output', {})
        key_output = "No output"
        
        if step.get('step') == 'ingestor':
            key_output = f"{output.get('num_rows', 0)} rows loaded"
        elif step.get('step') == 'cleaner':
            suggestions = len(output.get('suggestions', []))
            key_output = f"{suggestions} cleaning suggestions"
        elif step.get('step') == 'analyzer':
            key_output = "Statistical analysis completed"
        elif step.get('step') == 'summarizer':
            summary_len = len(output.get('summary_text', ''))
            key_output = f"Summary generated ({summary_len} chars)"
        
        rows.append(f"""
            <tr>
                <td><strong>{step.get('step', '').title()}</strong></td>
                <td>{step.get('agent', 'Unknown')}</td>
                <td>{step.get('description', 'No description')}</td>
                <td><span class="status-badge {status_class}">{step.get('status', 'Unknown')}</span></td>
                <td>{key_output}</td>
            </tr>
        """)
    
    return ''.join(rows)

def generate_cleaning_section(cleaning_info: Dict) -> str:
    """Generate HTML for data cleaning section"""
    null_summary = cleaning_info.get('null_summary', {})
    suggestions = cleaning_info.get('suggestions', [])
    
    if not null_summary:
        return "<p>No cleaning analysis available.</p>"
    
    # Create null values table
    null_table = "<table><thead><tr><th>Column</th><th>Missing Values</th></tr></thead><tbody>"
    for col, count in null_summary.items():
        null_table += f"<tr><td>{col}</td><td>{count}</td></tr>"
    null_table += "</tbody></table>"
    
    suggestions_html = ""
    if suggestions:
        suggestions_html = "<h4>Cleaning Suggestions:</h4><ul>"
        for suggestion in suggestions:
            suggestions_html += f"<li>{suggestion}</li>"
        suggestions_html += "</ul>"
    else:
        suggestions_html = "<div class='highlight'>✅ <strong>Great!</strong> No data quality issues found.</div>"
    
    return f"""
        <h3>Missing Values Analysis</h3>
        <div class="table-container">{null_table}</div>
        {suggestions_html}
    """

def generate_statistics_section(analysis_results: Dict) -> str:
    """Generate HTML for statistical analysis section"""
    if not analysis_results:
        return "<p>No statistical analysis available.</p>"
    
    html = ""
    
    for column, stats in analysis_results.items():
        if not stats or not isinstance(stats, dict):
            continue
            
        html += f"<h3>📊 {column}</h3>"
        
        # Create stats table
        html += "<div class='table-container'><table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>"
        
        for metric, value in stats.items():
            if value is not None:
                if isinstance(value, float):
                    value = f"{value:.2f}"
                html += f"<tr><td>{metric.title()}</td><td>{value}</td></tr>"
        
        html += "</tbody></table></div>"
    
    return html

def save_html_report(html_content: str, report_id: str) -> str:
    """Save HTML report to output directory"""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, f"{report_id}.html")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return file_path
