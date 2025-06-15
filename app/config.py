"""
Configuration settings for the Instagram Follower Audit Tool.
This module contains all configurable parameters and feature toggles.
"""

from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class AppConfig:
    """Application configuration settings."""
    
    # API Settings
    API_TIMEOUT: int = 30
    API_RETRY_ATTEMPTS: int = 3
    API_RETRY_DELAY: float = 1.0
    
    # Analysis Thresholds
    ENGAGEMENT_THRESHOLD: float = 0.3
    RISK_THRESHOLD: float = 0.7
    BATCH_SIZE: int = 10
    
    # Feature Toggles
    ENABLE_AI_ANALYSIS: bool = True
    ENABLE_BATCH_PROCESSING: bool = True
    ENABLE_DETAILED_LOGGING: bool = True
    
    # UI Settings
    REFRESH_INTERVAL: int = 60  # seconds
    MAX_DISPLAY_ITEMS: int = 100
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # File Paths
    LOG_DIR: str = "logs"
    CACHE_DIR: str = "cache"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

# Create global configuration instance
APP_CONFIG = AppConfig()

# Feature flags
FEATURES = {
    "ai_analysis": True,
    "batch_processing": True,
    "detailed_logging": True,
    "export_results": True,
    "real_time_updates": False
}

# Analysis weights
ANALYSIS_WEIGHTS = {
    "engagement": {
        "likes": 0.3,
        "comments": 0.25,
        "shares": 0.15,
        "saves": 0.1,
        "story_views": 0.1,
        "dm_interactions": 0.1
    },
    "risk": {
        "activity": 0.3,
        "content": 0.3,
        "interaction": 0.2,
        "age": 0.2
    }
}

# UI Theme
UI_THEME = {
    "primary_color": "#1DA1F2",
    "secondary_color": "#657786",
    "background_color": "#FFFFFF",
    "text_color": "#14171A",
    "success_color": "#17BF63",
    "warning_color": "#F45D22",
    "error_color": "#E0245E"
} 