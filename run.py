# run.py - Entry point for Notarnicola Data Management System
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.cli.main import main

if __name__ == "__main__":
    main()