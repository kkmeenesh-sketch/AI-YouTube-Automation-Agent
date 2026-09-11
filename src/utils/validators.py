"""
Input validation utilities for the automation agent.

Provides validation functions for various input types and parameters.
"""

import re
from typing import Any, List, Optional
from urllib.parse import urlparse
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Validators:
    """Input validation utilities."""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        """Validate YouTube URL."""
        youtube_patterns = [
            r'^https?://(?:www\.)?youtube\.com/watch\?v=',
            r'^https?://youtu\.be/',
            r'^https?://(?:www\.)?youtube\.com/@',
        ]
        return any(re.match(pattern, url) for pattern in youtube_patterns)
    
    @staticmethod
    def is_valid_youtube_channel_id(channel_id: str) -> bool:
        """Validate YouTube channel ID format (UC...)."""
        return bool(re.match(r'^UC[a-zA-Z0-9_-]{22}$', channel_id))
    
    @staticmethod
    def is_valid_video_title(title: str, min_length: int = 5, max_length: int = 100) -> bool:
        """Validate video title."""
        return isinstance(title, str) and min_length <= len(title) <= max_length
    
    @staticmethod
    def is_valid_description(description: str, max_length: int = 5000) -> bool:
        """Validate video description."""
        return isinstance(description, str) and len(description) <= max_length
    
    @staticmethod
    def is_valid_tags(tags: List[str], max_tags: int = 30, max_tag_length: int = 30) -> bool:
        """Validate video tags."""
        if not isinstance(tags, list) or len(tags) > max_tags:
            return False
        return all(isinstance(tag, str) and len(tag) <= max_tag_length for tag in tags)
    
    @staticmethod
    def is_valid_hashtag(hashtag: str) -> bool:
        """Validate hashtag format."""
        return bool(re.match(r'^#[a-zA-Z0-9_]+$', hashtag))
    
    @staticmethod
    def is_valid_iso_datetime(datetime_str: str) -> bool:
        """Validate ISO 8601 datetime format."""
        try:
            from datetime import datetime
            datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return True
        except (ValueError, AttributeError):
            return False
    
    @staticmethod
    def is_valid_privacy_status(status: str) -> bool:
        """Validate YouTube privacy status."""
        valid_statuses = ["public", "private", "unlisted"]
        return status.lower() in valid_statuses
    
    @staticmethod
    def is_valid_language_code(code: str) -> bool:
        """Validate language code format (e.g., en, es, fr)."""
        return bool(re.match(r'^[a-z]{2}(?:-[a-z]{2})?$', code.lower()))
    
    @staticmethod
    def validate_topic(topic: str, min_length: int = 3, max_length: int = 200) -> bool:
        """
        Validate topic for video creation.
        
        Args:
            topic: Video topic
            min_length: Minimum length
            max_length: Maximum length
        
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(topic, str):
            return False
        return min_length <= len(topic.strip()) <= max_length
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to remove invalid characters.
        
        Args:
            filename: Original filename
        
        Returns:
            Sanitized filename
        """
        # Remove invalid characters
        invalid_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(invalid_chars, '_', filename)
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(' .')
        # Limit length
        if len(sanitized) > 200:
            name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
            sanitized = name[:195] + ('.' + ext if ext else '')
        return sanitized
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate text to maximum length.
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add when truncated
        
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """
        Extract hashtags from text.
        
        Args:
            text: Text to extract from
        
        Returns:
            List of hashtags
        """
        hashtag_pattern = r'#\w+'
        return re.findall(hashtag_pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Extract URLs from text.
        
        Args:
            text: Text to extract from
        
        Returns:
            List of URLs
        """
        url_pattern = r'https?://[^\s]+'
        return re.findall(url_pattern, text)


# Validation error class
class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_or_raise(condition: bool, message: str) -> None:
    """
    Validate condition and raise ValidationError if False.
    
    Args:
        condition: Condition to validate
        message: Error message
    
    Raises:
        ValidationError: If condition is False
    """
    if not condition:
        raise ValidationError(message)
