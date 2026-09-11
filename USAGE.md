# Usage Guide

Detailed usage instructions for the AI YouTube Automation Agent.

## Quick Start

### Basic Usage

```python
from src.main import YouTubeAutomationAgent
from datetime import datetime, timedelta

# Initialize agent
agent = YouTubeAutomationAgent()

# Create and publish video
result = agent.automate_video_creation(
    topic="Your Video Topic Here",
    video_duration=5,  # minutes
    video_style="educational",
    target_audience="General audience",
    auto_publish=True
)

print(f"Video published: {result['youtube_url']}")
```

## Workflow Steps

The agent executes these steps automatically:

1. **Script Generation** - Uses ChatGPT to create engaging script
2. **Video Generation** - Generates video from script
3. **Subtitle Generation** - Creates automated captions
4. **Metadata Generation** - Generates SEO-optimized:
   - Titles (5 options)
   - Descriptions
   - Tags
   - Hashtags
5. **Thumbnail Generation** - AI-generated thumbnail (optional)
6. **YouTube Upload** - Uploads to your channel
7. **Publishing** - Schedules or publishes immediately

## Advanced Options

### Schedule for Future Publishing

```python
from datetime import datetime, timedelta

# Schedule for tomorrow at 2 PM
publish_time = datetime.now() + timedelta(days=1, hours=14)

result = agent.automate_video_creation(
    topic="AI Trends 2025",
    video_duration=8,
    publish_time=publish_time,
    schedule=True  # Schedule instead of immediate publish
)
```

### Custom Video Title

```python
result = agent.automate_video_creation(
    topic="Machine Learning",
    video_title="Complete ML Guide for Beginners 2025",  # Custom title
    video_duration=10,
)
```

### Different Video Styles

```python
# Educational style
agent.automate_video_creation(
    topic="Python Basics",
    video_style="educational",
    target_audience="Beginners"
)

# Entertaining style
agent.automate_video_creation(
    topic="Viral TikTok Trends",
    video_style="entertaining",
    target_audience="Gen Z audience"
)

# Professional style
agent.automate_video_creation(
    topic="Business Strategy",
    video_style="professional",
    target_audience="Business professionals"
)
```

## Module Usage

### Script Generator

```python
from src.modules import ScriptGenerator

script_gen = ScriptGenerator()

# Generate main script
script = script_gen.generate_script(
    topic="AI in Healthcare",
    duration_minutes=5,
    style="informative",
    target_audience="Medical professionals"
)

# Enhance existing script
enhanced = script_gen.enhance_script(
    script=script['script'],
    enhancement_type="seo"
)
```

### Metadata Generator

```python
from src.modules import MetadataGenerator

meta_gen = MetadataGenerator()

# Generate titles
titles = meta_gen.generate_title(
    topic="Python Programming",
    style="informative",
    max_length=60
)

# Generate description
desc = meta_gen.generate_description(
    topic="Python Programming",
    max_length=5000
)

# Generate tags
tags = meta_gen.generate_tags(topic="Python Programming")

# Generate hashtags
hashtags = meta_gen.generate_hashtags(topic="Python Programming")

# Or generate all at once
all_meta = meta_gen.generate_all_metadata(topic="Python Programming")
```

### Subtitle Generator

```python
from src.modules import SubtitleGenerator
from pathlib import Path

sub_gen = SubtitleGenerator(provider="google")  # or "assemblyai"

# Generate subtitles
subtitles = sub_gen.generate_subtitles(
    video_path=Path("video.mp4"),
    language="en-US",
    output_format="srt"  # or "vtt", "json"
)

# Save subtitles
sub_gen.save_subtitles(
    subtitles=subtitles['subtitles'],
    output_path=Path("subtitles.srt")
)
```

### Thumbnail Generator

```python
from src.modules import ThumbnailGenerator

thumb_gen = ThumbnailGenerator()

# Generate thumbnail
thumbnail = thumb_gen.generate_thumbnail(
    title="10 AI Trends 2025",
    description="Explore top AI trends...",
    style="bold",
    color_scheme="blue and orange"
)

# Download thumbnail
thumb_gen.download_thumbnail(
    image_url=thumbnail['image_url'],
    output_path=Path("thumbnail.png")
)
```

### YouTube Uploader

```python
from src.modules import YouTubeUploader
from pathlib import Path

uploader = YouTubeUploader()

# Upload video
result = uploader.upload_video(
    video_path=Path("video.mp4"),
    title="My Amazing Video",
    description="Video description here...",
    tags=["python", "programming", "tutorial"],
    privacy_status="private"
)

video_id = result['video_id']

# Upload thumbnail
uploader.upload_thumbnail(
    video_id=video_id,
    thumbnail_path=Path("thumbnail.png")
)

# Schedule for future
from datetime import datetime, timedelta
publish_time = datetime.now() + timedelta(days=1)
uploader.schedule_video(
    video_id=video_id,
    publish_time=publish_time
)
```

### Video Scheduler

```python
from src.modules import VideoScheduler
from datetime import datetime, timedelta

scheduler = VideoScheduler()
scheduler.start()  # Start scheduler

# Schedule single video
def publish_video(video_id):
    print(f"Publishing {video_id}")
    # Your publish logic

publish_time = datetime.now() + timedelta(hours=1)
job_id = scheduler.schedule_video_publish(
    video_id="abc123",
    publish_function=lambda: publish_video("abc123"),
    publish_time=publish_time
)

# Schedule recurring series
job_ids = scheduler.schedule_recurring_publish(
    series_id="daily_news",
    publish_function=lambda: print("Publishing daily news"),
    start_time=datetime.now() + timedelta(hours=1),
    interval_hours=24,
    num_occurrences=30  # 30 days
)

# Manage jobs
scheduler.reschedule_job(job_id, new_publish_time)
scheduler.cancel_scheduled_job(job_id)
scheduler.pause_job(job_id)
scheduler.resume_job(job_id)

# Check status
status = scheduler.get_job_status(job_id)
jobs = scheduler.get_scheduled_jobs()

scheduler.stop()  # Stop scheduler when done
```

## Configuration

### Disable Features

```bash
# Disable thumbnail generation
GENERATE_THUMBNAIL=False

# Disable scheduler
SCHEDULER_ENABLED=False

# Set privacy status
VIDEO_PRIVACY_STATUS=private  # or "unlisted", "public"
```

### Adjust Settings

```bash
# Change AI model
OPENAI_MODEL=gpt-4-turbo-preview

# Adjust creativity
OPENAI_TEMPERATURE=0.5  # 0=deterministic, 1=creative

# Change timezone for scheduling
SCHEDULER_TIMEZONE=America/New_York

# Enable debug logging
LOG_LEVEL=DEBUG
DEBUG_MODE=True
```

## Error Handling

```python
try:
    result = agent.automate_video_creation(
        topic="Your Topic",
        video_duration=5
    )
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Workflow failed: {e}")
    # Check logs/error.log for details
```

## Checking Workflow Status

```python
# Get workflow result
workflow_id = result['workflow_id']
status = agent.get_workflow_status(workflow_id)

print(f"Status: {status['status']}")
print(f"Steps completed: {list(status['steps'].keys())}")
print(f"Video URL: {status['youtube_url']}")
```

## Logging

All logs are saved to `logs/` directory:

- `logs/automation_agent.log` - All logs
- `logs/error.log` - Errors only

```python
from src.utils import get_logger

logger = get_logger(__name__)
logger.info("This is an info message")
logger.error("This is an error message")
```

## Tips and Best Practices

1. **Start with test publish**: Use `privacy_status="private"` for testing
2. **Monitor API costs**: OpenAI and Google Cloud charge per API call
3. **Batch operations**: Process multiple videos to optimize costs
4. **Save scripts**: Keep generated scripts for quality control
5. **Review metadata**: Always review auto-generated titles and descriptions
6. **Schedule during off-peak**: Spread out scheduled publishes
7. **Monitor quotas**: Check YouTube API quota usage
8. **Back up credentials**: Securely store API keys

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

---

For more help, check the examples in [examples.py](examples.py) or open a GitHub issue.
