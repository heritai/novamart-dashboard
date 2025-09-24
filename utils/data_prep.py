"""
Data preparation utilities for NovaMart forecasting dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_sales_data(file_path):
    """Load and prepare sales data"""
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Date', 'Product']).reset_index(drop=True)
    return df

def get_global_summary(df):
    """Calculate global summary statistics"""
    total_sales = df['Quantity'].sum()
    avg_daily_sales = df.groupby('Date')['Quantity'].sum().mean()
    
    # Top 3 products by total sales
    top_products = df.groupby('Product')['Quantity'].sum().sort_values(ascending=False).head(3)
    
    # Calculate growth rate (comparing first 6 months vs last 6 months)
    first_half = df[df['Date'] <= df['Date'].max() - timedelta(days=365)]
    second_half = df[df['Date'] > df['Date'].max() - timedelta(days=365)]
    
    first_half_sales = first_half['Quantity'].sum()
    second_half_sales = second_half['Quantity'].sum()
    growth_rate = ((second_half_sales - first_half_sales) / first_half_sales) * 100
    
    return {
        'total_sales': total_sales,
        'avg_daily_sales': avg_daily_sales,
        'top_products': top_products,
        'growth_rate': growth_rate
    }

def create_demand_trend_chart(df):
    """Create total demand trend chart"""
    daily_totals = df.groupby('Date')['Quantity'].sum().reset_index()
    
    fig = px.line(daily_totals, x='Date', y='Quantity', 
                  title='Total Daily Demand Trend',
                  labels={'Quantity': 'Daily Sales', 'Date': 'Date'})
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Daily Sales",
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_product_comparison_chart(df, chart_type='bar'):
    """Create product sales comparison chart"""
    product_totals = df.groupby('Product')['Quantity'].sum().sort_values(ascending=True)
    
    if chart_type == 'bar':
        fig = px.bar(x=product_totals.values, y=product_totals.index, 
                     orientation='h',
                     title='Total Sales by Product',
                     labels={'x': 'Total Sales', 'y': 'Product'})
    else:  # pie chart
        fig = px.pie(values=product_totals.values, names=product_totals.index,
                     title='Sales Distribution by Product')
    
    fig.update_layout(height=400)
    return fig

def create_seasonality_heatmap(df):
    """Create seasonality heatmap showing sales by month and day of week"""
    df_copy = df.copy()
    df_copy['Month'] = df_copy['Date'].dt.month
    df_copy['DayOfWeek'] = df_copy['Date'].dt.day_name()
    
    # Aggregate by month and day of week
    heatmap_data = df_copy.groupby(['Month', 'DayOfWeek'])['Quantity'].sum().reset_index()
    
    # Pivot for heatmap
    heatmap_pivot = heatmap_data.pivot(index='DayOfWeek', columns='Month', values='Quantity')
    
    # Reorder days of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex(day_order)
    
    # Create heatmap
    fig = px.imshow(heatmap_pivot.values,
                    labels=dict(x="Month", y="Day of Week", color="Sales"),
                    x=heatmap_pivot.columns,
                    y=heatmap_pivot.index,
                    title="Sales Heatmap: Day of Week vs Month",
                    color_continuous_scale='Blues')
    
    fig.update_layout(height=400)
    return fig

def prepare_product_data(df, product_name):
    """Prepare data for a specific product"""
    product_df = df[df['Product'] == product_name].copy()
    product_df = product_df.sort_values('Date').reset_index(drop=True)
    
    # Add time-based features
    product_df['ds'] = product_df['Date']  # Prophet expects 'ds' column
    product_df['y'] = product_df['Quantity']  # Prophet expects 'y' column
    
    return product_df

def get_product_summary(df, product_name):
    """Get summary statistics for a specific product"""
    product_df = df[df['Product'] == product_name]
    
    total_sales = product_df['Quantity'].sum()
    avg_daily_sales = product_df['Quantity'].mean()
    std_daily_sales = product_df['Quantity'].std()
    
    # Calculate trend (simple linear regression slope)
    x = np.arange(len(product_df))
    y = product_df['Quantity'].values
    if len(x) > 1:
        trend = np.polyfit(x, y, 1)[0]
    else:
        trend = 0
    
    # Calculate coefficient of variation (volatility)
    cv = (std_daily_sales / avg_daily_sales) * 100 if avg_daily_sales > 0 else 0
    
    return {
        'total_sales': total_sales,
        'avg_daily_sales': avg_daily_sales,
        'std_daily_sales': std_daily_sales,
        'trend': trend,
        'volatility': cv
    }

def create_product_trend_chart(df, product_name):
    """Create trend chart for a specific product"""
    product_df = df[df['Product'] == product_name].copy()
    
    fig = px.line(product_df, x='Date', y='Quantity',
                  title=f'{product_name} - Daily Sales Trend',
                  labels={'Quantity': 'Daily Sales', 'Date': 'Date'})
    
    # Add moving average
    product_df['MA_7'] = product_df['Quantity'].rolling(window=7).mean()
    product_df['MA_30'] = product_df['Quantity'].rolling(window=30).mean()
    
    fig.add_trace(go.Scatter(x=product_df['Date'], y=product_df['MA_7'],
                            mode='lines', name='7-day MA', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=product_df['Date'], y=product_df['MA_30'],
                            mode='lines', name='30-day MA', line=dict(dash='dot')))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Daily Sales",
        hovermode='x unified',
        height=400
    )
    
    return fig
