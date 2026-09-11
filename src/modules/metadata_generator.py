"""
Metadata Generator Module

Generates SEO-optimized metadata for YouTube videos:
- Titles
- Descriptions
- Tags
- Hashtags
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import openai
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE
from src.utils import get_logger, Validators

logger = get_logger(__name__)


class MetadataGenerator:
    """
    Generate YouTube metadata using AI.
    Optimizes for SEO and engagement.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize metadata generator.
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        openai.api_key = self.api_key
        self.model = OPENAI_MODEL

    def generate_title(
        self,
        topic: str,
        style: str = "informative",
        max_length: int = 60,
    ) -> Dict[str, Any]:
        """
        Generate SEO-optimized video title.
        
        Args:
            topic: Video topic
            style: Title style (clickbait, informative, question, etc.)
            max_length: Maximum title length
        
        Returns:
            Generated titles and metadata
        """
        logger.info(f"Generating titles for topic: {topic}")

        prompt = f"""Generate 5 compelling YouTube video titles about "{topic}". 
Each title should:
- Be {style} style
- Be maximum {max_length} characters
- Include relevant keywords
- Be clickable and engaging

Format as JSON list of objects with 'title' and 'notes' fields."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert YouTube SEO specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_TEMPERATURE,
            )

            titles = response.choices[0].message.content
            return {
                "topic": topic,
                "titles": titles,
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating titles: {e}")
            raise

    def generate_description(
        self,
        topic: str,
        script_excerpt: Optional[str] = None,
        max_length: int = 5000,
    ) -> Dict[str, Any]:
        """
        Generate SEO-optimized video description.
        
        Args:
            topic: Video topic
            script_excerpt: Excerpt from script
            max_length: Maximum description length
        
        Returns:
            Generated description
        """
        logger.info(f"Generating description for topic: {topic}")

        prompt = f"""Create a compelling YouTube video description for a video about "{topic}".

The description should:
- Be maximum {max_length} characters
- Include relevant keywords
- Have clear formatting with line breaks
- Include call-to-action
- Mention timestamps if applicable
- Include relevant links placeholder
{f'- Reference this content: {script_excerpt[:200]}...' if script_excerpt else ''}

Format with proper structure for YouTube."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a YouTube content strategist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_TEMPERATURE,
            )

            description = response.choices[0].message.content
            return {
                "topic": topic,
                "description": description,
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating description: {e}")
            raise

    def generate_tags(
        self,
        topic: str,
        max_tags: int = 30,
    ) -> Dict[str, Any]:
        """
        Generate relevant video tags.
        
        Args:
            topic: Video topic
            max_tags: Maximum number of tags
        
        Returns:
            Generated tags
        """
        logger.info(f"Generating tags for topic: {topic}")

        prompt = f"""Generate {max_tags} relevant YouTube tags for a video about "{topic}".

Tags should:
- Be relevant to the topic
- Include both broad and specific terms
- Include long-tail keywords
- Be practical for YouTube search

Return as JSON list of strings."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert in YouTube SEO and keywords."},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_TEMPERATURE,
            )

            tags_response = response.choices[0].message.content
            
            # Parse tags
            import json
            try:
                tags = json.loads(tags_response)
            except:
                tags = [tag.strip() for tag in tags_response.split(',')]
            
            # Validate and sanitize
            validated_tags = [tag for tag in tags if Validators.is_valid_tags([tag], max_tags=1)]

            return {
                "topic": topic,
                "tags": validated_tags[:max_tags],
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            raise

    def generate_hashtags(
        self,
        topic: str,
        max_hashtags: int = 10,
    ) -> Dict[str, Any]:
        """
        Generate trending hashtags for description/captions.
        
        Args:
            topic: Video topic
            max_hashtags: Maximum number of hashtags
        
        Returns:
            Generated hashtags
        """
        logger.info(f"Generating hashtags for topic: {topic}")

        prompt = f"""Generate {max_hashtags} trending hashtags for a video about "{topic}".

Hashtags should:
- Be relevant and trending
- Mix popular and niche hashtags
- Be properly formatted with #
- Be suitable for YouTube description

Return as JSON list of strings starting with #."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You understand YouTube trends and social media."},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_TEMPERATURE,
            )

            hashtags_response = response.choices[0].message.content
            
            # Parse hashtags
            import json
            try:
                hashtags = json.loads(hashtags_response)
            except:
                hashtags = [tag.strip() for tag in hashtags_response.split()]
            
            # Validate
            validated_hashtags = [
                tag for tag in hashtags 
                if Validators.is_valid_hashtag(tag)
            ]

            return {
                "topic": topic,
                "hashtags": validated_hashtags[:max_hashtags],
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating hashtags: {e}")
            raise

    def generate_all_metadata(
        self,
        topic: str,
        script_excerpt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate all metadata at once.
        
        Args:
            topic: Video topic
            script_excerpt: Script excerpt for description
        
        Returns:
            Complete metadata package
        """
        logger.info(f"Generating complete metadata for: {topic}")

        return {
            "topic": topic,
            "title": self.generate_title(topic),
            "description": self.generate_description(topic, script_excerpt),
            "tags": self.generate_tags(topic),
            "hashtags": self.generate_hashtags(topic),
            "generated_at": datetime.now().isoformat(),
        }
