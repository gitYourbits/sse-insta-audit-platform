"""
Logging functionality for the Instagram Follower Audit Tool.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import json

class AuditLogger:
    """Handles logging of audit operations."""
    
    def __init__(self):
        """Initialize the audit logger."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Set up file handler
        log_file = self.logs_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_audit(
        self,
        username: str,
        engagement_score: float,
        risk_score: float,
        action: str,
        reason: Optional[str] = None
    ):
        """Log an audit result.
        
        Args:
            username: Username of the follower
            engagement_score: Calculated engagement score
            risk_score: Calculated risk score
            action: Action taken (keep/remove/monitor)
            reason: Optional reason for the action
        """
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "engagement_score": engagement_score,
            "risk_score": risk_score,
            "action": action,
            "reason": reason
        }
        
        self.logger.info(f"Audit result for {username}: {json.dumps(log_data)}")
    
    def log_error(self, username: str, error: str):
        """Log an error.
        
        Args:
            username: Username of the follower
            error: Error message
        """
        self.logger.error(f"{username} - Error: {error}")
    
    @classmethod
    def get_latest_log(cls) -> Optional[str]:
        """
        Get the path to the latest log file.
        
        Returns:
            Path to the latest log file or None if no logs exist
        """
        logs_dir = Path("logs")
        if not logs_dir.exists():
            return None
            
        log_files = list(logs_dir.glob("audit_*.log"))
        if not log_files:
            return None
            
        return str(max(log_files, key=lambda x: x.stat().st_mtime))

    def _save_detailed_result(self, result: Dict[str, Any]) -> None:
        """Save detailed audit result to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = self.logs_dir / f'audit_result_{timestamp}.json'
        
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2) 