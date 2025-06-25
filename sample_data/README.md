# Sample Datasets for InsightMesh

This directory contains sample datasets for demonstrating the capabilities of the InsightMesh data analysis platform.

## Available Datasets

### 1. Sample Sales Data (`sample_sales_data.csv`)
- **Description**: Retail sales transactions with product, customer, and location information.
- **Columns**: 15
- **Rows**: 1000
- **Use Case**: Sales performance analysis, customer segmentation, product profitability.

### 2. Customer Analytics (`customer_analytics.csv`)
- **Description**: Customer behavior and demographic data with engagement metrics.
- **Columns**: 20
- **Rows**: 50
- **Use Case**: Customer segmentation, behavior analysis, lifetime value prediction.

### 3. Financial Performance (`financial_performance.csv`)
- **Description**: Daily financial metrics by department, region, and product line.
- **Columns**: 21
- **Rows**: 59
- **Use Case**: Financial analysis, profitability assessment, trend identification.

### 4. Marketing Campaigns (`marketing_campaigns.csv`)
- **Description**: Campaign performance metrics across different channels and audiences.
- **Columns**: 25
- **Rows**: 50
- **Use Case**: Marketing ROI analysis, channel effectiveness, audience targeting.

### 5. Employee Satisfaction (`employee_satisfaction.csv`)
- **Description**: HR survey results with employee satisfaction scores across various dimensions.
- **Columns**: 40
- **Rows**: 50
- **Use Case**: HR analytics, employee satisfaction analysis, retention risk assessment.

### 6. Product Inventory (`product_inventory.csv`)
- **Description**: Product catalog with inventory levels, pricing, and supplier information.
- **Columns**: 45
- **Rows**: 50
- **Use Case**: Inventory management, pricing optimization, supplier analysis.

### 7. Website Traffic (`website_traffic.csv`)
- **Description**: Web analytics data with page views, conversion rates, and user behavior.
- **Columns**: 35
- **Rows**: 70
- **Use Case**: Web performance analysis, user journey optimization, conversion funnel analysis.

## Using the Datasets

These datasets can be used with the InsightMesh platform in two ways:

1. **Through the Frontend**: Select a sample dataset from the Dashboard page.
2. **Through the API**: Use the `/analyze/sample` endpoint with the filename parameter.

Example API call:
```bash
curl -X GET "http://localhost:8000/analyze/sample?filename=sample_sales_data.csv"
```

## Dataset Structure

Each dataset is structured as a CSV file with headers in the first row. The datasets are designed to showcase different types of data and analysis scenarios.

## Adding New Datasets

To add a new sample dataset:

1. Place the CSV file in this directory
2. Update the `create_sample_datasets_info()` function in `frontend/utils/data_processing.py`
3. Restart the application

## License

These sample datasets are synthetic and created for demonstration purposes only. They do not contain real customer or business data.
