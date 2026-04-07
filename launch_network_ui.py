#!/usr/bin/env python3
"""
Launcher for Banking Assistant Web Interface - Network Access Enabled
This version allows access from other computers on the network
"""

import subprocess
import sys
import os
import socket
from pathlib import Path

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a remote address to determine local IP
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

def launch_network_interface():
    """Launch the Streamlit web interface with network access"""
    print("🚀 Launching Banking Assistant Web Interface - Network Access Enabled")
    print("=" * 70)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check data files
    if not check_data_files():
        return False
    
    # Get local IP address
    local_ip = get_local_ip()
    
    print("\n🎯 Starting Streamlit web interface with network access...")
    print("📱 The interface will open in your default web browser")
    print(f"🌐 Local access: http://localhost:8501")
    print(f"🌐 Network access: http://{local_ip}:8501")
    print("\n💡 Network Access Tips:")
    print("   • Other computers on the same network can access using the network URL above")
    print("   • Make sure your firewall allows connections on port 8501")
    print("   • Use Ctrl+C to stop the server")
    print("   • The interface will automatically reload when you make changes")
    
    print("\n" + "=" * 70)
    
    try:
        # Launch Streamlit with network access enabled
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_interface.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to launch web interface: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🏦 Banking Assistant System - Network Web Interface Launcher")
    print("=" * 70)
    
    # Launch the web interface
    success = launch_network_interface()
    
    if success:
        print("\n✅ Web interface launched successfully!")
    else:
        print("\n❌ Failed to launch web interface")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()
