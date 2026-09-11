"""
Database manager for workflow persistence.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import json
from config.settings import DATA_DIR
from src.utils import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """
    Manages workflow data persistence.
    Currently uses JSON files; can be extended to use SQLite/PostgreSQL.
    """

    def __init__(self, data_dir: Path = DATA_DIR):
        """
        Initialize database manager.
        
        Args:
            data_dir: Directory for data storage
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.workflows_file = self.data_dir / "workflows.json"
        self._ensure_workflows_file()

    def _ensure_workflows_file(self) -> None:
        """Ensure workflows file exists."""
        if not self.workflows_file.exists():
            self.workflows_file.write_text(json.dumps({"workflows": []}))

    def save_workflow(
        self,
        workflow_id: str,
        workflow_data: Dict[str, Any],
    ) -> bool:
        """
        Save workflow data.
        
        Args:
            workflow_id: Unique workflow identifier
            workflow_data: Workflow data dictionary
        
        Returns:
            True if successful
        """
        try:
            with open(self.workflows_file, "r") as f:
                data = json.load(f)
            
            data["workflows"].append({
                "id": workflow_id,
                "data": workflow_data,
                "saved_at": datetime.now().isoformat(),
            })
            
            with open(self.workflows_file, "w") as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Workflow {workflow_id} saved")
            return True
        except Exception as e:
            logger.error(f"Error saving workflow: {e}")
            return False

    def get_workflow(
        self,
        workflow_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve workflow data.
        
        Args:
            workflow_id: Workflow identifier
        
        Returns:
            Workflow data or None
        """
        try:
            with open(self.workflows_file, "r") as f:
                data = json.load(f)
            
            for item in data.get("workflows", []):
                if item["id"] == workflow_id:
                    return item["data"]
        except Exception as e:
            logger.error(f"Error retrieving workflow: {e}")
        
        return None

    def list_workflows(
        self,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List all workflows.
        
        Args:
            limit: Maximum number of workflows to return
        
        Returns:
            List of workflows
        """
        try:
            with open(self.workflows_file, "r") as f:
                data = json.load(f)
            
            return data.get("workflows", [])[:limit]
        except Exception as e:
            logger.error(f"Error listing workflows: {e}")
            return []
