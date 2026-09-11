"""
Script Generator Module

Uses OpenAI ChatGPT to research topics and generate engaging video scripts.
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime
import openai
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS
from src.utils import get_logger, Validators, ValidationError

logger = get_logger(__name__)


class ScriptGenerator:
    """Generate video scripts using OpenAI ChatGPT."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize ScriptGenerator.
        
        Args:
            api_key: OpenAI API key (defaults to env variable)
        """
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        openai.api_key = self.api_key
        self.model = OPENAI_MODEL
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens = OPENAI_MAX_TOKENS
    
    def generate_script(
        self,
        topic: str,
        duration_minutes: int = 5,
        style: str = "educational",
        target_audience: str = "general",
        language: str = "English",
        additional_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a video script for given topic.
        
        Args:
            topic: Video topic/title
            duration_minutes: Target video duration in minutes
            style: Video style (educational, entertaining, informative, etc.)
            target_audience: Target audience description
            language: Script language
            additional_context: Additional instructions for script generation
        
        Returns:
            Dictionary containing script and metadata
        
        Raises:
            ValidationError: If input validation fails
            openai.error.OpenAIError: If API call fails
        """
        
        # Validate input
        if not Validators.validate_topic(topic):
            raise ValidationError(f"Invalid topic: {topic}")
        
        if duration_minutes < 1 or duration_minutes > 120:
            raise ValidationError("Duration must be between 1 and 120 minutes")
        
        logger.info(f"Generating script for topic: {topic}")
        
        # Prepare prompt
        prompt = self._build_prompt(
            topic=topic,
            duration_minutes=duration_minutes,
            style=style,
            target_audience=target_audience,
            additional_context=additional_context,
        )
        
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert video scriptwriter. Create engaging, professional video scripts."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            # Extract script
            script_content = response.choices[0].message.content
            
            # Parse and structure the response
            result = {
                "topic": topic,
                "script": script_content,
                "duration_minutes": duration_minutes,
                "style": style,
                "target_audience": target_audience,
                "language": language,
                "model": self.model,
                "generated_at": datetime.now().isoformat(),
                "tokens_used": response.usage.total_tokens,
            }
            
            logger.info(f"Script generated successfully (tokens: {response.usage.total_tokens})")
            return result
        
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in script generation: {e}")
            raise
    
    def enhance_script(
        self,
        script: str,
        enhancement_type: str = "seo",
        additional_instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Enhance existing script with SEO, engagement, or other improvements.
        
        Args:
            script: Original script text
            enhancement_type: Type of enhancement (seo, engagement, brevity, detail, etc.)
            additional_instructions: Additional enhancement instructions
        
        Returns:
            Enhanced script with metadata
        """
        logger.info(f"Enhancing script with {enhancement_type} optimization")
        
        enhancement_prompts = {
            "seo": "Enhance this video script for SEO. Add keywords, improve search visibility, and optimize for YouTube algorithm.",
            "engagement": "Make this script more engaging and entertaining. Add hooks, questions, and call-to-actions.",
            "brevity": "Make this script more concise and to-the-point while maintaining key information.",
            "detail": "Expand this script with more detailed information and examples.",
            "accessibility": "Make this script more accessible and easier to understand for a general audience.",
        }
        
        base_instruction = enhancement_prompts.get(enhancement_type, "Improve this script.")
        
        prompt = f"""{base_instruction}

Script to enhance:
{script}

{additional_instructions or ''}

Provide the enhanced script."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at enhancing video scripts."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            enhanced_script = response.choices[0].message.content
            
            return {
                "original_script": script,
                "enhanced_script": enhanced_script,
                "enhancement_type": enhancement_type,
                "generated_at": datetime.now().isoformat(),
                "tokens_used": response.usage.total_tokens,
            }
        
        except Exception as e:
            logger.error(f"Error enhancing script: {e}")
            raise
    
    def generate_script_sections(
        self,
        topic: str,
        num_sections: int = 5,
    ) -> Dict[str, Any]:
        """
        Generate script broken down into specific sections.
        
        Args:
            topic: Video topic
            num_sections: Number of sections
        
        Returns:
            Script with sections
        """
        prompt = f"""Create a video script about "{topic}" divided into {num_sections} clear sections.

Format as JSON with this structure:
{{
  "title": "Video Title",
  "intro": "Opening section",
  "sections": [
    {{"title": "Section 1", "content": "..."}},
    ...
  ],
  "conclusion": "Closing remarks",
  "call_to_action": "CTA for viewers"
}}

Make each section engaging and informative."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating structured video scripts."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON
            try:
                structured_script = json.loads(content)
            except json.JSONDecodeError:
                # If JSON parsing fails, return as-is
                structured_script = {"raw_content": content}
            
            return {
                "topic": topic,
                "script": structured_script,
                "generated_at": datetime.now().isoformat(),
                "tokens_used": response.usage.total_tokens,
            }
        
        except Exception as e:
            logger.error(f"Error generating sectioned script: {e}")
            raise
    
    def _build_prompt(
        self,
        topic: str,
        duration_minutes: int,
        style: str,
        target_audience: str,
        additional_context: Optional[str],
    ) -> str:
        """Build the prompt for script generation."""
        
        words_estimate = duration_minutes * 150  # Approximate words per minute
        
        prompt = f"""Generate a professional video script about: "{topic}"

Requirements:
- Duration: approximately {duration_minutes} minutes ({words_estimate} words)
- Style: {style}
- Target Audience: {target_audience}
- Language: English

The script should include:
1. An engaging hook/introduction (first 10-15 seconds)
2. Clear main content sections with logical flow
3. Key points highlighted
4. Call-to-action at the end
5. Natural speaking voice suitable for video narration

Format:
- Use clear section headers
- Include timing cues (e.g., [0:00-0:30])
- Mark important pauses
- Suggest visual cues where relevant

{f'Additional requirements: {additional_context}' if additional_context else ''}

Generate the complete script:"""
        
        return prompt
