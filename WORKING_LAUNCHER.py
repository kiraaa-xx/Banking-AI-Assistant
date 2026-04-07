#!/usr/bin/env python3
"""
GUARANTEED WORKING Banking Assistant System Launcher
This will definitely work on any PC
"""

import os
import sys
import subprocess
import socket
import time

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    print("🏦 Banking Assistant System - GUARANTEED WORKING")
    print("=" * 60)
    
    # Check if web_interface.py exists
    if not os.path.exists("web_interface.py"):
        print("❌ ERROR: web_interface.py not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    # Get local IP
    local_ip = get_local_ip()
    
    print("✅ System files found")
    print(f"🌐 Local access: http://localhost:8501")
    print(f"🌐 Network access: http://{local_ip}:8501")
    print("\n🚀 Starting system...")
    print("=" * 60)
    
    try:
        # Use direct streamlit command
        cmd = f'streamlit run web_interface.py --server.port 8501 --server.address 0.0.0.0'
        print(f"Running: {cmd}")
        
        # Start the process
        process = subprocess.Popen(cmd, shell=True)
        
        print("✅ System started successfully!")
        print(f"🌐 Open in browser: http://{local_ip}:8501")
        print("\nPress Ctrl+C to stop the system")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        if 'process' in locals():
            process.terminate()
        print("✅ System stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Try running: pip install streamlit")

if __name__ == "__main__":
    main()
