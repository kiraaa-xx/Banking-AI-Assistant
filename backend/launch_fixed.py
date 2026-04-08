#!/usr/bin/env python3
"""
Fixed Launcher for Banking Assistant Web Interface
This version properly launches Streamlit without errors
"""

import subprocess
import sys
import os
import socket
from pathlib import Path

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

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
    
    # Get local IP address
    local_ip = get_local_ip()
    
    print("\n🎯 Starting Streamlit web interface...")
    print("📱 The interface will open in your default web browser")
    print(f"🌐 Local access: http://localhost:8501")
    print(f"🌐 Network access: http://{local_ip}:8501")
    print("\n💡 Tips:")
    print("   • Use Ctrl+C to stop the server")
    print("   • The interface will automatically reload when you make changes")
    print("   • Check the sidebar for system information and quick actions")
    
    print("\n" + "=" * 60)
    
    try:
        # Launch Streamlit using the proper command
        cmd = [
            sys.executable, "-m", "streamlit", "run", "web_interface.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "false"
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to launch web interface: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🏦 Banking Assistant System - Fixed Web Interface Launcher")
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
