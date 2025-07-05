"""Base pipeline class for PEAK."""

import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from peak.config.logging_config import get_logger

logger = get_logger(__name__)


class PipelineError(Exception):
    """Custom exception for pipeline errors."""
    pass


class BasePipeline(ABC):
    """Abstract base class for PEAK pipelines."""
    
    def __init__(self, name: str, checkpoint_dir: Optional[Union[str, Path]] = None):
        """
        Initialize base pipeline.
        
        Args:
            name: Pipeline name for logging and checkpoints
            checkpoint_dir: Directory to save checkpoints
        """
        self.name = name
        self.checkpoint_dir = Path(checkpoint_dir) if checkpoint_dir else None
        self.steps_completed = []
        self.start_time = None
        self.end_time = None
        
        if self.checkpoint_dir:
            self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Pipeline initialized", pipeline_name=self.name)
    
    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Run the pipeline.
        
        Returns:
            Dictionary with pipeline results
        """
        pass
    
    def start(self) -> None:
        """Start pipeline execution."""
        self.start_time = time.time()
        logger.info("Pipeline started", pipeline_name=self.name)
    
    def finish(self) -> None:
        """Finish pipeline execution."""
        self.end_time = time.time()
        duration = self.end_time - self.start_time if self.start_time else 0
        logger.info("Pipeline completed", 
                   pipeline_name=self.name,
                   duration_seconds=duration,
                   steps_completed=len(self.steps_completed))
    
    def add_step(self, step_name: str) -> None:
        """
        Mark a step as completed.
        
        Args:
            step_name: Name of the completed step
        """
        self.steps_completed.append(step_name)
        logger.info("Pipeline step completed", 
                   pipeline_name=self.name,
                   step_name=step_name,
                   total_steps=len(self.steps_completed))
    
    def save_checkpoint(self, data: Dict[str, Any], checkpoint_name: str) -> None:
        """
        Save a checkpoint of pipeline state.
        
        Args:
            data: Data to checkpoint
            checkpoint_name: Name of the checkpoint
        """
        if not self.checkpoint_dir:
            logger.warning("No checkpoint directory configured")
            return
        
        import joblib
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_name}.pkl"
        
        try:
            joblib.dump(data, checkpoint_path)
            logger.info("Checkpoint saved", 
                       checkpoint_name=checkpoint_name,
                       checkpoint_path=str(checkpoint_path))
        except Exception as e:
            logger.error("Failed to save checkpoint", 
                        checkpoint_name=checkpoint_name,
                        error=str(e))
    
    def load_checkpoint(self, checkpoint_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a checkpoint.
        
        Args:
            checkpoint_name: Name of the checkpoint to load
            
        Returns:
            Loaded checkpoint data or None if not found
        """
        if not self.checkpoint_dir:
            logger.warning("No checkpoint directory configured")
            return None
        
        import joblib
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_name}.pkl"
        
        if not checkpoint_path.exists():
            logger.info("Checkpoint not found", checkpoint_name=checkpoint_name)
            return None
        
        try:
            data = joblib.load(checkpoint_path)
            logger.info("Checkpoint loaded", checkpoint_name=checkpoint_name)
            return data
        except Exception as e:
            logger.error("Failed to load checkpoint", 
                        checkpoint_name=checkpoint_name,
                        error=str(e))
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current pipeline status.
        
        Returns:
            Dictionary with pipeline status information
        """
        status = {
            "name": self.name,
            "steps_completed": self.steps_completed,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_running": self.start_time is not None and self.end_time is None,
            "duration": None
        }
        
        if self.start_time and self.end_time:
            status["duration"] = self.end_time - self.start_time
        elif self.start_time:
            status["duration"] = time.time() - self.start_time
            
        return status