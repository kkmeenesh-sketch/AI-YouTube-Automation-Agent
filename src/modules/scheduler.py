"""
Scheduler Module

Handles scheduling of video publishing tasks using APScheduler.
"""

from typing import Dict, Any, Callable, Optional
from datetime import datetime, timedelta
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import pytz

from config.settings import SCHEDULER_TIMEZONE, SCHEDULER_ENABLED
from src.utils import get_logger

logger = get_logger(__name__)


class VideoScheduler:
    """
    Schedule video publishing tasks.
    
    Manages:
    - Scheduled video uploads
    - Automated publishing at specific times
    - Recurring publication schedules
    """

    def __init__(self, timezone: str = SCHEDULER_TIMEZONE):
        """
        Initialize video scheduler.
        
        Args:
            timezone: Timezone for scheduling (e.g., 'UTC', 'America/New_York')
        """
        if not SCHEDULER_ENABLED:
            logger.warning("Scheduler is disabled in settings")
        
        self.timezone = pytz.timezone(timezone)
        self.scheduler = BackgroundScheduler(timezone=timezone)
        self.scheduled_jobs: Dict[str, Dict[str, Any]] = {}

    def start(self) -> None:
        """
        Start the scheduler.
        Must be called before scheduling any tasks.
        """
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")

    def stop(self) -> None:
        """
        Stop the scheduler.
        """
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")

    def schedule_video_publish(
        self,
        video_id: str,
        publish_function: Callable,
        publish_time: datetime,
        job_id: Optional[str] = None,
    ) -> str:
        """
        Schedule a video to be published at specific time.
        
        Args:
            video_id: Video identifier
            publish_function: Function to execute for publishing
            publish_time: When to publish (datetime object)
            job_id: Custom job ID (optional)
        
        Returns:
            Job ID
        """
        if not SCHEDULER_ENABLED:
            logger.warning("Scheduler is disabled, cannot schedule tasks")
            return ""

        job_id = job_id or f"publish_{video_id}_{int(publish_time.timestamp())}"

        logger.info(f"Scheduling video {video_id} for publishing at {publish_time}")

        # Ensure publish_time is timezone-aware
        if publish_time.tzinfo is None:
            publish_time = self.timezone.localize(publish_time)

        try:
            job = self.scheduler.add_job(
                publish_function,
                trigger=DateTrigger(run_date=publish_time),
                id=job_id,
                name=f"Publish {video_id}",
                replace_existing=True,
            )

            self.scheduled_jobs[job_id] = {
                "video_id": video_id,
                "publish_time": publish_time.isoformat(),
                "job_id": job_id,
                "status": "scheduled",
            }

            logger.info(f"Video scheduled with job ID: {job_id}")
            return job_id
        except Exception as e:
            logger.error(f"Error scheduling video: {e}")
            raise

    def schedule_recurring_publish(
        self,
        series_id: str,
        publish_function: Callable,
        start_time: datetime,
        interval_hours: int = 24,
        num_occurrences: Optional[int] = None,
    ) -> Dict[str, str]:
        """
        Schedule recurring video publishing.
        
        Args:
            series_id: Series identifier
            publish_function: Function to execute
            start_time: First publish time
            interval_hours: Hours between publications
            num_occurrences: Number of times to repeat (None = infinite)
        
        Returns:
            Dictionary of scheduled job IDs
        """
        logger.info(f"Scheduling recurring series {series_id}")
        
        job_ids = {}
        current_time = start_time
        occurrence = 0

        while num_occurrences is None or occurrence < num_occurrences:
            job_id = self.schedule_video_publish(
                video_id=f"{series_id}_{occurrence}",
                publish_function=publish_function,
                publish_time=current_time,
                job_id=f"recurring_{series_id}_{occurrence}",
            )
            job_ids[f"occurrence_{occurrence}"] = job_id
            current_time += timedelta(hours=interval_hours)
            occurrence += 1

        logger.info(f"Scheduled {occurrence} occurrences for series {series_id}")
        return job_ids

    def cancel_scheduled_job(self, job_id: str) -> bool:
        """
        Cancel a scheduled publishing job.
        
        Args:
            job_id: Job ID to cancel
        
        Returns:
            True if successful
        """
        logger.info(f"Cancelling job {job_id}")
        
        try:
            self.scheduler.remove_job(job_id)
            if job_id in self.scheduled_jobs:
                self.scheduled_jobs[job_id]["status"] = "cancelled"
            logger.info(f"Job {job_id} cancelled")
            return True
        except Exception as e:
            logger.error(f"Error cancelling job: {e}")
            return False

    def get_scheduled_jobs(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all scheduled jobs.
        
        Returns:
            Dictionary of scheduled jobs
        """
        return self.scheduled_jobs.copy()

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of specific job.
        
        Args:
            job_id: Job ID
        
        Returns:
            Job status or None if not found
        """
        return self.scheduled_jobs.get(job_id)

    def reschedule_job(
        self,
        job_id: str,
        new_publish_time: datetime,
    ) -> bool:
        """
        Reschedule an existing job to new time.
        
        Args:
            job_id: Job ID to reschedule
            new_publish_time: New publish time
        
        Returns:
            True if successful
        """
        logger.info(f"Rescheduling job {job_id} to {new_publish_time}")
        
        if job_id not in self.scheduled_jobs:
            logger.warning(f"Job {job_id} not found")
            return False

        try:
            job = self.scheduler.get_job(job_id)
            if job:
                job.reschedule(trigger=DateTrigger(run_date=new_publish_time))
                self.scheduled_jobs[job_id]["publish_time"] = new_publish_time.isoformat()
                logger.info(f"Job {job_id} rescheduled")
                return True
            return False
        except Exception as e:
            logger.error(f"Error rescheduling job: {e}")
            return False

    def pause_job(self, job_id: str) -> bool:
        """
        Pause a scheduled job (without removing it).
        
        Args:
            job_id: Job ID to pause
        
        Returns:
            True if successful
        """
        logger.info(f"Pausing job {job_id}")
        
        try:
            self.scheduler.pause_job(job_id)
            if job_id in self.scheduled_jobs:
                self.scheduled_jobs[job_id]["status"] = "paused"
            return True
        except Exception as e:
            logger.error(f"Error pausing job: {e}")
            return False

    def resume_job(self, job_id: str) -> bool:
        """
        Resume a paused job.
        
        Args:
            job_id: Job ID to resume
        
        Returns:
            True if successful
        """
        logger.info(f"Resuming job {job_id}")
        
        try:
            self.scheduler.resume_job(job_id)
            if job_id in self.scheduled_jobs:
                self.scheduled_jobs[job_id]["status"] = "scheduled"
            return True
        except Exception as e:
            logger.error(f"Error resuming job: {e}")
            return False
