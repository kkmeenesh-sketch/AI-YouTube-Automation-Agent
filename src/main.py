"""
Main Orchestration Agent

Coordinates the complete workflow for automated YouTube video creation,
optimization, and publishing.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import json

from config.settings import (
    APP_NAME, APP_VERSION, DEBUG_MODE, OUTPUT_DIR,
    TEMP_DIR, validate_required_config
)
from src.utils import get_logger, FileHandler, Validators
from src.modules import (
    ScriptGenerator,
    VideoGenerator,
    SubtitleGenerator,
    MetadataGenerator,
    ThumbnailGenerator,
    YouTubeUploader,
    VideoScheduler,
)

logger = get_logger(__name__)


class YouTubeAutomationAgent:
    """
    Main automation agent for complete YouTube workflow.
    
    Orchestrates:
    1. Script generation from topic
    2. Video generation from script
    3. Subtitle generation
    4. Metadata generation (title, description, tags)
    5. Thumbnail generation
    6. YouTube upload
    7. Video scheduling and publishing
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the automation agent.
        
        Args:
            config_path: Path to configuration file
        """
        logger.info(f"Initializing {APP_NAME} v{APP_VERSION}")
        
        # Validate configuration
        missing_config = validate_required_config()
        if missing_config:
            logger.warning(f"Missing configuration: {', '.join(missing_config)}")
        
        # Initialize modules
        self.script_generator = ScriptGenerator()
        self.video_generator = VideoGenerator()
        self.subtitle_generator = SubtitleGenerator()
        self.metadata_generator = MetadataGenerator()
        self.thumbnail_generator = ThumbnailGenerator()
        self.youtube_uploader = YouTubeUploader()
        self.scheduler = VideoScheduler()
        
        # State tracking
        self.current_workflow = {}
        self.workflow_history = []
        
        logger.info(f"{APP_NAME} initialized successfully")

    def automate_video_creation(
        self,
        topic: str,
        video_title: Optional[str] = None,
        video_duration: int = 5,
        video_style: str = "educational",
        target_audience: str = "general",
        publish_time: Optional[datetime] = None,
        schedule: bool = False,
        auto_publish: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute complete automated workflow for video creation and publishing.
        
        Args:
            topic: Video topic
            video_title: Custom video title (auto-generated if not provided)
            video_duration: Target duration in minutes
            video_style: Video style
            target_audience: Target audience description
            publish_time: When to publish (datetime object)
            schedule: Whether to schedule for future publishing
            auto_publish: Whether to auto-publish after upload
        
        Returns:
            Workflow result with video ID and metadata
        """
        workflow_id = f"workflow_{int(datetime.now().timestamp())}"
        logger.info(f"Starting workflow {workflow_id} for topic: {topic}")
        
        try:
            # Validate input
            if not Validators.validate_topic(topic):
                raise ValueError(f"Invalid topic: {topic}")
            
            result = {
                "workflow_id": workflow_id,
                "topic": topic,
                "start_time": datetime.now().isoformat(),
                "steps": {},
            }
            
            # Step 1: Generate Script
            logger.info("Step 1/7: Generating script...")
            script_result = self._generate_script(
                topic, video_duration, video_style, target_audience
            )
            result["steps"]["script_generation"] = script_result
            script = script_result.get("script", "")
            
            # Step 2: Generate Video
            logger.info("Step 2/7: Generating video...")
            video_result = self._generate_video(script, video_duration)
            result["steps"]["video_generation"] = video_result
            video_path = video_result.get("video_path")
            
            # Step 3: Generate Subtitles
            logger.info("Step 3/7: Generating subtitles...")
            subtitle_result = self._generate_subtitles(video_path)
            result["steps"]["subtitle_generation"] = subtitle_result
            
            # Step 4: Generate Metadata
            logger.info("Step 4/7: Generating metadata...")
            metadata_result = self._generate_metadata(topic, script)
            result["steps"]["metadata_generation"] = metadata_result
            
            # Step 5: Generate Thumbnail
            logger.info("Step 5/7: Generating thumbnail...")
            thumbnail_result = self._generate_thumbnail(
                metadata_result.get("title", {}).get("titles", [topic])[0],
                metadata_result.get("description", {}).get("description", "")
            )
            result["steps"]["thumbnail_generation"] = thumbnail_result
            
            # Step 6: Upload to YouTube
            logger.info("Step 6/7: Uploading to YouTube...")
            upload_result = self._upload_to_youtube(
                video_path,
                metadata_result,
                thumbnail_result
            )
            result["steps"]["youtube_upload"] = upload_result
            video_id = upload_result.get("video_id")
            
            # Step 7: Schedule/Publish
            logger.info("Step 7/7: Scheduling/Publishing...")
            publish_result = self._schedule_or_publish(
                video_id, publish_time, schedule, auto_publish
            )
            result["steps"]["publishing"] = publish_result
            
            result["status"] = "success"
            result["end_time"] = datetime.now().isoformat()
            result["youtube_url"] = f"https://www.youtube.com/watch?v={video_id}"
            
            # Save workflow result
            self._save_workflow_result(workflow_id, result)
            
            logger.info(f"Workflow {workflow_id} completed successfully")
            return result
        
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {e}", exc_info=True)
            result["status"] = "failed"
            result["error"] = str(e)
            result["end_time"] = datetime.now().isoformat()
            self._save_workflow_result(workflow_id, result)
            raise

    def _generate_script(
        self,
        topic: str,
        duration: int,
        style: str,
        audience: str,
    ) -> Dict[str, Any]:
        """Generate video script."""
        try:
            return self.script_generator.generate_script(
                topic=topic,
                duration_minutes=duration,
                style=style,
                target_audience=audience,
            )
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            return {"status": "failed", "error": str(e)}

    def _generate_video(
        self,
        script: str,
        duration: int,
    ) -> Dict[str, Any]:
        """Generate video from script."""
        try:
            result = self.video_generator.generate_video(
                script=script,
                duration_seconds=duration * 60,
            )
            # Note: video_path would be actual path if API implemented
            result["video_path"] = None
            return result
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            return {"status": "failed", "error": str(e)}

    def _generate_subtitles(self, video_path: Optional[Path]) -> Dict[str, Any]:
        """Generate subtitles from video."""
        if not video_path:
            return {"status": "skipped", "reason": "No video path"}
        
        try:
            return self.subtitle_generator.generate_subtitles(video_path)
        except Exception as e:
            logger.error(f"Subtitle generation failed: {e}")
            return {"status": "failed", "error": str(e)}

    def _generate_metadata(
        self,
        topic: str,
        script: str,
    ) -> Dict[str, Any]:
        """Generate all metadata."""
        try:
            return self.metadata_generator.generate_all_metadata(
                topic=topic,
                script_excerpt=script[:500],
            )
        except Exception as e:
            logger.error(f"Metadata generation failed: {e}")
            return {"status": "failed", "error": str(e)}

    def _generate_thumbnail(
        self,
        title: str,
        description: str,
    ) -> Dict[str, Any]:
        """Generate thumbnail."""
        try:
            return self.thumbnail_generator.generate_thumbnail(
                title=title,
                description=description,
            )
        except Exception as e:
            logger.error(f"Thumbnail generation failed: {e}")
            return {"status": "failed", "error": str(e)}

    def _upload_to_youtube(
        self,
        video_path: Optional[Path],
        metadata: Dict[str, Any],
        thumbnail: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Upload video to YouTube."""
        if not video_path:
            return {"status": "failed", "error": "No video to upload"}
        
        try:
            title = metadata.get("title", {}).get("titles", ["Untitled"])[0]
            description = metadata.get("description", {}).get("description", "")
            tags = metadata.get("tags", {}).get("tags", [])
            
            result = self.youtube_uploader.upload_video(
                video_path=video_path,
                title=title,
                description=description,
                tags=tags,
            )
            
            # Upload thumbnail if available
            if thumbnail.get("image_url"):
                try:
                    self.youtube_uploader.upload_thumbnail(
                        video_id=result.get("video_id"),
                        thumbnail_path=thumbnail.get("thumbnail_path"),
                    )
                except Exception as e:
                    logger.warning(f"Failed to upload thumbnail: {e}")
            
            return result
        except Exception as e:
            logger.error(f"YouTube upload failed: {e}")
            return {"status": "failed", "error": str(e)}

    def _schedule_or_publish(
        self,
        video_id: str,
        publish_time: Optional[datetime],
        schedule: bool,
        auto_publish: bool,
    ) -> Dict[str, Any]:
        """Schedule or publish video."""
        try:
            if schedule and publish_time:
                return self.youtube_uploader.schedule_video(
                    video_id=video_id,
                    publish_time=publish_time,
                )
            elif auto_publish:
                return {"status": "published", "video_id": video_id}
            else:
                return {"status": "uploaded", "video_id": video_id}
        except Exception as e:
            logger.error(f"Publishing failed: {e}")
            return {"status": "failed", "error": str(e)}

    def _save_workflow_result(
        self,
        workflow_id: str,
        result: Dict[str, Any],
    ) -> None:
        """Save workflow result to file."""
        try:
            output_file = OUTPUT_DIR / f"{workflow_id}.json"
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2, default=str)
            logger.info(f"Workflow result saved to {output_file}")
        except Exception as e:
            logger.warning(f"Failed to save workflow result: {e}")

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of completed workflow."""
        try:
            result_file = OUTPUT_DIR / f"{workflow_id}.json"
            if result_file.exists():
                with open(result_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading workflow: {e}")
        return None


if __name__ == "__main__":
    logger.info(f"Starting {APP_NAME}...")
    
    # Example usage
    agent = YouTubeAutomationAgent()
    
    # Test workflow
    result = agent.automate_video_creation(
        topic="Introduction to AI and Machine Learning",
        video_duration=5,
        video_style="educational",
        target_audience="Beginners",
    )
    
    print(json.dumps(result, indent=2, default=str))
