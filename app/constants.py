"""
Constants and enums for the Instagram Follower Audit Tool.
This module contains predefined values used throughout the application.
"""

from enum import Enum
from typing import Dict, List, Set

class RiskLevel(Enum):
    """Risk level classification."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EngagementType(Enum):
    """Types of engagement metrics."""
    LIKES = "likes"
    COMMENTS = "comments"
    SHARES = "shares"
    SAVES = "saves"
    STORY_VIEWS = "story_views"
    DM_INTERACTIONS = "dm_interactions"

class EvaluationAction(str, Enum):
    """Possible actions for follower evaluation."""
    KEEP = "keep"
    REMOVE = "remove"
    MONITOR = "monitor"

# Risk level thresholds
RISK_THRESHOLDS = {
    RiskLevel.LOW: 0.3,
    RiskLevel.MEDIUM: 0.5,
    RiskLevel.HIGH: 0.7,
    RiskLevel.CRITICAL: 0.9
}

# Common pronouns for profile analysis
PRONOUNS: Set[str] = {
    "he/him", "she/her", "they/them", "he/they", "she/they",
    "they/he", "they/she", "it/its", "any/all", "other"
}

# Demographic keywords for bio analysis
DEMOGRAPHIC_KEYWORDS: Set[str] = {
    # Music-related
    "listener", "fan", "music", "concert", "gig", "tour", "album",
    "song", "artist", "musician", "band", "singer", "producer",
    
    # Age-related
    "student", "college", "university", "grad", "graduate",
    "professional", "working", "career", "business",
    
    # Interest-related
    "creative", "art", "design", "photography", "film",
    "tech", "technology", "digital", "online", "social",
    
    # Lifestyle
    "travel", "food", "fitness", "health", "wellness",
    "fashion", "style", "beauty", "lifestyle"
}

# Core Instagram accounts to monitor
CORE_ACCOUNTS: List[str] = [
    "instagram",
    "meta",
    "facebook",
    "threads"
]

# Evaluation thresholds
EVALUATION_THRESHOLDS = {
    "mass_following": 2000,  # Following count threshold
    "min_engagement": 0.3,   # Minimum engagement score
    "min_confidence": 0.7    # Minimum confidence for profile analysis
}

# Engagement score categories
ENGAGEMENT_CATEGORIES: Dict[str, float] = {
    "very_low": 0.2,
    "low": 0.4,
    "medium": 0.6,
    "high": 0.8,
    "very_high": 1.0
}

# Profile analysis categories
PROFILE_CATEGORIES = {
    "personal": "Personal account",
    "business": "Business account",
    "creator": "Creator account",
    "bot": "Automated account",
    "spam": "Spam account",
    "inactive": "Inactive account"
}

# Error messages
ERROR_MESSAGES = {
    "api_error": "Error connecting to Instagram API",
    "rate_limit": "Rate limit exceeded. Please try again later",
    "invalid_credentials": "Invalid API credentials",
    "network_error": "Network connection error",
    "timeout": "Request timed out"
}

# Success messages
SUCCESS_MESSAGES = {
    "analysis_complete": "Analysis completed successfully",
    "export_complete": "Results exported successfully",
    "settings_saved": "Settings saved successfully",
    "cache_cleared": "Cache cleared successfully"
}

# File extensions
FILE_EXTENSIONS = {
    "export": {
        "csv": ".csv",
        "json": ".json",
        "excel": ".xlsx"
    },
    "log": {
        "audit": ".log",
        "error": ".error.log"
    }
}

# Cache keys
CACHE_KEYS = {
    "follower_data": "follower_data_{}",
    "engagement_metrics": "engagement_metrics_{}",
    "analysis_results": "analysis_results_{}",
    "user_settings": "user_settings"
} 