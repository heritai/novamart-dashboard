"""
Stock optimization utilities for NovaMart inventory management
Implements reorder point and safety stock calculations
"""

import pandas as pd
import numpy as np
from scipy import stats

def calculate_safety_stock(avg_demand, demand_std, lead_time, service_level=0.95):
    """
    Calculate safety stock using statistical approach
    
    Args:
        avg_demand: Average daily demand
        demand_std: Standard deviation of daily demand
        lead_time: Lead time in days
        service_level: Desired service level (default 95%)
    
    Returns:
        float: Safety stock quantity
    """
    # Z-score for desired service level
    z_score = stats.norm.ppf(service_level)
    
    # Safety stock = Z * sqrt(lead_time) * demand_std
    safety_stock = z_score * np.sqrt(lead_time) * demand_std
    
    return max(0, safety_stock)

def calculate_reorder_point(avg_demand, lead_time, safety_stock):
    """
    Calculate reorder point
    
    Args:
        avg_demand: Average daily demand
        lead_time: Lead time in days
        safety_stock: Safety stock quantity
    
    Returns:
        float: Reorder point
    """
    # Reorder Point = (Average Demand × Lead Time) + Safety Stock
    reorder_point = (avg_demand * lead_time) + safety_stock
    
    return max(0, reorder_point)

def calculate_economic_order_quantity(annual_demand, ordering_cost, holding_cost):
    """
    Calculate Economic Order Quantity (EOQ)
    
    Args:
        annual_demand: Annual demand quantity
        ordering_cost: Cost per order
        holding_cost: Holding cost per unit per year
    
    Returns:
        float: Economic order quantity
    """
    if holding_cost <= 0:
        return annual_demand  # Fallback if holding cost is 0
    
    eoq = np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
    return max(1, eoq)

def get_stock_recommendations(df, product_name, lead_time_days=7, safety_stock_percent=20, service_level=0.95):
    """
    Get comprehensive stock recommendations for a product
    
    Args:
        df: Product sales data
        product_name: Name of the product
        lead_time_days: Lead time in days
        safety_stock_percent: Safety stock as percentage of average demand
        service_level: Desired service level (0-1)
    
    Returns:
        dict: Stock optimization recommendations
    """
    # Calculate demand statistics
    avg_daily_demand = df['Quantity'].mean()
    demand_std = df['Quantity'].std()
    annual_demand = avg_daily_demand * 365
    
    # Calculate safety stock using statistical method
    statistical_safety_stock = calculate_safety_stock(
        avg_daily_demand, demand_std, lead_time_days, service_level
    )
    
    # Calculate safety stock using percentage method
    percentage_safety_stock = avg_daily_demand * (safety_stock_percent / 100)
    
    # Use the higher of the two methods
    safety_stock = max(statistical_safety_stock, percentage_safety_stock)
    
    # Calculate reorder point
    reorder_point = calculate_reorder_point(avg_daily_demand, lead_time_days, safety_stock)
    
    # Calculate EOQ (using estimated costs)
    # These are typical retail values - in real implementation, these would come from business data
    ordering_cost = 50  # Cost per order
    holding_cost = avg_daily_demand * 0.1  # 10% of daily demand value as holding cost
    
    eoq = calculate_economic_order_quantity(annual_demand, ordering_cost, holding_cost)
    
    # Calculate stockout risk reduction
    # This is a simplified calculation showing the improvement in service level
    current_service_level = 0.85  # Assume current service level
    improvement = (service_level - current_service_level) * 100
    
    # Calculate recommended reorder quantity
    # Use EOQ or lead time demand + safety stock, whichever is higher
    lead_time_demand = avg_daily_demand * lead_time_days
    recommended_reorder_qty = max(eoq, lead_time_demand + safety_stock)
    
    return {
        'product_name': product_name,
        'avg_daily_demand': avg_daily_demand,
        'demand_std': demand_std,
        'lead_time_days': lead_time_days,
        'safety_stock': safety_stock,
        'reorder_point': reorder_point,
        'recommended_reorder_qty': recommended_reorder_qty,
        'economic_order_quantity': eoq,
        'service_level': service_level,
        'stockout_risk_reduction': improvement,
        'annual_demand': annual_demand
    }

def create_stock_optimization_chart(recommendations, historical_data):
    """
    Create visualization for stock optimization recommendations
    
    Args:
        recommendations: Stock recommendations dict
        historical_data: Historical demand data
    
    Returns:
        plotly figure: Stock optimization chart
    """
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Demand Distribution & Reorder Point', 'Stock Level Simulation'),
        vertical_spacing=0.15  # Increased spacing between subplots
    )
    
    # Plot 1: Demand distribution with reorder point
    fig.add_trace(
        go.Histogram(
            x=historical_data['Quantity'],
            nbinsx=30,
            name='Demand Distribution',
            opacity=0.7,
            marker_color='lightblue'
        ),
        row=1, col=1
    )
    
    # Add reorder point line
    fig.add_vline(
        x=recommendations['reorder_point'],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Reorder Point: {recommendations['reorder_point']:.0f}",
        row=1, col=1
    )
    
    # Add average demand line
    fig.add_vline(
        x=recommendations['avg_daily_demand'],
        line_dash="dot",
        line_color="green",
        annotation_text=f"Avg Demand: {recommendations['avg_daily_demand']:.0f}",
        row=1, col=1
    )
    
    # Plot 2: Stock level simulation (simplified)
    days = list(range(30))
    stock_levels = []
    current_stock = recommendations['recommended_reorder_qty']
    
    for day in days:
        # Simulate demand (using historical average with some randomness)
        daily_demand = max(0, np.random.normal(
            recommendations['avg_daily_demand'], 
            recommendations['demand_std']
        ))
        
        # Update stock level
        current_stock = max(0, current_stock - daily_demand)
        
        # Reorder if below reorder point
        if current_stock <= recommendations['reorder_point']:
            current_stock += recommendations['recommended_reorder_qty']
        
        stock_levels.append(current_stock)
    
    fig.add_trace(
        go.Scatter(
            x=days,
            y=stock_levels,
            mode='lines',
            name='Stock Level',
            line=dict(color='blue', width=2)
        ),
        row=2, col=1
    )
    
    # Add reorder point line to stock simulation
    fig.add_hline(
        y=recommendations['reorder_point'],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Reorder Point",
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"Stock Optimization Analysis - {recommendations['product_name']}",
        height=700,  # Increased height to prevent overlap
        showlegend=True,
        margin=dict(l=50, r=50, t=80, b=50)  # Add margins to prevent overlap
    )
    
    fig.update_xaxes(title_text="Daily Demand", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)
    fig.update_xaxes(title_text="Days", row=2, col=1)
    fig.update_yaxes(title_text="Stock Level", row=2, col=1)
    
    return fig

def calculate_inventory_metrics(recommendations, current_inventory=None):
    """
    Calculate key inventory performance metrics
    
    Args:
        recommendations: Stock recommendations dict
        current_inventory: Current inventory level (optional)
    
    Returns:
        dict: Inventory performance metrics
    """
    avg_daily_demand = recommendations['avg_daily_demand']
    reorder_point = recommendations['reorder_point']
    safety_stock = recommendations['safety_stock']
    
    # Calculate days of inventory
    if current_inventory:
        days_of_inventory = current_inventory / avg_daily_demand
    else:
        days_of_inventory = recommendations['recommended_reorder_qty'] / avg_daily_demand
    
    # Calculate inventory turnover (annual)
    annual_demand = recommendations['annual_demand']
    avg_inventory = (recommendations['recommended_reorder_qty'] + safety_stock) / 2
    inventory_turnover = annual_demand / avg_inventory if avg_inventory > 0 else 0
    
    # Calculate stockout probability (simplified)
    # This is a rough estimate based on demand variability
    cv = recommendations['demand_std'] / avg_daily_demand if avg_daily_demand > 0 else 0
    stockout_probability = max(0, min(1, cv * 0.5))  # Simplified calculation
    
    return {
        'days_of_inventory': days_of_inventory,
        'inventory_turnover': inventory_turnover,
        'stockout_probability': stockout_probability,
        'safety_stock_coverage': safety_stock / avg_daily_demand if avg_daily_demand > 0 else 0
    }

def get_optimization_summary(recommendations, metrics):
    """
    Generate a summary of optimization recommendations
    
    Args:
        recommendations: Stock recommendations dict
        metrics: Inventory metrics dict
    
    Returns:
        dict: Optimization summary
    """
    return {
        'key_recommendations': [
            f"Set reorder point at {recommendations['reorder_point']:.0f} units",
            f"Maintain safety stock of {recommendations['safety_stock']:.0f} units",
            f"Order {recommendations['recommended_reorder_qty']:.0f} units when reordering",
            f"Expected service level: {recommendations['service_level']*100:.1f}%"
        ],
        'expected_benefits': [
            f"Reduce stockout risk by {recommendations['stockout_risk_reduction']:.1f}%",
            f"Inventory turnover: {metrics['inventory_turnover']:.1f} times per year",
            f"Average {metrics['days_of_inventory']:.1f} days of inventory on hand"
        ],
        'cost_considerations': [
            "Higher safety stock increases holding costs",
            "More frequent orders increase ordering costs",
            "Balance between service level and inventory costs"
        ]
    }
