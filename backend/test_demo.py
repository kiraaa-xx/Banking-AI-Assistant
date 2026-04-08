#!/usr/bin/env python3
"""
Quick Test Script for Banking Assistant Demo
Tests the demonstration system without requiring full setup
"""

import pandas as pd
import numpy as np
from pathlib import Path

def test_demo_system():
    """Test the demonstration system"""
    print("🧪 Testing Banking Assistant Demo System...")
    
    try:
        # Check if processed data exists
        if Path('processed_banking_dataset.csv').exists():
            data = pd.read_csv('processed_banking_dataset.csv')
            print(f"✅ Processed data loaded: {len(data)} records")
            
            # Show sample data
            print(f"\n📊 Sample Data Preview:")
            print(f"Columns: {list(data.columns)}")
            print(f"Categories: {data['category'].nunique()}")
            print(f"Intents: {data['intent'].nunique()}")
            
            # Show sample records
            print(f"\n📋 Sample Records:")
            for i in range(min(3, len(data))):
                print(f"Record {i+1}:")
                print(f"  Category: {data.iloc[i]['category']}")
                print(f"  Intent: {data.iloc[i]['intent']}")
                print(f"  Instruction: {data.iloc[i]['instruction_clean'][:100]}...")
                print()
            
            print("✅ Demo system test completed successfully!")
            return True
            
        else:
            print("❌ Processed data not found. Please run preprocessing first:")
            print("   python preprocessing_pipeline.py")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_demo_instructions():
    """Show instructions for running the demo"""
    print("\n📋 DEMO INSTRUCTIONS:")
    print("=" * 50)
    print("1. First, run the preprocessing pipeline:")
    print("   python preprocessing_pipeline.py")
    print()
    print("2. Then run the presentation demo:")
    print("   python presentation_demo.py")
    print()
    print("3. For live system demo (requires setup):")
    print("   python demo_system.py")
    print()
    print("4. For interactive banking assistant:")
    print("   python banking_assistant.py")
    print()

def main():
    """Main test function"""
    print("🏦 Banking Assistant System - Demo Test")
    print("=" * 50)
    
    # Test the system
    success = test_demo_system()
    
    if success:
        print("\n🎉 System is ready for demonstration!")
        print("You can now run the presentation demo.")
    else:
        print("\n⚠️ System needs setup before demonstration.")
        print("Please follow the setup instructions.")
    
    # Show demo instructions
    show_demo_instructions()

if __name__ == "__main__":
    main()
