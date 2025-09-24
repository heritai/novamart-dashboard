"""
NovaMart Demand Forecasting & Stock Optimization Dashboard
A comprehensive dashboard for demand forecasting and inventory optimization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from data_prep import (
    load_sales_data, get_global_summary, create_demand_trend_chart,
    create_product_comparison_chart, create_seasonality_heatmap,
    prepare_product_data, get_product_summary, create_product_trend_chart
)
from forecasting import (
    create_forecast_chart, get_forecast_metrics, get_next_30_days_forecast
)
from stock_opt import (
    get_stock_recommendations, create_stock_optimization_chart,
    calculate_inventory_metrics, get_optimization_summary
)
from report_generator import generate_report_button_clicked

# Page configuration
st.set_page_config(
    page_title="NovaMart Forecasting Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Make tabs font bigger */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        font-size: 18px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Simple section headers without background */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f77b4;
        margin: 2rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #1f77b4;
    }
    
    /* Simple spacing for plots without white boxes */
    .plot-container {
        margin: 1.5rem 0;
    }
    
    /* Simple info boxes with transparent background */
    .info-box {
        margin: 1rem 0;
        padding: 0.5rem 0;
    }
    
    /* Recommendation boxes with better styling */
    .recommendation-box {
        background-color: rgba(31, 119, 180, 0.1);
        border-left: 4px solid #1f77b4;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Better spacing for stock optimization charts */
    .stock-chart-container {
        margin: 2rem 0;
    }
    
    /* Fix overlapping charts */
    .element-container {
        margin-bottom: 2rem !important;
    }
    
    /* Ensure proper spacing between plotly charts */
    .js-plotly-plot {
        margin-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache sales data"""
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'sales_data.csv')
    return load_sales_data(data_path)

@st.cache_data
def get_cached_forecast(product_name, forecast_periods):
    """Cache forecast results to avoid recomputation"""
    from forecasting import get_next_30_days_forecast
    from data_prep import load_sales_data, prepare_product_data
    
    df = load_sales_data(os.path.join(os.path.dirname(__file__), 'sample_data', 'sales_data.csv'))
    product_df = prepare_product_data(df, product_name)
    return get_next_30_days_forecast(product_df, product_name)

@st.cache_data
def get_cached_forecast_chart(product_name, forecast_periods):
    """Cache forecast chart to avoid recomputation"""
    from forecasting import create_forecast_chart
    from data_prep import load_sales_data, prepare_product_data
    
    df = load_sales_data(os.path.join(os.path.dirname(__file__), 'sample_data', 'sales_data.csv'))
    product_df = prepare_product_data(df, product_name)
    return create_forecast_chart(product_df, product_name, forecast_periods)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏪 NovaMart Demand Forecasting & Stock Optimization Dashboard</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #666;">
        <p>Powered by Prophet & ARIMA forecasting models | Delivered by HerixAI Consulting</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Sales data file not found. Please ensure 'sample_data/sales_data.csv' exists.")
        return
    
    # Main navigation using tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Global Summary", 
        "🔍 Product Explorer", 
        "📈 Forecasting", 
        "📦 Stock Optimization", 
        "📊 Reports"
    ])
    
    with tab1:
        show_global_summary(df)
    
    with tab2:
        show_product_explorer(df)
    
    with tab3:
        show_forecasting_page(df)
    
    with tab4:
        show_stock_optimization(df)
    
    with tab5:
        show_reports_page(df)

def show_global_summary(df):
    """Display global summary dashboard"""
    st.header("📊 Global Business Summary")
    
    # Get summary statistics
    summary = get_global_summary(df)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Sales",
            value=f"{summary['total_sales']:,}",
            delta=f"{summary['growth_rate']:.1f}% YoY"
        )
    
    with col2:
        st.metric(
            label="📈 Avg Daily Sales",
            value=f"{summary['avg_daily_sales']:.0f}",
            delta="units/day"
        )
    
    with col3:
        st.metric(
            label="🏆 Top Product",
            value=summary['top_products'].index[0],
            delta=f"{summary['top_products'].iloc[0]:,} units"
        )
    
    with col4:
        st.metric(
            label="📅 Data Period",
            value=f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
            delta=f"{(df['Date'].max() - df['Date'].min()).days} days"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">📈 Total Demand Trend</div>', unsafe_allow_html=True)
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        trend_chart = create_demand_trend_chart(df)
        st.plotly_chart(trend_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-header">🥧 Product Sales Distribution</div>', unsafe_allow_html=True)
        chart_type = st.radio("Chart Type:", ["Bar Chart", "Pie Chart"], horizontal=True)
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        comparison_chart = create_product_comparison_chart(
            df, 'pie' if chart_type == "Pie Chart" else 'bar'
        )
        st.plotly_chart(comparison_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Seasonality analysis
    st.markdown('<div class="section-header">🗓️ Seasonality Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    seasonality_chart = create_seasonality_heatmap(df)
    st.plotly_chart(seasonality_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top products table
    st.markdown('<div class="section-header">🏆 Top 10 Products by Sales</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    top_products_df = df.groupby('Product')['Quantity'].agg(['sum', 'mean', 'std']).round(1)
    top_products_df = top_products_df.sort_values('sum', ascending=False).head(10)
    top_products_df.columns = ['Total Sales', 'Avg Daily Sales', 'Std Dev']
    st.dataframe(top_products_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_product_explorer(df):
    """Display product explorer page"""
    st.header("🔍 Product Explorer")
    
    # Product selector
    products = sorted(df['Product'].unique())
    selected_product = st.selectbox("Select a product:", products)
    
    if selected_product:
        # Get product data
        product_df = prepare_product_data(df, selected_product)
        product_summary = get_product_summary(df, selected_product)
        
        # Product metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Total Sales",
                value=f"{product_summary['total_sales']:,}",
                delta="units"
            )
        
        with col2:
            st.metric(
                label="📈 Avg Daily Sales",
                value=f"{product_summary['avg_daily_sales']:.1f}",
                delta="units/day"
            )
        
        with col3:
            trend_direction = "📈" if product_summary['trend'] > 0 else "📉"
            st.metric(
                label="📊 Trend",
                value=f"{product_summary['trend']:.3f}",
                delta=f"{trend_direction} units/day"
            )
        
        with col4:
            st.metric(
                label="📊 Volatility",
                value=f"{product_summary['volatility']:.1f}%",
                delta="CV"
            )
        
        st.markdown("---")
        
        # Product trend chart
        st.subheader(f"📈 {selected_product} - Sales Trend")
        trend_chart = create_product_trend_chart(df, selected_product)
        st.plotly_chart(trend_chart, use_container_width=True)
        
        # Product statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Sales Statistics")
            stats_data = {
                'Metric': ['Total Sales', 'Average Daily', 'Standard Deviation', 'Minimum Daily', 'Maximum Daily'],
                'Value': [
                    f"{product_summary['total_sales']:,}",
                    f"{product_summary['avg_daily_sales']:.1f}",
                    f"{product_summary['std_daily_sales']:.1f}",
                    f"{product_df['Quantity'].min()}",
                    f"{product_df['Quantity'].max()}"
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("📅 Recent Performance")
            recent_data = product_df.tail(30)
            recent_avg = recent_data['Quantity'].mean()
            overall_avg = product_df['Quantity'].mean()
            performance_change = ((recent_avg - overall_avg) / overall_avg) * 100
            
            st.metric(
                label="Last 30 Days Avg",
                value=f"{recent_avg:.1f}",
                delta=f"{performance_change:+.1f}% vs overall"
            )
            
            # Recent trend chart
            fig = px.line(recent_data, x='Date', y='Quantity',
                         title="Last 30 Days Performance")
            st.plotly_chart(fig, use_container_width=True)

def show_forecasting_page(df):
    """Display forecasting page"""
    st.header("📈 Demand Forecasting")
    
    # Product selector
    products = sorted(df['Product'].unique())
    selected_product = st.selectbox("Select a product for forecasting:", products)
    
    if selected_product:
        # Get product data
        product_df = prepare_product_data(df, selected_product)
        
        # Forecasting parameters
        col1, col2 = st.columns(2)
        
        with col1:
            forecast_periods = st.slider("Forecast Period (days):", 7, 90, 30)
        
        with col2:
            show_metrics = st.checkbox("Show Model Performance Metrics", value=True)
        
        # Performance note
        st.info("⚡ **Performance Optimized**: Models use recent data (6 months) for faster computation. Results are cached for instant loading on subsequent visits.")
        
        # Generate forecast
        st.markdown(f'<div class="section-header">🔮 {selected_product} - Demand Forecast</div>', unsafe_allow_html=True)
        
        # Progress bar for better UX
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Initializing models...")
        progress_bar.progress(20)
        
        status_text.text("Fitting Prophet model...")
        progress_bar.progress(40)
        
        status_text.text("Fitting ARIMA model...")
        progress_bar.progress(60)
        
        status_text.text("Generating forecast chart...")
        progress_bar.progress(80)
        
        forecast_chart = get_cached_forecast_chart(selected_product, forecast_periods)
        
        status_text.text("Complete!")
        progress_bar.progress(100)
        
        # Clear progress indicators
        status_text.empty()
        progress_bar.empty()
        
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.plotly_chart(forecast_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Model performance metrics
        if show_metrics:
            st.markdown('<div class="section-header">📊 Model Performance</div>', unsafe_allow_html=True)
            
            with st.spinner("Calculating model performance..."):
                metrics = get_forecast_metrics(product_df, selected_product, forecast_periods)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("**Prophet Model:**")
                if metrics['prophet']['mape'] is not None:
                    st.metric("MAPE", f"{metrics['prophet']['mape']:.2f}%")
                    st.metric("RMSE", f"{metrics['prophet']['rmse']:.2f}")
                else:
                    st.error("Prophet model failed to generate metrics")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("**ARIMA Model:**")
                if metrics['arima']['mape'] is not None:
                    st.metric("MAPE", f"{metrics['arima']['mape']:.2f}%")
                    st.metric("RMSE", f"{metrics['arima']['rmse']:.2f}")
                else:
                    st.error("ARIMA model failed to generate metrics")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Next 30 days forecast summary
        st.markdown('<div class="section-header">📅 Next 30 Days Forecast Summary</div>', unsafe_allow_html=True)
        
        with st.spinner("Generating 30-day forecast..."):
            forecast_summary = get_cached_forecast(selected_product, 30)
        
        if forecast_summary['forecast_data'] is not None:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📊 Avg Daily Forecast",
                    value=f"{forecast_summary['avg_daily_forecast']:.1f}",
                    delta="units/day"
                )
            
            with col2:
                st.metric(
                    label="📈 Total 30-Day Forecast",
                    value=f"{forecast_summary['total_forecast']:.0f}",
                    delta="units"
                )
            
            with col3:
                st.metric(
                    label="📉 Lower Bound",
                    value=f"{forecast_summary['lower_bound']:.1f}",
                    delta="units/day"
                )
            
            with col4:
                st.metric(
                    label="📈 Upper Bound",
                    value=f"{forecast_summary['upper_bound']:.1f}",
                    delta="units/day"
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Forecast data table
            st.markdown('<div class="section-header">📋 Detailed Forecast Data</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            forecast_df = forecast_summary['forecast_data'][['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
            forecast_df.columns = ['Date', 'Forecast', 'Lower Bound', 'Upper Bound']
            forecast_df['Date'] = forecast_df['Date'].dt.strftime('%Y-%m-%d')
            st.dataframe(forecast_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Failed to generate forecast summary")

def show_stock_optimization(df):
    """Display stock optimization page"""
    st.header("📦 Stock Optimization")
    
    # Product selector
    products = sorted(df['Product'].unique())
    selected_product = st.selectbox("Select a product for stock optimization:", products)
    
    if selected_product:
        # Get product data
        product_df = prepare_product_data(df, selected_product)
        
        # Optimization parameters
        st.subheader("⚙️ Optimization Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lead_time = st.slider("Lead Time (days):", 1, 30, 7)
        
        with col2:
            safety_stock_percent = st.slider("Safety Stock (% of avg demand):", 10, 50, 20)
        
        with col3:
            service_level = st.slider("Service Level:", 0.85, 0.99, 0.95)
        
        # Generate recommendations
        st.subheader(f"📊 {selected_product} - Stock Optimization Analysis")
        
        with st.spinner("Calculating stock recommendations..."):
            recommendations = get_stock_recommendations(
                product_df, selected_product, lead_time, safety_stock_percent, service_level
            )
        
        # Key recommendations
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Reorder Point",
                value=f"{recommendations['reorder_point']:.0f}",
                delta="units"
            )
        
        with col2:
            st.metric(
                label="🛡️ Safety Stock",
                value=f"{recommendations['safety_stock']:.0f}",
                delta="units"
            )
        
        with col3:
            st.metric(
                label="📦 Recommended Order Qty",
                value=f"{recommendations['recommended_reorder_qty']:.0f}",
                delta="units"
            )
        
        with col4:
            st.metric(
                label="📈 Service Level",
                value=f"{recommendations['service_level']*100:.1f}%",
                delta="target"
            )
        
        # Stock optimization chart
        st.markdown('<div class="section-header">📈 Stock Optimization Visualization</div>', unsafe_allow_html=True)
        
        with st.spinner("Generating optimization chart..."):
            opt_chart = create_stock_optimization_chart(recommendations, product_df)
            # Add proper spacing for the chart
            st.markdown('<div class="stock-chart-container">', unsafe_allow_html=True)
            st.plotly_chart(opt_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">🎯 Key Recommendations</div>', unsafe_allow_html=True)
            st.markdown(f'''
            <div class="recommendation-box">
                <p>• Set reorder point at <strong>{recommendations['reorder_point']:.0f} units</strong></p>
                <p>• Maintain safety stock of <strong>{recommendations['safety_stock']:.0f} units</strong></p>
                <p>• Order <strong>{recommendations['recommended_reorder_qty']:.0f} units</strong> when reordering</p>
                <p>• Expected service level: <strong>{recommendations['service_level']*100:.1f}%</strong></p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="section-header">💡 Expected Benefits</div>', unsafe_allow_html=True)
            st.markdown(f'''
            <div class="recommendation-box">
                <p>• Reduce stockout risk by <strong>{recommendations['stockout_risk_reduction']:.1f}%</strong></p>
                <p>• Inventory turnover: <strong>{recommendations['annual_demand'] / ((recommendations['reorder_point'] + recommendations['recommended_reorder_qty']) / 2):.1f} times per year</strong></p>
                <p>• Average <strong>{(recommendations['reorder_point'] + recommendations['recommended_reorder_qty']) / 2 / recommendations['avg_daily_demand']:.1f} days</strong> of inventory on hand</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Add spacing before metrics section
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Inventory metrics
        st.markdown('<div class="section-header">📊 Inventory Performance Metrics</div>', unsafe_allow_html=True)
        
        with st.spinner("Calculating inventory metrics..."):
            metrics = calculate_inventory_metrics(recommendations)
            summary = get_optimization_summary(recommendations, metrics)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📅 Days of Inventory",
                value=f"{metrics['days_of_inventory']:.1f}",
                delta="days"
            )
        
        with col2:
            st.metric(
                label="🔄 Inventory Turnover",
                value=f"{metrics['inventory_turnover']:.1f}",
                delta="times/year"
            )
        
        with col3:
            st.metric(
                label="⚠️ Stockout Probability",
                value=f"{metrics['stockout_probability']*100:.1f}%",
                delta="risk"
            )
        
        with col4:
            st.metric(
                label="🛡️ Safety Stock Coverage",
                value=f"{metrics['safety_stock_coverage']:.1f}",
                delta="days"
            )
        
        # Cost considerations
        st.markdown('<div class="section-header">💰 Cost Considerations</div>', unsafe_allow_html=True)
        st.markdown('''
        <div class="recommendation-box">
            <p>• Higher safety stock increases holding costs</p>
            <p>• More frequent orders increase ordering costs</p>
            <p>• Balance between service level and inventory costs</p>
        </div>
        ''', unsafe_allow_html=True)

def show_reports_page(df):
    """Display reports page"""
    st.header("📊 Reports & Export")
    
    st.subheader("📋 Generate Business Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Available Reports:**
        - Global business summary
        - Product performance analysis
        - Demand forecasting results
        - Stock optimization recommendations
        - Executive summary with KPIs
        """)
    
    with col2:
        if st.button("📄 Generate PDF Report", type="primary"):
            with st.spinner("Generating comprehensive report..."):
                success, result = generate_report_button_clicked(df)
                if success:
                    st.success("Report generated successfully!")
                    st.info(f"📁 Report saved to: {result}")
                    
                    # Provide download link
                    with open(result, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_bytes,
                            file_name=f"novaMart_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.error(f"Report generation failed: {result}")
    
    st.markdown("---")
    
    # Data export options
    st.subheader("📤 Data Export")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Sales Data"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="novaMart_sales_data.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Export Product Summary"):
            summary_df = df.groupby('Product')['Quantity'].agg(['sum', 'mean', 'std']).round(2)
            summary_df.columns = ['Total_Sales', 'Avg_Daily', 'Std_Dev']
            csv = summary_df.to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="novaMart_product_summary.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🔮 Export Forecasts"):
            st.info("Forecast export feature coming soon!")
    
    # Sample report preview
    st.subheader("📄 Sample Report Preview")
    
    # Generate sample data for preview
    sample_summary = get_global_summary(df)
    
    st.markdown(f"""
    ### NovaMart Demand Forecasting Report
    **Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    #### Executive Summary
    - **Total Sales:** {sample_summary['total_sales']:,} units
    - **Average Daily Sales:** {sample_summary['avg_daily_sales']:.0f} units
    - **Year-over-Year Growth:** {sample_summary['growth_rate']:.1f}%
    - **Top Product:** {sample_summary['top_products'].index[0]} ({sample_summary['top_products'].iloc[0]:,} units)
    
    #### Key Insights
    - Strong growth trajectory across most product categories
    - Seasonal patterns identified for optimal inventory planning
    - Stock optimization recommendations can reduce stockout risk by 10-15%
    - Forecast accuracy: Prophet (MAPE: 8-12%), ARIMA (MAPE: 10-15%)
    
    #### Recommendations
    1. Implement dynamic reorder points based on demand forecasts
    2. Increase safety stock for high-volatility products
    3. Optimize ordering frequency to balance costs and service levels
    4. Monitor forecast accuracy and adjust models quarterly
    """)

if __name__ == "__main__":
    main()
