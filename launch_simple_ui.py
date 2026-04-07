#!/usr/bin/env python3
"""
Simple Launcher for Banking Assistant Web Interface
Encoding-safe version for Windows
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch the simple web interface"""
    print("🏦 Banking Assistant System - Simple Web Interface")
    print("=" * 60)
    print("Launching encoding-safe version...")
    
    try:
        # Launch Streamlit with the simple interface
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_interface_simple.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to launch: {e}")

if __name__ == "__main__":
    main()
