"""
File handling utilities for video processing and management.

Provides functions for file operations, video handling, and cleanup.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List
from config.settings import TEMP_DIR, OUTPUT_DIR, DATA_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FileHandler:
    """Utility class for file operations."""
    
    @staticmethod
    def ensure_directory_exists(directory: Path) -> Path:
        """
        Ensure directory exists, create if not.
        
        Args:
            directory: Directory path
        
        Returns:
            Path object of the directory
        """
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {directory}")
        return directory
    
    @staticmethod
    def save_file(content: bytes, filepath: Path, overwrite: bool = False) -> Path:
        """
        Save content to a file.
        
        Args:
            content: File content
            filepath: Target file path
            overwrite: Whether to overwrite existing file
        
        Returns:
            Path to saved file
        
        Raises:
            FileExistsError: If file exists and overwrite is False
        """
        filepath = Path(filepath)
        
        if filepath.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {filepath}")
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(content)
        logger.info(f"File saved: {filepath}")
        return filepath
    
    @staticmethod
    def read_file(filepath: Path) -> bytes:
        """
        Read file content.
        
        Args:
            filepath: File path
        
        Returns:
            File content as bytes
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        return filepath.read_bytes()
    
    @staticmethod
    def delete_file(filepath: Path) -> bool:
        """
        Delete a file.
        
        Args:
            filepath: File path
        
        Returns:
            True if deleted, False if not found
        """
        filepath = Path(filepath)
        if filepath.exists():
            filepath.unlink()
            logger.info(f"File deleted: {filepath}")
            return True
        return False
    
    @staticmethod
    def delete_directory(directory: Path, recursive: bool = True) -> bool:
        """
        Delete a directory.
        
        Args:
            directory: Directory path
            recursive: Whether to delete recursively
        
        Returns:
            True if deleted, False if not found
        """
        directory = Path(directory)
        if directory.exists():
            if recursive:
                shutil.rmtree(directory)
            else:
                directory.rmdir()
            logger.info(f"Directory deleted: {directory}")
            return True
        return False
    
    @staticmethod
    def get_file_size(filepath: Path) -> int:
        """
        Get file size in bytes.
        
        Args:
            filepath: File path
        
        Returns:
            File size in bytes
        """
        filepath = Path(filepath)
        return filepath.stat().st_size if filepath.exists() else 0
    
    @staticmethod
    def move_file(source: Path, destination: Path) -> Path:
        """
        Move file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination path
        
        Returns:
            Path to moved file
        """
        source = Path(source)
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        logger.info(f"File moved: {source} -> {destination}")
        return destination
    
    @staticmethod
    def copy_file(source: Path, destination: Path) -> Path:
        """
        Copy file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination path
        
        Returns:
            Path to copied file
        """
        source = Path(source)
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source), str(destination))
        logger.info(f"File copied: {source} -> {destination}")
        return destination
    
    @staticmethod
    def list_files(directory: Path, pattern: str = "*") -> List[Path]:
        """
        List files in directory matching pattern.
        
        Args:
            directory: Directory path
            pattern: File pattern (e.g., "*.mp4")
        
        Returns:
            List of file paths
        """
        directory = Path(directory)
        if not directory.exists():
            return []
        return list(directory.glob(pattern))
    
    @staticmethod
    def cleanup_temp_files(max_age_days: int = 7) -> int:
        """
        Clean up temporary files older than specified days.
        
        Args:
            max_age_days: Maximum age in days
        
        Returns:
            Number of files deleted
        """
        import time
        deleted_count = 0
        now = time.time()
        max_age_seconds = max_age_days * 24 * 3600
        
        for file_path in TEMP_DIR.glob("**/*"):
            if file_path.is_file():
                file_age = now - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                    except Exception as e:
                        logger.warning(f"Failed to delete {file_path}: {e}")
        
        logger.info(f"Cleaned up {deleted_count} temporary files")
        return deleted_count


class VideoFileHandler(FileHandler):
    """Specialized handler for video files."""
    
    SUPPORTED_FORMATS = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    
    @staticmethod
    def is_video_file(filepath: Path) -> bool:
        """Check if file is a supported video format."""
        return Path(filepath).suffix.lower() in VideoFileHandler.SUPPORTED_FORMATS
    
    @staticmethod
    def get_video_duration(filepath: Path) -> Optional[float]:
        """
        Get video duration in seconds (requires ffmpeg).
        
        Args:
            filepath: Video file path
        
        Returns:
            Duration in seconds or None if unavailable
        """
        try:
            import ffmpeg
            probe = ffmpeg.probe(str(filepath))
            duration = float(probe["format"]["duration"])
            return duration
        except Exception as e:
            logger.warning(f"Failed to get video duration: {e}")
            return None
    
    @staticmethod
    def save_video(content: bytes, filename: str, output_dir: Path = OUTPUT_DIR) -> Path:
        """Save video file to output directory."""
        if not filename.lower().endswith(tuple(VideoFileHandler.SUPPORTED_FORMATS)):
            raise ValueError(f"Unsupported video format: {filename}")
        
        filepath = output_dir / filename
        return FileHandler.save_file(content, filepath, overwrite=True)
