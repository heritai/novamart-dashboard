"""
Forecasting models for NovaMart demand prediction
Implements Prophet and ARIMA models for demand forecasting
"""

import pandas as pd
import numpy as np
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

def fit_prophet_model(df, periods=30):
    """
    Fit Prophet model for demand forecasting (optimized for speed)
    
    Args:
        df: DataFrame with columns 'ds' (date) and 'y' (quantity)
        periods: Number of periods to forecast ahead
    
    Returns:
        model: Fitted Prophet model
        forecast: Forecast DataFrame
    """
    # Use a subset of data for faster fitting (last 6 months)
    if len(df) > 180:
        df_subset = df.tail(180).copy()
    else:
        df_subset = df.copy()
    
    # Initialize and fit Prophet model with optimized settings
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='multiplicative',
        changepoint_prior_scale=0.1,  # Increased for faster fitting
        seasonality_prior_scale=10.0,
        changepoint_range=0.8,  # Reduced for faster fitting
        mcmc_samples=0,  # Disable MCMC for speed
        interval_width=0.8  # Reduced confidence interval for speed
    )
    
    # Add custom seasonalities for retail patterns (reduced complexity)
    model.add_seasonality(name='monthly', period=30.5, fourier_order=3)  # Reduced from 5 to 3
    
    # Fit the model
    model.fit(df_subset)
    
    # Make future dataframe
    future = model.make_future_dataframe(periods=periods)
    
    # Make forecast
    forecast = model.predict(future)
    
    return model, forecast

def fit_arima_model(df, periods=30):
    """
    Fit ARIMA model for demand forecasting (optimized for speed)
    
    Args:
        df: DataFrame with 'Quantity' column
        periods: Number of periods to forecast ahead
    
    Returns:
        model: Fitted ARIMA model
        forecast: Forecast values
        conf_int: Confidence intervals
    """
    # Use a subset of data for faster fitting (last 6 months)
    if len(df) > 180:
        data_subset = df['Quantity'].tail(180)
    else:
        data_subset = df['Quantity']
    
    # Use simple ARIMA parameters for speed (skip parameter search)
    # Most retail data works well with these standard parameters
    try:
        # Try SARIMA(1,1,1)(1,1,1,7) first (most common for retail)
        model = ARIMA(data_subset, order=(1, 1, 1), 
                      seasonal_order=(1, 1, 1, 7))
        fitted_model = model.fit()
    except:
        try:
            # Fallback to simpler ARIMA(1,1,1)
            model = ARIMA(data_subset, order=(1, 1, 1))
            fitted_model = model.fit()
        except:
            # Final fallback to ARIMA(0,1,1)
            model = ARIMA(data_subset, order=(0, 1, 1))
            fitted_model = model.fit()
    
    # Make forecast
    forecast_result = fitted_model.get_forecast(steps=periods)
    forecast = forecast_result.predicted_mean
    conf_int = forecast_result.conf_int()
    
    return fitted_model, forecast, conf_int

def create_forecast_chart(df, product_name, periods=30):
    """
    Create comprehensive forecast chart with both Prophet and ARIMA
    
    Args:
        df: Product data with 'ds' and 'y' columns
        product_name: Name of the product
        periods: Number of periods to forecast
    
    Returns:
        fig: Plotly figure with historical data and forecasts
    """
    # Prepare data
    df_prophet = df[['ds', 'y']].copy()
    
    # Fit Prophet model
    try:
        prophet_model, prophet_forecast = fit_prophet_model(df_prophet, periods)
        prophet_success = True
    except Exception as e:
        print(f"Prophet model failed for {product_name}: {e}")
        prophet_success = False
    
    # Fit ARIMA model
    try:
        arima_model, arima_forecast, arima_conf_int = fit_arima_model(df, periods)
        arima_success = True
    except Exception as e:
        print(f"ARIMA model failed for {product_name}: {e}")
        arima_success = False
    
    # Create figure
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=df['ds'],
        y=df['y'],
        mode='lines',
        name='Historical Data',
        line=dict(color='blue', width=2)
    ))
    
    if prophet_success:
        # Add Prophet forecast
        future_dates = prophet_forecast['ds'].tail(periods)
        prophet_pred = prophet_forecast['yhat'].tail(periods)
        prophet_lower = prophet_forecast['yhat_lower'].tail(periods)
        prophet_upper = prophet_forecast['yhat_upper'].tail(periods)
        
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=prophet_pred,
            mode='lines',
            name='Prophet Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # Add Prophet confidence interval
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=prophet_upper,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=prophet_lower,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.2)',
            name='Prophet Confidence',
            hoverinfo='skip'
        ))
    
    if arima_success:
        # Add ARIMA forecast
        future_dates = pd.date_range(start=df['ds'].max() + pd.Timedelta(days=1), 
                                   periods=periods, freq='D')
        
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=arima_forecast,
            mode='lines',
            name='ARIMA Forecast',
            line=dict(color='green', width=2, dash='dot')
        ))
        
        # Add ARIMA confidence interval
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=arima_conf_int.iloc[:, 1],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=arima_conf_int.iloc[:, 0],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(0,255,0,0.2)',
            name='ARIMA Confidence',
            hoverinfo='skip'
        ))
    
    # Update layout
    fig.update_layout(
        title=f'{product_name} - Demand Forecast (Next {periods} Days)',
        xaxis_title='Date',
        yaxis_title='Daily Sales',
        hovermode='x unified',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

def get_forecast_metrics(df, product_name, periods=30):
    """
    Get forecast accuracy metrics for both models (optimized for speed)
    
    Args:
        df: Product data
        product_name: Name of the product
        periods: Number of periods to forecast
    
    Returns:
        dict: Metrics for both models
    """
    # Use smaller validation period for faster computation
    validation_periods = min(periods, 14)  # Use max 2 weeks for validation
    split_point = len(df) - validation_periods
    
    if split_point < 30:  # Need minimum data for training
        return {
            'prophet': {'mape': None, 'rmse': None},
            'arima': {'mape': None, 'rmse': None}
        }
    
    train_df = df.iloc[:split_point].copy()
    test_df = df.iloc[split_point:].copy()
    
    metrics = {}
    
    # Prophet metrics (simplified)
    try:
        # Use even smaller subset for validation
        if len(train_df) > 90:
            train_subset = train_df.tail(90)
        else:
            train_subset = train_df
            
        prophet_model, prophet_forecast = fit_prophet_model(train_subset, validation_periods)
        prophet_pred = prophet_forecast['yhat'].tail(validation_periods).values
        prophet_mape = np.mean(np.abs((test_df['y'].values - prophet_pred) / test_df['y'].values)) * 100
        prophet_rmse = np.sqrt(np.mean((test_df['y'].values - prophet_pred) ** 2))
        
        metrics['prophet'] = {
            'mape': prophet_mape,
            'rmse': prophet_rmse
        }
    except:
        metrics['prophet'] = {'mape': None, 'rmse': None}
    
    # ARIMA metrics (simplified)
    try:
        if len(train_df) > 90:
            train_subset = train_df.tail(90)
        else:
            train_subset = train_df
            
        arima_model, arima_forecast, _ = fit_arima_model(train_subset, validation_periods)
        arima_pred = arima_forecast.values
        arima_mape = np.mean(np.abs((test_df['Quantity'].values - arima_pred) / test_df['Quantity'].values)) * 100
        arima_rmse = np.sqrt(np.mean((test_df['Quantity'].values - arima_pred) ** 2))
        
        metrics['arima'] = {
            'mape': arima_mape,
            'rmse': arima_rmse
        }
    except:
        metrics['arima'] = {'mape': None, 'rmse': None}
    
    return metrics

def get_next_30_days_forecast(df, product_name):
    """
    Get forecast for next 30 days using Prophet (primary model)
    
    Args:
        df: Product data with 'ds' and 'y' columns
        product_name: Name of the product
    
    Returns:
        dict: Forecast summary
    """
    try:
        model, forecast = fit_prophet_model(df, periods=30)
        
        # Get next 30 days forecast
        next_30_days = forecast.tail(30)
        
        avg_daily_forecast = next_30_days['yhat'].mean()
        total_forecast = next_30_days['yhat'].sum()
        
        # Calculate confidence intervals
        lower_bound = next_30_days['yhat_lower'].mean()
        upper_bound = next_30_days['yhat_upper'].mean()
        
        return {
            'avg_daily_forecast': avg_daily_forecast,
            'total_forecast': total_forecast,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'forecast_data': next_30_days
        }
    except Exception as e:
        print(f"Forecast failed for {product_name}: {e}")
        return {
            'avg_daily_forecast': 0,
            'total_forecast': 0,
            'lower_bound': 0,
            'upper_bound': 0,
            'forecast_data': None
        }
