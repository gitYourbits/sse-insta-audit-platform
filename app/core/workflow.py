"""
Workflow controller for the Instagram Follower Audit Tool.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging
import asyncio
from datetime import datetime
import json
import os
from pathlib import Path

from app.core.engagement import EngagementChecker, EngagementResult
from app.core.profile import ProfileAnalyzer, ProfileResult
from app.core.logger import AuditLogger
from app.constants import (
    EvaluationAction,
    PRONOUNS,
    DEMOGRAPHIC_KEYWORDS,
    EVALUATION_THRESHOLDS
)

@dataclass
class AuditResult:
    """Data class for storing audit results."""
    username: str
    action: str
    reason: str
    engagement_score: float
    risk_score: float
    recommendations: List[str]

class WorkflowController:
    """Controls the workflow for auditing Instagram followers."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the workflow controller.
        
        Args:
            api_key: Optional OpenAI API key for profile analysis
        """
        self.engagement_checker = EngagementChecker()
        self.profile_analyzer = ProfileAnalyzer(api_key)
        self.logger = AuditLogger()
    
    async def audit_follower(self, follower_data: Dict[str, Any]) -> Dict[str, Any]:
        """Audit a single follower's data.
        
        Args:
            follower_data: Dictionary containing follower data
            
        Returns:
            Dictionary containing audit results
        """
        username = follower_data.get("username", "Unknown")
        
        try:
            # Get engagement score
            engagement_result = await self.engagement_checker.check_engagement(follower_data)
            engagement_score = engagement_result.score
            
            # Analyze profile
            profile_result = await self.profile_analyzer.analyze_profile(follower_data)
            risk_score = profile_result.risk_score
            
            # Determine action based on scores
            action = self._determine_action(engagement_score, risk_score)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                engagement_score,
                risk_score,
                profile_result.analysis
            )
            
            # Log the result
            self.logger.log_audit(
                username=username,
                engagement_score=engagement_score,
                risk_score=risk_score,
                action=action.value,
                reason=profile_result.analysis
            )
            
            return {
                "username": username,
                "engagement_score": engagement_score,
                "risk_score": risk_score,
                "action": action.value,
                "reason": profile_result.analysis,
                "recommendations": recommendations
            }
            
        except Exception as e:
            self.logger.log_error(username, str(e))
            raise
    
    def _determine_action(self, engagement_score: float, risk_score: float) -> EvaluationAction:
        """Determine the action to take based on scores.
        
        Args:
            engagement_score: Engagement score (0-1)
            risk_score: Risk score (0-1)
            
        Returns:
            Action to take
        """
        if engagement_score >= 0.7 and risk_score <= 0.3:
            return EvaluationAction.KEEP
        elif engagement_score >= 0.5 and risk_score <= 0.5:
            return EvaluationAction.MONITOR
        elif engagement_score <= 0.3 or risk_score >= 0.7:
            return EvaluationAction.REMOVE
        else:
            return EvaluationAction.MONITOR
    
    def _generate_recommendations(
        self,
        engagement_score: float,
        risk_score: float,
        analysis: str
    ) -> List[str]:
        """Generate recommendations based on scores and analysis.
        
        Args:
            engagement_score: Engagement score (0-1)
            risk_score: Risk score (0-1)
            analysis: Profile analysis text
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if engagement_score < 0.5:
            recommendations.append("Low engagement - Consider removing if no improvement")
        
        if risk_score > 0.5:
            recommendations.append("High risk - Monitor closely or remove")
            
        if "private" in analysis.lower():
            recommendations.append("Private account - Consider impact on engagement")
            
        if "inactive" in analysis.lower():
            recommendations.append("Inactive account - May be safe to remove")
            
        return recommendations 