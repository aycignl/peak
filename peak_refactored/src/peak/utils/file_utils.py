"""File utilities for PEAK."""

import json
import pickle
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import joblib
import pandas as pd

from peak.config.logging_config import get_logger

logger = get_logger(__name__)


class FileUtils:
    """File utilities for PEAK operations."""
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> Path:
        """
        Ensure directory exists, create if necessary.
        
        Args:
            path: Directory path
            
        Returns:
            Path object
        """
        path_obj = Path(path)
        path_obj.mkdir(parents=True, exist_ok=True)
        logger.info("Directory ensured", path=str(path_obj))
        return path_obj
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
        """
        Save data as JSON file.
        
        Args:
            data: Data to save
            file_path: Output file path
        """
        file_path = Path(file_path)
        FileUtils.ensure_directory(file_path.parent)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info("JSON file saved", path=str(file_path))
    
    @staticmethod
    def load_json(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load data from JSON file.
        
        Args:
            file_path: Input file path
            
        Returns:
            Loaded data
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        logger.info("JSON file loaded", path=str(file_path))
        return data
    
    @staticmethod
    def save_pickle(obj: Any, file_path: Union[str, Path]) -> None:
        """
        Save object as pickle file.
        
        Args:
            obj: Object to save
            file_path: Output file path
        """
        file_path = Path(file_path)
        FileUtils.ensure_directory(file_path.parent)
        
        with open(file_path, 'wb') as f:
            pickle.dump(obj, f)
        
        logger.info("Pickle file saved", path=str(file_path))
    
    @staticmethod
    def load_pickle(file_path: Union[str, Path]) -> Any:
        """
        Load object from pickle file.
        
        Args:
            file_path: Input file path
            
        Returns:
            Loaded object
        """
        with open(file_path, 'rb') as f:
            obj = pickle.load(f)
        
        logger.info("Pickle file loaded", path=str(file_path))
        return obj
    
    @staticmethod
    def save_joblib(obj: Any, file_path: Union[str, Path]) -> None:
        """
        Save object using joblib.
        
        Args:
            obj: Object to save
            file_path: Output file path
        """
        file_path = Path(file_path)
        FileUtils.ensure_directory(file_path.parent)
        
        joblib.dump(obj, file_path)
        logger.info("Joblib file saved", path=str(file_path))
    
    @staticmethod
    def load_joblib(file_path: Union[str, Path]) -> Any:
        """
        Load object using joblib.
        
        Args:
            file_path: Input file path
            
        Returns:
            Loaded object
        """
        obj = joblib.load(file_path)
        logger.info("Joblib file loaded", path=str(file_path))
        return obj
    
    @staticmethod
    def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        Copy file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        src_path = Path(src)
        dst_path = Path(dst)
        
        FileUtils.ensure_directory(dst_path.parent)
        shutil.copy2(src_path, dst_path)
        
        logger.info("File copied", src=str(src_path), dst=str(dst_path))
    
    @staticmethod
    def list_files(
        directory: Union[str, Path], 
        pattern: str = "*",
        recursive: bool = False
    ) -> List[Path]:
        """
        List files in directory.
        
        Args:
            directory: Directory to search
            pattern: File pattern to match
            recursive: Whether to search recursively
            
        Returns:
            List of file paths
        """
        dir_path = Path(directory)
        
        if recursive:
            files = list(dir_path.rglob(pattern))
        else:
            files = list(dir_path.glob(pattern))
        
        # Filter to files only
        files = [f for f in files if f.is_file()]
        
        logger.info("Files listed", 
                   directory=str(dir_path),
                   pattern=pattern,
                   count=len(files))
        
        return files
    
    @staticmethod
    def get_file_size(file_path: Union[str, Path]) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: File path
            
        Returns:
            File size in bytes
        """
        path_obj = Path(file_path)
        size = path_obj.stat().st_size
        
        logger.info("File size retrieved", 
                   path=str(path_obj),
                   size_bytes=size,
                   size_mb=size / 1024 / 1024)
        
        return size
    
    @staticmethod
    def backup_file(file_path: Union[str, Path], backup_suffix: str = ".bak") -> Path:
        """
        Create backup of file.
        
        Args:
            file_path: File to backup
            backup_suffix: Suffix for backup file
            
        Returns:
            Path to backup file
        """
        src_path = Path(file_path)
        backup_path = src_path.with_suffix(src_path.suffix + backup_suffix)
        
        if src_path.exists():
            FileUtils.copy_file(src_path, backup_path)
            logger.info("File backed up", 
                       original=str(src_path),
                       backup=str(backup_path))
        
        return backup_path
    
    @staticmethod
    def clean_directory(
        directory: Union[str, Path],
        pattern: str = "*",
        dry_run: bool = True
    ) -> List[Path]:
        """
        Clean files from directory.
        
        Args:
            directory: Directory to clean
            pattern: Pattern of files to delete
            dry_run: If True, only list files that would be deleted
            
        Returns:
            List of files that were (or would be) deleted
        """
        files = FileUtils.list_files(directory, pattern)
        
        if dry_run:
            logger.info("Dry run - files that would be deleted", count=len(files))
            for file_path in files:
                logger.info("Would delete", path=str(file_path))
        else:
            for file_path in files:
                file_path.unlink()
                logger.info("File deleted", path=str(file_path))
        
        return files