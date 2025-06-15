"""
Main Streamlit dashboard for the Instagram Follower Audit Tool.
This module provides the user interface for the application.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any
import time
from datetime import datetime
import json
import os
from pathlib import Path
import traceback
import asyncio

from app.core.workflow import WorkflowController
from app.core.logger import AuditLogger
from app.ui.components import (
    metric_card,
    status_badge,
    profile_preview,
    info_box,
    loading_spinner,
    error_message,
    success_message,
    stats_summary,
    engagement_chart,
    recommendation_list,
    file_uploader
)

def initialize_session_state():
    """Initialize all session state variables."""
    if "audit_results" not in st.session_state:
        st.session_state.audit_results = None
    if "processing_time" not in st.session_state:
        st.session_state.processing_time = 0
    if "show_logs" not in st.session_state:
        st.session_state.show_logs = False
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "engagement_threshold" not in st.session_state:
        st.session_state.engagement_threshold = 0.3
    if "risk_threshold" not in st.session_state:
        st.session_state.risk_threshold = 0.7

def export_results(results: List[Dict], format: str = "csv") -> None:
    """
    Export audit results to file.
    
    Args:
        results: List of audit results
        format: Export format ('csv' or 'json')
    """
    if not results:
        error_message("No results to export")
        return
    
    df = pd.DataFrame(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format == "csv":
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"audit_results_{timestamp}.csv",
            mime="text/csv"
        )
    else:
        json_str = df.to_json(orient="records", indent=2)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name=f"audit_results_{timestamp}.json",
            mime="application/json"
        )

def display_results(results: List[Dict]) -> None:
    """
    Display audit results in an interactive table.
    
    Args:
        results: List of audit results
    """
    if not results:
        st.info("No results to display")
        return
    
    df = pd.DataFrame(results)
    
    # Add status badges
    df["Status"] = df["action"].apply(
        lambda x: status_badge(x)
    )
    
    # Add profile previews
    df["Profile"] = df.apply(
        lambda row: profile_preview(
            row["username"],
            row.get("profile_pic_url")
        ),
        axis=1
    )
    
    # Display interactive table
    st.dataframe(
        df[["Profile", "Status", "reason", "engagement_score", "risk_score"]],
        use_container_width=True,
        hide_index=True
    )

def process_json_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process JSON data into the expected format.
    
    Args:
        data: List of follower data dictionaries
        
    Returns:
        Processed list of follower data
    """
    processed_data = []
    for follower in data:
        if not isinstance(follower, dict):
            continue
            
        # Validate required fields
        if "username" not in follower:
            raise ValueError(f"Missing username in follower data: {follower}")
            
        processed_data.append(follower)
    
    return processed_data

async def process_followers(workflow: WorkflowController, followers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process followers asynchronously.
    
    Args:
        workflow: WorkflowController instance
        followers: List of follower data
        
    Returns:
        List of audit results
    """
    results = []
    for follower in followers:
        try:
            result = await workflow.audit_follower(follower)
            results.append(result)
        except Exception as e:
            error_message(
                f"Error processing {follower.get('username', 'Unknown')}",
                str(e)
            )
    return results

def main():
    """Main dashboard function."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("📊 Instagram Follower Audit")
    st.markdown("""
        Analyze your Instagram followers to identify engaged followers and potential fake accounts.
        Upload your follower data to get started.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # API Key input
        st.session_state.api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_key,
            type="password",
            help="Required for profile analysis"
        )
        
        # Thresholds
        st.subheader("Thresholds")
        st.session_state.engagement_threshold = st.slider(
            "Minimum Engagement Score",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.engagement_threshold,
            step=0.1
        )
        
        st.session_state.risk_threshold = st.slider(
            "Maximum Risk Score",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.risk_threshold,
            step=0.1
        )
        
        # Logging toggle
        st.session_state.show_logs = st.checkbox(
            "Show Processing Logs",
            value=st.session_state.show_logs
        )
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload
        uploaded_file = file_uploader(
            "Upload Follower Data",
            ["json", "csv"],
            "Upload a JSON or CSV file containing follower data"
        )
        
        if uploaded_file:
            try:
                # Process file
                if uploaded_file.name.endswith(".json"):
                    data = json.load(uploaded_file)
                    followers = process_json_data(data)
                else:
                    followers = pd.read_csv(uploaded_file).to_dict("records")
                
                # Initialize workflow
                workflow = WorkflowController(
                    api_key=st.session_state.api_key if st.session_state.api_key else None
                )
                
                # Start audit
                if st.button("Start Audit"):
                    with loading_spinner("Analyzing followers..."):
                        start_time = time.time()
                        
                        # Process followers asynchronously
                        results = asyncio.run(process_followers(workflow, followers))
                        
                        # Store results
                        st.session_state.audit_results = results
                        st.session_state.processing_time = time.time() - start_time
                        
                        success_message("Audit completed successfully!")
                
                # Display results
                if st.session_state.audit_results:
                    st.subheader("Audit Results")
                    
                    # Statistics
                    stats_summary(
                        total=len(st.session_state.audit_results),
                        keep=sum(1 for r in st.session_state.audit_results if r["action"] == "keep"),
                        remove=sum(1 for r in st.session_state.audit_results if r["action"] == "remove"),
                        processing_time=st.session_state.processing_time
                    )
                    
                    # Results table
                    display_results(st.session_state.audit_results)
                    
                    # Export options
                    st.subheader("Export Results")
                    col1, col2 = st.columns(2)
                    with col1:
                        export_results(st.session_state.audit_results, "csv")
                    with col2:
                        export_results(st.session_state.audit_results, "json")
            
            except Exception as e:
                error_message(
                    "Error processing file",
                    f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
                )
    
    with col2:
        # Information panel
        info_box(
            "About",
            """
            This tool helps you analyze your Instagram followers to:
            - Identify engaged followers
            - Detect potential fake accounts
            - Optimize your follower base
            """,
            "ℹ️"
        )
        
        # Logs panel
        if st.session_state.show_logs:
            st.subheader("Processing Logs")
            log_file = AuditLogger.get_latest_log()
            if log_file and os.path.exists(log_file):
                with open(log_file, "r") as f:
                    st.code(f.read())
            else:
                st.info("No logs available")

if __name__ == "__main__":
    main() 