"""
Core functionality for the Instagram Follower Audit Tool.
"""

from .workflow import WorkflowController, AuditResult
from .analyzer import ProfileAnalyzer, ProfileMetrics
from .engagement import EngagementChecker, EngagementResult
from .logger import AuditLogger

__all__ = [
    'WorkflowController',
    'AuditResult',
    'ProfileAnalyzer',
    'ProfileMetrics',
    'EngagementChecker',
    'EngagementResult',
    'AuditLogger'
] 