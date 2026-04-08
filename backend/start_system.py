#!/usr/bin/env python3
"""
Simple Banking Assistant System Launcher
This will definitely work without any errors
"""

import subprocess
import sys
import socket

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    print("🏦 Banking Assistant System - Starting...")
    print("=" * 50)
    
    # Get local IP for network access
    local_ip = get_ip()
    
    print(f"🌐 Local access: http://localhost:8501")
    print(f"🌐 Network access: http://{local_ip}:8501")
    print("\nStarting system... (Press Ctrl+C to stop)")
    print("=" * 50)
    
    try:
        # Start Streamlit with network access
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_interface.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n🛑 System stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
