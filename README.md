# NovaMart: AI-Powered Demand Forecasting & Stock Optimization Dashboard

Transforming retail inventory management with AI-driven forecasting and optimization. A comprehensive consulting demo project by HerixAI.

---

## 🏪 Business Context

NovaMart, a mid-size online retailer specializing in groceries and household products, faces a pervasive retail challenge: optimizing inventory. The persistent dilemma of balancing costly stockouts against expensive overstocking directly impacts profitability and customer satisfaction.

### The Challenge
-   **Lost Sales**: Frequent stockouts, particularly during peak demand, lead to missed revenue opportunities.
-   **Tied Capital**: Excessive overstocking, especially in off-peak seasons, results in inefficient capital allocation and increased holding costs.
-   **Operational Inefficiency**: Manual inventory management often lacks data-driven insights, leading to suboptimal operations.
-   **Missed Opportunities**: Inadequate consideration of complex seasonal demand patterns hinders strategic planning.

### The Solution
This dashboard delivers a robust, data-driven solution, leveraging advanced machine learning to provide a comprehensive demand forecasting and stock optimization system:
-   **Precise Demand Forecasting**: Utilizes Prophet and ARIMA models for highly accurate, data-driven predictions.
-   **Intelligent Stock Optimization**: Dynamically calculates optimal reorder points and safety stock levels to minimize risk.
-   **Actionable Insights**: Offers intuitive, interactive visualizations for clear and immediate business understanding.
-   **Strategic Reporting**: Generates automated, executive-ready reports to facilitate informed decision-making.

---

## 🚀 Dashboard Features

### 📊 Global Summary
-   **Key Performance Indicators (KPIs)**: Displays total sales, growth rates, and top-performing products.
-   **Demand Trend Analysis**: Visualizes historical patterns, growth trajectories, and future projections.
-   **Product Performance Overview**: Analyzes sales distribution and comparative product performance.
-   **Seasonality Insights**: Utilizes heatmaps to reveal demand patterns by month, day, and time-of-day.

### 🔍 Product Explorer
-   **Individual Product Deep Dive**: Offers granular analysis of specific product performance.
-   **Performance Metrics**: Displays key indicators like growth rates, demand stability, and recent sales trends.
-   **Trend Analysis**: Visualizes moving averages and volatility metrics for a deeper understanding of product dynamics.

### 📈 Advanced Forecasting
-   **Dual-Model Approach**: Leverages Prophet (primary) and ARIMA (baseline) models for robust predictions.
-   **Interactive Forecasts**: Provides adjustable prediction horizons (7-90 days) with clear confidence intervals.
-   **Model Performance Metrics**: Displays key accuracy metrics (MAPE, RMSE) for transparent assessment.
-   **30-Day Operational Forecast**: Offers detailed predictions optimized for immediate operational planning.

### 📦 Stock Optimization
-   **Dynamic Reorder Points**: Intelligently calculated based on lead time and forecasted demand.
-   **Adaptive Safety Stock**: Statistically optimized and aligned with target service levels, preventing stockouts.
-   **Economic Order Quantity (EOQ)**: Offers cost-optimized recommendations for order sizes.
-   **Comprehensive Inventory Metrics**: Monitors turnover rates, stockout probabilities, and coverage analysis.

### 📊 Comprehensive Reporting
-   **PDF Report Generation**: Creates executive summaries, complete with charts and actionable recommendations.
-   **Data Export**: Enables seamless CSV downloads for external analysis and integration.
-   **Actionable Business Insights**: Provides clear recommendations for continuous inventory optimization strategies.

---

## 🎯 Live Demo

🚀 **Dive into the Live Demo!**

[**Launch the NovaMart Dashboard on Streamlit Cloud**](https://novamart-forecasting.streamlit.app)

*Discover the full power of interactive forecasting, dynamic stock optimization, and comprehensive reporting with real-time insights.*

## 🚀 Quick Deployment

**Launch Your Own NovaMart Instance in Minutes!**

Get your personalized NovaMart dashboard up and running on Streamlit Cloud with these simple steps:

1.  **Fork this repository** on GitHub.
2.  Navigate to [share.streamlit.io](https://share.streamlit.io).
3.  **Connect your GitHub account** if prompted.
4.  **Select this repository** and click "Deploy."
5.  Your customized dashboard will be live at a unique URL (e.g., `https://your-app-name.streamlit.app`).

📖 For a comprehensive, step-by-step walkthrough, refer to our [**Detailed Deployment Guide**](DEPLOYMENT.md).

---

## 📸 Screenshots

### Global Business Overview
![Global Business Overview](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Global+Business+Overview%3A+Key+Performance+Insights)

### Product Forecasting
![Product Forecasting](https://via.placeholder.com/800x400/ff7f0e/ffffff?text=Advanced+Forecasting%3A+Predictive+Analytics)

### Stock Optimization
![Stock Optimization](https://via.placeholder.com/800x400/2ca02c/ffffff?text=Intelligent+Stock+Optimization%3A+Reorder+%26+Safety+Stock)

### Interactive Reports
![Interactive Reports](https://via.placeholder.com/800x400/d62728/ffffff?text=Comprehensive+Reporting%3A+Actionable+PDFs)

---

## 🎯 Key Benefits

### **For Business Operations**
-   **Significant Reduction in Stockouts**: Achieve a **20-25% reduction** in stockout incidents.
-   **Optimized Inventory Costs**: Realize a substantial **10-15% reduction** in inventory holding costs.
-   **Enhanced Cash Flow**: Improve cash flow by **5-10%** through more strategic and efficient ordering.
-   **Boosted Customer Satisfaction**: Drive a significant **15-20% improvement** in product availability and fulfillment rates.

### **For Decision Making**
-   **Empowered Decision-Making**: Move beyond intuition with robust, data-driven statistical analysis.
-   **Proactive Strategic Planning**: Forecast demand **30-90 days** into the future, enabling forward-looking strategies.
-   **Intelligent Risk Management**: Quantify, understand, and mitigate potential inventory risks effectively.
-   **Continuous Performance Monitoring**: Accurately track forecast accuracy and other critical inventory metrics.

---

## ⚠️ Important Disclaimers: Demo Scope & Considerations

### **Data and Methodology**
-   **Synthetic Data**: All sales data presented is artificially generated, meticulously designed to emulate realistic retail patterns for demonstration purposes.
-   **Demo Scope & Model Simplifications**: While powerful for demonstration, a full production implementation typically integrates more sophisticated features, such as:
    -   Multi-product optimization with cross-correlations and dependencies.
    -   Advanced supplier lead time variability modeling.
    -   Comprehensive cost trade-off optimization (holding, ordering, and stockout costs).
    -   Deep learning models (e.g., LSTM, Transformer) for more complex pattern recognition.
    -   Real-time demand sensing, anomaly detection, and adaptive model adjustments.
    -   Robust MLOps pipeline for continuous model retraining and deployment.

### **Business Context**
-   **Consulting Demonstration**: This project serves as a comprehensive demonstration of HerixAI's capabilities in advanced retail analytics solutions.
-   **Production Implementations**: A full-scale consulting engagement with HerixAI typically entails:
    -   Custom model development tailored to specific business needs and data characteristics.
    -   Seamless integration with existing ERP/WMS systems and data infrastructure.
    -   Comprehensive change management and user training programs.
    -   Ongoing model maintenance, performance monitoring, and continuous improvement.

---

## 🛠️ Developer & Contribution Guide

### **Quick Start**

1.  **Prerequisites**: Ensure you have Python 3.10 or higher installed.

2.  **Clone the repository**
    ```bash
    git clone https://github.com/herixai/novamart-forecasting-dashboard.git
    cd novamart-forecasting-dashboard
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application**
    ```bash
    streamlit run app.py
    ```

5.  **Access the dashboard**
    Open your web browser to `http://localhost:8501`.

### **System Requirements**
-   **Python**: 3.10 or higher (recommended 3.11+)
-   **Memory**: 4GB RAM minimum (8GB recommended for optimal performance)
-   **Storage**: Approximately 500MB for data and dependencies

### **Project Structure**
```
novamart-forecasting-dashboard/
├── app.py                    # Main Streamlit application entry point
├── requirements.txt          # Python dependencies for the project
├── README.md                # This file you're reading!
├── utils/                   # Module containing helper functions and logic
│   ├── data_prep.py         # Data loading, cleaning, and feature engineering
│   ├── forecasting.py       # Prophet and ARIMA model implementation
│   ├── stock_opt.py         # Stock optimization algorithms and calculations
│   └── report_generator.py  # Logic for generating PDF reports
├── sample_data/             # Contains synthetic sales data
│   └── sales_data.csv       # 2 years of daily sales data for demonstration
└── reports/                 # Stores generated PDF reports
    └── example_report.pdf   # A sample generated PDF report
```

### **Key Dependencies**
-   **Streamlit**: The framework for building the interactive web application.
-   **Prophet**: Facebook's powerful time-series forecasting library, ideal for data with strong seasonal effects.
-   **Statsmodels**: Comprehensive library for statistical modeling, including ARIMA and other econometric models.
-   **Plotly**: For rich, interactive data visualizations that enhance user engagement.
-   **Pandas/NumPy**: Essential for efficient data manipulation and numerical operations.
-   **Matplotlib/Seaborn**: For generating high-quality static plots, particularly for PDF reports.

### **Customization Options**
-   **Forecast Horizons**: Adjust prediction periods from 7 to 90 days.
-   **Service Level Targets**: Configure desired service levels from 85% to 99% for safety stock calculations.
-   **Safety Stock Methodologies**: Select between percentage-based or statistical safety stock calculation methods.
-   **Model Parameters**: Fine-tune Prophet seasonality components and ARIMA model orders.
-   **Report Customization**: Define report sections, metrics, and visual elements to customize output.

---

## 🤝 Contact & Support

**HerixAI Consulting**

For inquiries, support, or to explore how HerixAI can transform your business with advanced analytics, please reach out:
-   **Email**: info@herixai.com
-   **Website**: [www.herixai.com](https://www.herixai.com)
-   **LinkedIn**: [HerixAI Consulting](https://linkedin.com/company/herixai)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Developed with ❤️ by the HerixAI team to showcase advanced analytics capabilities for retail inventory management.*