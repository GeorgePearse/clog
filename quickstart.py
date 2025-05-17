#!/usr/bin/env python3
"""
QUICKSTART GUIDE FOR CLOG
========================

Just run: python quickstart.py
"""

import subprocess
import sys
import os

def main():
    print("🚀 clog Quickstart")
    print("=================")
    print()
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  No virtual environment detected!")
        print("Creating one now...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
        
        print("\n✅ Virtual environment created!")
        print("\nNow run these commands:")
        print("\n1. Activate the environment:")
        print("   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
        print("\n2. Run this script again:")
        print("   python quickstart.py")
        return
    
    print("✅ Virtual environment detected")
    
    # Install maturin
    print("\n📦 Installing build tools...")
    subprocess.run([sys.executable, "-m", "pip", "install", "maturin"])
    
    # Build clog
    print("\n🔨 Building clog...")
    subprocess.run(["maturin", "develop", "--release"])
    
    print("\n✅ Installation complete!")
    print("\n🎮 Running demo...")
    print("-" * 40)
    
    # Run the demo
    subprocess.run([sys.executable, "examples/simple_demo.py"])

if __name__ == "__main__":
    main()