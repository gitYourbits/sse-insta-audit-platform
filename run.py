"""
Script to run the Instagram Follower Audit Tool.
"""

import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent

# Install the package in development mode if not already installed
if not any(p.startswith("instagram-follower-audit") for p in sys.modules):
    os.system(f"pip install -e {project_root}")

# Run the Streamlit app
if __name__ == "__main__":
    os.system(f"streamlit run {project_root}/app/main.py") 