#!/usr/bin/env python3
"""
Launcher for Banking Assistant Web Interface
Simple script to start the Streamlit web UI
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ All required dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies using:")
        print("pip install -r requirements_web.txt")
        return False

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        'processed_banking_dataset.csv',
        'config.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all files are present before running the web interface.")
        return False
    
    print("✅ All required data files are present!")
    return True

def launch_web_interface():
    """Launch the Streamlit web interface"""
    print("🚀 Launching Banking Assistant Web Interface...")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check data files
    if not check_data_files():
        return False
    
    print("\n🎯 Starting Streamlit web interface...")
    print("📱 The interface will open in your default web browser")
    print("🌐 If it doesn't open automatically, go to: http://localhost:8501")
    print("🌐 For network access, use: http://[YOUR_IP_ADDRESS]:8501")
    print("\n💡 Tips:")
    print("   • Use Ctrl+C to stop the server")
    print("   • The interface will automatically reload when you make changes")
    print("   • Check the sidebar for system information and quick actions")
    
    print("\n" + "=" * 60)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_interface.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to launch web interface: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🏦 Banking Assistant System - Web Interface Launcher")
    print("=" * 60)
    
    # Launch the web interface
    success = launch_web_interface()
    
    if success:
        print("\n✅ Web interface launched successfully!")
    else:
        print("\n❌ Failed to launch web interface")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()
