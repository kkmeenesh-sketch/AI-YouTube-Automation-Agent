"""
Thumbnail Generator Module

Generates AI-powered YouTube thumbnails using DALL-E or other image generation services.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import openai
from config.settings import (
    OPENAI_API_KEY, DALL_E_MODEL, THUMBNAIL_SIZE,
    GENERATE_THUMBNAIL
)
from src.utils import get_logger, FileHandler

logger = get_logger(__name__)


class ThumbnailGenerator:
    """
    Generate YouTube thumbnails using AI image generation.
    Supports DALL-E and other providers.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = DALL_E_MODEL):
        """
        Initialize thumbnail generator.
        
        Args:
            api_key: OpenAI API key for DALL-E
            model: Model to use (dall-e-3, dall-e-2)
        """
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not configured for DALL-E")
        
        openai.api_key = self.api_key
        self.model = model
        self.size = THUMBNAIL_SIZE

    def generate_thumbnail(
        self,
        title: str,
        description: str,
        style: str = "bold",
        color_scheme: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a thumbnail for video.
        
        Args:
            title: Video title
            description: Video description
            style: Thumbnail style (bold, minimal, colorful, etc.)
            color_scheme: Color scheme preference
        
        Returns:
            Generated thumbnail metadata
        """
        if not GENERATE_THUMBNAIL:
            logger.info("Thumbnail generation disabled in settings")
            return {"status": "disabled", "generated_at": datetime.now().isoformat()}

        logger.info(f"Generating thumbnail for: {title}")

        prompt = self._build_prompt(title, description, style, color_scheme)

        try:
            response = openai.Image.create(
                model=self.model,
                prompt=prompt,
                n=1,
                size="1280x720",  # YouTube thumbnail standard
                quality="hd" if self.model == "dall-e-3" else "standard",
            )

            image_url = response.data[0].url

            return {
                "title": title,
                "image_url": image_url,
                "model": self.model,
                "style": style,
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating thumbnail: {e}")
            raise

    def download_thumbnail(
        self,
        image_url: str,
        output_path: Path,
    ) -> Path:
        """
        Download generated thumbnail image.
        
        Args:
            image_url: URL of generated image
            output_path: Path to save thumbnail
        
        Returns:
            Path to saved thumbnail
        """
        logger.info(f"Downloading thumbnail to {output_path}")

        try:
            import requests
            response = requests.get(image_url)
            response.raise_for_status()
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(response.content)
            logger.info(f"Thumbnail saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error downloading thumbnail: {e}")
            raise

    def _build_prompt(self, title: str, description: str, style: str, color_scheme: Optional[str]) -> str:
        """
        Build prompt for DALL-E thumbnail generation.
        
        Args:
            title: Video title
            description: Video description
            style: Thumbnail style
            color_scheme: Color scheme
        
        Returns:
            Prompt for DALL-E
        """
        style_descriptions = {
            "bold": "eye-catching with bold, vibrant colors",
            "minimal": "clean, minimal design with plenty of whitespace",
            "colorful": "bright, multi-colored design",
            "professional": "sleek, professional appearance",
            "playful": "fun, engaging, playful style",
        }

        style_desc = style_descriptions.get(style, "attractive")
        
        color_part = f" Color scheme: {color_scheme}." if color_scheme else ""

        prompt = f"""Create a YouTube thumbnail for a video about: {title}

Design requirements:
- Size: 1280x720 pixels (16:9 aspect ratio)
- Style: {style_desc}
- Must include: {title[:30]}... as prominent text
- Make it attention-grabbing and clickable
- Professional quality suitable for YouTube{color_part}
- Avoid copyright issues
- Clear, readable, high contrast

Description for context: {description[:100]}..."""

        return prompt
