#!/usr/bin/env python3
"""
Quick runner script to seed the database.
Just run: python run_seed.py
"""
import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seed_database import main

if __name__ == "__main__":
    main()

