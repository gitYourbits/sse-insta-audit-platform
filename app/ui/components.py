"""
Reusable UI components for the Instagram Follower Audit Tool.
This module provides custom Streamlit components for consistent UI elements.
"""

import streamlit as st
from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
from PIL import Image
import io
import base64
from app.constants import EvaluationAction

def metric_card(
    title: str,
    value: float,
    delta: Optional[float] = None,
    format: str = "%.2f"
) -> None:
    """
    Display a metric card with optional delta.
    
    Args:
        title: The metric title
        value: The metric value
        delta: Optional delta value
        format: Format string for the value
    """
    st.metric(
        label=title,
        value=format % value,
        delta=f"{delta:+.1%}" if delta is not None else None
    )

def status_badge(action: str) -> str:
    """
    Create a colored status badge for keep/remove actions.
    
    Args:
        action: The action ('keep' or 'remove')
        
    Returns:
        HTML string for the badge
    """
    color = "green" if action == EvaluationAction.KEEP.value else "red"
    return f"""
        <div style="
            background-color: {color};
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            display: inline-block;
            font-size: 0.8em;
        ">
            {action.upper()}
        </div>
    """

def profile_preview(
    username: str,
    profile_pic_url: Optional[str] = None,
    size: int = 40
) -> str:
    """
    Create a profile preview with username and optional profile picture.
    
    Args:
        username: The username to display
        profile_pic_url: Optional URL to profile picture
        size: Size of the profile picture in pixels
        
    Returns:
        HTML string for the profile preview
    """
    if profile_pic_url:
        return f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="{profile_pic_url}" 
                     style="width: {size}px; height: {size}px; border-radius: 50%;">
                <span>{username}</span>
            </div>
        """
    return f'<div style="padding-left: {size + 10}px;">{username}</div>'

def info_box(
    title: str,
    content: str,
    icon: Optional[str] = None
) -> None:
    """
    Display an information box with optional icon.
    
    Args:
        title: Box title
        content: Box content
        icon: Optional emoji icon
    """
    with st.container():
        st.markdown(f"### {icon or 'ℹ️'} {title}")
        st.markdown(content)
        st.divider()

def loading_spinner(message: str):
    """
    Display a loading spinner with a message.
    
    Args:
        message: Message to display while loading
        
    Returns:
        A context manager for the loading spinner
    """
    return st.spinner(message)

def error_message(title: str, details: Optional[str] = None):
    """
    Display an error message.
    
    Args:
        title: Error title
        details: Optional error details
    """
    st.error(f"**{title}**")
    if details:
        st.error(details)

def success_message(message: str):
    """
    Display a success message.
    
    Args:
        message: Success message to display
    """
    st.success(message)

def stats_summary(
    total: int,
    keep: int,
    remove: int,
    processing_time: float
) -> None:
    """
    Display audit statistics summary.
    
    Args:
        total: Total followers processed
        keep: Number of followers to keep
        remove: Number of followers to remove
        processing_time: Total processing time in seconds
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Total Followers", total)
    with col2:
        metric_card("Keep", keep, format="%d")
    with col3:
        metric_card("Remove", remove, format="%d")
    with col4:
        metric_card("Processing Time", processing_time, format="%.1fs")

def engagement_chart(
    metrics: Dict[str, float],
    title: str = "Engagement Metrics"
) -> None:
    """
    Display an engagement metrics radar chart.
    
    Args:
        metrics: Dictionary of metric names and values
        title: Chart title
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(metrics.values()),
        theta=list(metrics.keys()),
        fill='toself',
        name='Engagement'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        title=title
    )
    
    st.plotly_chart(fig)

def recommendation_list(recommendations: List[str]) -> None:
    """
    Display a list of recommendations with icons.
    
    Args:
        recommendations: List of recommendation strings
    """
    for rec in recommendations:
        st.info(f"💡 {rec}")

def file_uploader(
    label: str,
    file_types: List[str],
    help_text: Optional[str] = None
) -> Optional[Any]:
    """
    Enhanced file uploader with help text and type validation.
    
    Args:
        label: Uploader label
        file_types: List of allowed file types
        help_text: Optional help text
        
    Returns:
        Uploaded file or None
    """
    return st.file_uploader(
        label,
        type=file_types,
        help=help_text
    ) 