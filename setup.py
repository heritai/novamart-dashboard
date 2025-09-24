"""
Setup script for NovaMart Dashboard
Handles Prophet installation and dependencies
"""

import subprocess
import sys
import os

def install_packages():
    """Install system packages required for Prophet"""
    try:
        # Try to install Prophet with conda first (faster)
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "prophet", "--no-cache-dir"
        ])
        print("✅ Prophet installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Prophet installation failed, trying alternative...")
        try:
            # Fallback to conda-forge
            subprocess.check_call([
                "conda", "install", "-c", "conda-forge", "prophet", "-y"
            ])
            print("✅ Prophet installed via conda")
            return True
        except subprocess.CalledProcessError:
            print("❌ Prophet installation failed")
            return False

def main():
    """Main setup function"""
    print("🚀 Setting up NovaMart Dashboard...")
    
    # Install Prophet
    if install_packages():
        print("🎉 Setup completed successfully!")
    else:
        print("⚠️ Setup completed with warnings. Prophet may not work correctly.")

if __name__ == "__main__":
    main()
