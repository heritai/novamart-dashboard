# 🚀 NovaMart Dashboard - Streamlit Cloud Deployment Guide

This guide will walk you through deploying the NovaMart Demand Forecasting Dashboard to Streamlit Community Cloud.

## 📋 Prerequisites

1. **GitHub Account**: You need a GitHub account
2. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Repository**: Your code should be in a GitHub repository

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** (if you haven't already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: NovaMart Dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/novamart-dashboard.git
   git push -u origin main
   ```

2. **Ensure all files are included**:
   - ✅ `app.py` (main application)
   - ✅ `requirements.txt` (Python dependencies)
   - ✅ `packages.txt` (system packages for Prophet)
   - ✅ `utils/` directory (all utility modules)
   - ✅ `sample_data/sales_data.csv` (synthetic data)
   - ✅ `.streamlit/config.toml` (theme configuration)

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

2. **Sign in with GitHub**: Use your GitHub credentials

3. **Click "New app"**: 
   - Select your repository: `YOUR_USERNAME/novamart-dashboard`
   - Select branch: `main`
   - Main file path: `app.py`

4. **Configure the app**:
   - **App URL**: Choose a custom URL (e.g., `novamart-forecasting`)
   - **Python version**: 3.9 (recommended)
   - **Advanced settings**: Leave as default

5. **Deploy**: Click "Deploy!"

### Step 3: Monitor Deployment

The deployment process will:
1. Install system packages (gcc, g++, make) for Prophet
2. Install Python dependencies from `requirements.txt`
3. Start the Streamlit application

**Expected deployment time**: 5-10 minutes (first time)

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. **Prophet Installation Fails**
**Error**: `Microsoft Visual C++ 14.0 is required`
**Solution**: The `packages.txt` file should handle this automatically. If it fails, try:
```toml
# In packages.txt
gcc
g++
make
cmake
```

#### 2. **Memory Issues**
**Error**: `Process killed due to memory limit`
**Solution**: The optimizations we implemented should prevent this, but if it occurs:
- Reduce the data subset size in `forecasting.py`
- Use fewer forecast periods

#### 3. **Slow Loading**
**Solution**: The caching system should handle this, but ensure:
- All `@st.cache_data` decorators are in place
- The app is using the optimized models

#### 4. **File Not Found Errors**
**Error**: `FileNotFoundError: sample_data/sales_data.csv`
**Solution**: Ensure the file structure is correct:
```
novamart-dashboard/
├── app.py
├── requirements.txt
├── packages.txt
├── utils/
│   ├── data_prep.py
│   ├── forecasting.py
│   ├── stock_opt.py
│   └── report_generator.py
└── sample_data/
    └── sales_data.csv
```

## 📊 Performance Optimization

The deployed app includes several optimizations:

1. **Caching**: Results are cached for instant loading
2. **Data Subsets**: Uses 6 months of data instead of 2 years
3. **Model Optimization**: Simplified Prophet and ARIMA models
4. **Progress Indicators**: Better user experience

## 🔗 Accessing Your Deployed App

Once deployed, your app will be available at:
```
https://YOUR_APP_NAME.streamlit.app
```

## 📈 Monitoring and Updates

### Updating Your App
1. Make changes to your local code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main
   ```
3. Streamlit Cloud will automatically redeploy

### Monitoring Performance
- Check the Streamlit Cloud dashboard for logs
- Monitor memory usage and response times
- Use the built-in analytics to track usage

## 🎯 Best Practices

1. **Keep Dependencies Updated**: Regularly update `requirements.txt`
2. **Monitor Resource Usage**: Watch for memory or CPU limits
3. **Test Locally First**: Always test changes locally before deploying
4. **Use Caching**: Leverage Streamlit's caching for better performance
5. **Optimize Models**: Keep models lightweight for cloud deployment

## 🆘 Getting Help

If you encounter issues:

1. **Check Streamlit Cloud Logs**: Available in your app dashboard
2. **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
3. **GitHub Issues**: Create an issue in your repository
4. **Documentation**: [docs.streamlit.io](https://docs.streamlit.io)

## 🎉 Success!

Once deployed, you'll have a fully functional NovaMart Dashboard accessible from anywhere with:
- ✅ Interactive forecasting
- ✅ Stock optimization
- ✅ PDF report generation
- ✅ Real-time analytics
- ✅ Professional UI

Your dashboard will be ready to demonstrate to clients and stakeholders!
