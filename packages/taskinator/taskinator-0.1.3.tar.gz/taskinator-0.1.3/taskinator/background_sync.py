"""Background synchronization for Taskinator."""

import asyncio
import threading
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Tuple, Union
from queue import Queue, PriorityQueue

from loguru import logger

from taskinator.plugin_registry import registry as plugin_registry
from taskinator.constants import SyncDirection


class JobStatus(str, Enum):
    """Job status constants."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobPriority(int, Enum):
    """Job priority constants."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class SyncJob:
    """Represents a synchronization job."""
    
    def __init__(
        self,
        task_id: str,
        system_id: str,
        direction: str = SyncDirection.BIDIRECTIONAL,
        priority: JobPriority = JobPriority.MEDIUM,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize a sync job.
        
        Args:
            task_id: ID of the task to synchronize
            system_id: ID of the external system
            direction: Sync direction (bidirectional, push, pull)
            priority: Job priority
            config: Additional configuration for the job
        """
        self.id = str(uuid.uuid4())
        self.task_id = task_id
        self.system_id = system_id
        self.direction = direction
        self.priority = priority
        self.config = config or {}
        self.status = JobStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        
    def __lt__(self, other):
        """Compare jobs by priority."""
        if not isinstance(other, SyncJob):
            return NotImplemented
        return self.priority.value < other.priority.value
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the job to a dictionary.
        
        Returns:
            Dictionary representation of the job
        """
        return {
            "id": self.id,
            "task_id": self.task_id,
            "system_id": self.system_id,
            "direction": self.direction,
            "priority": self.priority.value,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error
        }


class JobQueue:
    """Queue for synchronization jobs."""
    
    def __init__(self):
        """Initialize the job queue."""
        self.queue = PriorityQueue()
        self.jobs: Dict[str, SyncJob] = {}
        self._lock = threading.Lock()
        
    def add_job(self, job: SyncJob) -> str:
        """Add a job to the queue.
        
        Args:
            job: Job to add
            
        Returns:
            Job ID
        """
        with self._lock:
            self.jobs[job.id] = job
            self.queue.put((job.priority.value, job.id))
            
        logger.info(f"Added job {job.id} to queue (task: {job.task_id}, system: {job.system_id})")
        return job.id
        
    def get_job(self, job_id: str) -> Optional[SyncJob]:
        """Get a job by ID.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job if found, None otherwise
        """
        with self._lock:
            return self.jobs.get(job_id)
            
    def get_next_job(self) -> Optional[SyncJob]:
        """Get the next job from the queue.
        
        Returns:
            Next job if available, None otherwise
        """
        if self.queue.empty():
            return None
            
        try:
            _, job_id = self.queue.get_nowait()
            with self._lock:
                return self.jobs.get(job_id)
        except Exception as e:
            logger.error(f"Error getting next job: {e}")
            return None
            
    def update_job(self, job: SyncJob) -> None:
        """Update a job in the queue.
        
        Args:
            job: Job to update
        """
        with self._lock:
            self.jobs[job.id] = job
            
    def remove_job(self, job_id: str) -> None:
        """Remove a job from the queue.
        
        Args:
            job_id: Job ID
        """
        with self._lock:
            if job_id in self.jobs:
                del self.jobs[job_id]
                
    def get_all_jobs(self) -> List[SyncJob]:
        """Get all jobs in the queue.
        
        Returns:
            List of all jobs
        """
        with self._lock:
            return list(self.jobs.values())
            
    def get_jobs_by_status(self, status: JobStatus) -> List[SyncJob]:
        """Get jobs by status.
        
        Args:
            status: Job status
            
        Returns:
            List of jobs with the specified status
        """
        with self._lock:
            return [job for job in self.jobs.values() if job.status == status]
            
    def get_jobs_by_task(self, task_id: str) -> List[SyncJob]:
        """Get jobs for a specific task.
        
        Args:
            task_id: Task ID
            
        Returns:
            List of jobs for the specified task
        """
        with self._lock:
            return [job for job in self.jobs.values() if job.task_id == task_id]
            
    def get_jobs_by_system(self, system_id: str) -> List[SyncJob]:
        """Get jobs for a specific system.
        
        Args:
            system_id: System ID
            
        Returns:
            List of jobs for the specified system
        """
        with self._lock:
            return [job for job in self.jobs.values() if job.system_id == system_id]


class JobWorker:
    """Worker for processing synchronization jobs."""
    
    def __init__(self, queue: JobQueue):
        """Initialize the job worker.
        
        Args:
            queue: Job queue
        """
        self.queue = queue
        self.running = False
        self.thread = None
        self.loop = None
        
    def start(self) -> None:
        """Start the worker thread."""
        if self.running:
            logger.warning("Worker is already running")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        
        logger.info("Started job worker thread")
        
    def stop(self) -> None:
        """Stop the worker thread."""
        if not self.running:
            logger.warning("Worker is not running")
            return
            
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5.0)
            
        logger.info("Stopped job worker thread")
        
    def _run(self) -> None:
        """Run the worker thread."""
        # Create a new event loop for this thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            # Run the main worker loop
            self.loop.run_until_complete(self._worker_loop())
        except Exception as e:
            logger.error(f"Error in worker thread: {e}")
        finally:
            # Clean up the event loop
            self.loop.close()
            self.loop = None
            
    async def _worker_loop(self) -> None:
        """Main worker loop."""
        while self.running:
            # Get the next job from the queue
            job = self.queue.get_next_job()
            if not job:
                # No jobs available, wait a bit
                await asyncio.sleep(1.0)
                continue
                
            # Process the job
            try:
                await self._process_job(job)
            except Exception as e:
                logger.error(f"Error processing job {job.id}: {e}")
                job.status = JobStatus.FAILED
                job.error = str(e)
                self.queue.update_job(job)
                
    async def _process_job(self, job: SyncJob) -> None:
        """Process a job.
        
        Args:
            job: Job to process
        """
        logger.info(f"Processing job {job.id} (task: {job.task_id}, system: {job.system_id})")
        
        # Update job status
        job.status = JobStatus.RUNNING
        job.started_at = datetime.now()
        self.queue.update_job(job)
        
        try:
            # Load the plugin for the specified system
            plugin_name = f"{job.system_id}_adapter"
            if not plugin_registry.load_plugin(plugin_name):
                raise ValueError(f"Failed to load plugin for system {job.system_id}")
            
            # Get the sync configuration
            config = self._get_sync_config(job.system_id)
            if not config:
                raise ValueError(f"Failed to get configuration for system {job.system_id}")
            
            # Merge with job config
            if job.config:
                config.update(job.config)
            
            # Get the adapter for the system
            adapter = await plugin_registry.get_adapter_instance(job.system_id, **config)
            if not adapter:
                raise ValueError(f"Failed to get adapter for system {job.system_id}")
                
            # Get the task data
            task_data = self._get_task_data(job.task_id)
            if not task_data:
                raise ValueError(f"Failed to get task data for task {job.task_id}")
                
            # Synchronize the task
            result = await adapter.sync_task(task_data, direction=job.direction)
            
            # Update job status
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now()
            job.result = result
            self.queue.update_job(job)
            
            logger.info(f"Completed job {job.id}")
            
        except Exception as e:
            # Update job status
            job.status = JobStatus.FAILED
            job.completed_at = datetime.now()
            job.error = str(e)
            self.queue.update_job(job)
            
            logger.error(f"Failed job {job.id}: {e}")
            
        finally:
            # Close the adapter
            if 'adapter' in locals() and adapter:
                await plugin_registry.close_adapter(job.system_id)
                
    def _get_sync_config(self, system_id: str) -> Dict[str, Any]:
        """Get sync configuration for a system.
        
        Args:
            system_id: System ID
            
        Returns:
            Sync configuration
        """
        import os
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        # Get configuration based on system ID
        if system_id == "nextcloud":
            return {
                "host": os.getenv("NEXTCLOUD_HOST", ""),
                "username": os.getenv("NEXTCLOUD_USERNAME", ""),
                "password": os.getenv("NEXTCLOUD_PASSWORD", ""),
                "calendar_name": os.getenv("NEXTCLOUD_CALENDAR", "Taskinator")
            }
        
        # Default empty configuration
        return {}
        
    def _get_task_data(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task data by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task data if found, None otherwise
        """
        import json
        from pathlib import Path
        
        # Read tasks from the tasks.json file
        tasks_file = Path("tasks/tasks.json")
        if not tasks_file.exists():
            logger.error(f"Tasks file not found: {tasks_file}")
            return None
            
        try:
            with open(tasks_file, "r") as f:
                tasks_data = json.load(f)
                
            # Get the tasks list
            tasks_list = tasks_data.get("tasks", [])
            
            # Find the task by ID
            for task in tasks_list:
                if str(task.get("id")) == task_id:
                    return task
                    
            logger.error(f"Task not found: {task_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error loading task data: {e}")
            return None


class BackgroundSyncManager:
    """Manager for background synchronization."""
    
    _instance = None
    
    def __new__(cls):
        """Create a new instance or return the existing one."""
        if cls._instance is None:
            cls._instance = super(BackgroundSyncManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        """Initialize the background sync manager."""
        if self._initialized:
            return
            
        self.job_queue = JobQueue()
        self.worker = JobWorker(self.job_queue)
        self._initialized = True
        self._running = False
        self._scheduled = False
        self._scheduler_thread = None
        self._scheduler_interval = 0
        
    def start(self) -> None:
        """Start the background sync manager."""
        self.worker.start()
        self._running = True
        logger.info("Background sync manager started")
        
    def stop(self) -> None:
        """Stop the background sync manager."""
        self.worker.stop()
        self._running = False
        
        # Stop the scheduler if it's running
        if self._scheduled and self._scheduler_thread and self._scheduler_thread.is_alive():
            self._scheduled = False
            self._scheduler_thread.join(timeout=5.0)
            self._scheduler_thread = None
            
        logger.info("Background sync manager stopped")
        
    def get_status(self) -> str:
        """Get the status of the background sync manager.
        
        Returns:
            Status string
        """
        if self.worker and self.worker.running:
            if self._scheduled:
                return f"running (scheduled every {self._scheduler_interval} minutes)"
            return "running"
        return "stopped"
        
    def schedule(self, interval: int) -> None:
        """Schedule background sync to run at regular intervals.
        
        Args:
            interval: Interval in minutes between syncs
        """
        if interval <= 0:
            raise ValueError("Interval must be positive")
            
        # Stop the current scheduler if it's running
        if self._scheduled and self._scheduler_thread and self._scheduler_thread.is_alive():
            self._scheduled = False
            self._scheduler_thread.join(timeout=5.0)
            
        # Start a new scheduler
        self._scheduled = True
        self._scheduler_interval = interval
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self._scheduler_thread.daemon = True
        self._scheduler_thread.start()
        
        logger.info(f"Scheduled background sync every {interval} minutes")
        
    def unschedule(self) -> None:
        """Unschedule background sync."""
        if not self._scheduled:
            logger.warning("Background sync is not scheduled")
            return
            
        self._scheduled = False
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            self._scheduler_thread.join(timeout=5.0)
            
        self._scheduler_thread = None
        self._scheduler_interval = 0
        
        logger.info("Unscheduled background sync")
        
    def _scheduler_loop(self) -> None:
        """Scheduler loop."""
        while self._scheduled and self._running:
            # Schedule sync for all tasks and all systems
            self._schedule_all_tasks()
            
            # Wait for the next interval
            for _ in range(self._scheduler_interval * 60):
                if not self._scheduled or not self._running:
                    break
                time.sleep(1)
                
    def _schedule_all_tasks(self) -> None:
        """Schedule sync for all tasks and all systems."""
        import json
        from pathlib import Path
        
        # Read tasks from the tasks.json file
        tasks_file = Path("tasks/tasks.json")
        if not tasks_file.exists():
            logger.error(f"Tasks file not found: {tasks_file}")
            return
            
        try:
            with open(tasks_file, "r") as f:
                tasks_data = json.load(f)
                
            # Get the tasks list
            tasks_list = tasks_data.get("tasks", [])
            
            # Get all available systems
            systems = plugin_registry.get_available_systems()
            
            # Schedule sync for each task and system
            for task in tasks_list:
                task_id = str(task.get("id"))
                for system in systems:
                    self.add_job(task_id, system, SyncDirection.BIDIRECTIONAL, JobPriority.LOW)
                    
            logger.info(f"Scheduled sync for {len(tasks_list)} tasks and {len(systems)} systems")
            
        except Exception as e:
            logger.error(f"Error scheduling tasks: {e}")
            
    def add_job(
        self,
        task_id: str,
        system_id: str,
        direction: str = SyncDirection.BIDIRECTIONAL,
        priority: JobPriority = JobPriority.MEDIUM,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add a job to the queue.
        
        Args:
            task_id: ID of the task to synchronize
            system_id: ID of the external system
            direction: Sync direction (bidirectional, push, pull)
            priority: Job priority
            config: Additional configuration for the job
            
        Returns:
            Job ID
        """
        job = SyncJob(task_id, system_id, direction, priority, config)
        return self.job_queue.add_job(job)
        
    def get_job(self, job_id: str) -> Optional[SyncJob]:
        """Get a job by ID.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job if found, None otherwise
        """
        return self.job_queue.get_job(job_id)
        
    def get_all_jobs(self) -> List[SyncJob]:
        """Get all jobs in the queue.
        
        Returns:
            List of all jobs
        """
        return self.job_queue.get_all_jobs()
        
    def get_jobs_by_status(self, status: JobStatus) -> List[SyncJob]:
        """Get jobs by status.
        
        Args:
            status: Job status
            
        Returns:
            List of jobs with the specified status
        """
        return self.job_queue.get_jobs_by_status(status)
        
    def get_jobs_by_task(self, task_id: str) -> List[SyncJob]:
        """Get jobs for a specific task.
        
        Args:
            task_id: Task ID
            
        Returns:
            List of jobs for the specified task
        """
        return self.job_queue.get_jobs_by_task(task_id)
        
    def get_jobs_by_system(self, system_id: str) -> List[SyncJob]:
        """Get jobs for a specific system.
        
        Args:
            system_id: System ID
            
        Returns:
            List of jobs for the specified system
        """
        return self.job_queue.get_jobs_by_system(system_id)
        
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job.
        
        Args:
            job_id: Job ID
            
        Returns:
            True if the job was cancelled, False otherwise
        """
        job = self.job_queue.get_job(job_id)
        if not job:
            return False
            
        if job.status == JobStatus.PENDING:
            job.status = JobStatus.CANCELLED
            self.job_queue.update_job(job)
            return True
            
        return False


# Create a singleton instance
background_sync_manager = BackgroundSyncManager()
