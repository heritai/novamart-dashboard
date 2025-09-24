#!/bin/bash

# NovaMart Dashboard Startup Script
echo "🏪 Starting NovaMart Demand Forecasting Dashboard..."
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project directory."
    exit 1
fi

# Check if sample data exists
if [ ! -f "sample_data/sales_data.csv" ]; then
    echo "❌ Error: Sales data not found. Please ensure sample_data/sales_data.csv exists."
    exit 1
fi

echo "✅ All files found. Starting dashboard..."
echo ""
echo "🌐 The dashboard will be available at: http://localhost:8501"
echo "📊 Press Ctrl+C to stop the server"
echo ""

# Run the Streamlit app
python -m streamlit run app.py
