"""
Main entry point for the Instagram Follower Audit Tool.
"""

import streamlit as st
from app.ui import main

# Page configuration
st.set_page_config(
    page_title="Instagram Follower Audit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if __name__ == "__main__":
    main() 