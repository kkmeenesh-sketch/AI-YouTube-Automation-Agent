"""
Quick start guide and examples for AI YouTube Automation Agent.
"""

from src.main import YouTubeAutomationAgent
from datetime import datetime, timedelta
import json


def example_basic_workflow():
    """
    Example: Basic workflow with default settings.
    """
    print("\n=== Example 1: Basic Workflow ===")
    
    agent = YouTubeAutomationAgent()
    
    result = agent.automate_video_creation(
        topic="Top 10 AI Trends in 2025",
        video_duration=5,
        video_style="informative",
        target_audience="Tech enthusiasts",
    )
    
    print(json.dumps(result, indent=2, default=str))


def example_scheduled_publish():
    """
    Example: Schedule video for future publishing.
    """
    print("\n=== Example 2: Scheduled Publishing ===")
    
    agent = YouTubeAutomationAgent()
    
    # Schedule for tomorrow at 2 PM
    publish_time = datetime.now() + timedelta(days=1, hours=14)
    
    result = agent.automate_video_creation(
        topic="Introduction to Quantum Computing",
        video_duration=10,
        video_style="educational",
        publish_time=publish_time,
        schedule=True,
    )
    
    print(f"Video scheduled for: {publish_time}")
    print(json.dumps(result, indent=2, default=str))


def example_custom_title():
    """
    Example: Use custom video title instead of auto-generated.
    """
    print("\n=== Example 3: Custom Title ===")
    
    agent = YouTubeAutomationAgent()
    
    result = agent.automate_video_creation(
        topic="Machine Learning Basics",
        video_title="Complete Guide to ML for Beginners 2025",
        video_duration=8,
        video_style="educational",
    )
    
    print(json.dumps(result, indent=2, default=str))


def example_immediate_publish():
    """
    Example: Auto-publish immediately after upload.
    """
    print("\n=== Example 4: Immediate Auto-Publish ===")
    
    agent = YouTubeAutomationAgent()
    
    result = agent.automate_video_creation(
        topic="Python Programming Tips",
        video_duration=6,
        video_style="entertaining",
        auto_publish=True,  # Automatically publish
    )
    
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("AI YouTube Automation Agent - Examples")
    print(f"{'='*60}")
    
    # Run examples (uncomment to execute)
    # example_basic_workflow()
    # example_scheduled_publish()
    # example_custom_title()
    # example_immediate_publish()
    
    print("\nExamples are ready to run!")
    print("\nTo run examples, uncomment the function calls at the bottom.")
    print("\nNote: These are demonstration examples.")
    print("In production, ensure all API credentials are configured in .env")
