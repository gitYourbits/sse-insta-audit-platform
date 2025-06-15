"""
Instagram Follower Audit Tool package.
"""

from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Version
__version__ = "0.1.0"

__author__ = "Your Name"
__email__ = "your.email@example.com"

from .config import APP_CONFIG
from .constants import (
    RiskLevel,
    EngagementType,
    RISK_THRESHOLDS,
    ENGAGEMENT_CATEGORIES
)

# Add the app directory to Python path
app_dir = Path(__file__).parent
sys.path.append(str(app_dir)) 