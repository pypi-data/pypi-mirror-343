"""
Scheduler module for GibGram.

This module provides functionality for scheduling media downloads at regular intervals.
"""

import os
import json
import time
import logging
import subprocess
import threading
import signal
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)

class ScheduledTask:
    """Represents a scheduled download task."""

    def __init__(
        self,
        task_id: int,
        name: str,
        interval: str,
        command: List[str],
        next_run: Optional[datetime] = None
    ):
        """
        Initialize a scheduled task.

        Args:
            task_id: Unique identifier for the task
            name: Name of the task
            interval: Interval string (e.g., '1h', '30m', '1d')
            command: Command to run
            next_run: Next scheduled run time
        """
        self.task_id = task_id
        self.name = name
        self.interval = interval
        self.command = command

        # Parse interval
        self.interval_seconds = self._parse_interval(interval)

        # Set next run time
        if next_run:
            self.next_run = next_run
        else:
            self.next_run = datetime.now() + timedelta(seconds=self.interval_seconds)

    def _parse_interval(self, interval: str) -> int:
        """
        Parse interval string to seconds.

        Args:
            interval: Interval string (e.g., '1h', '30m', '1d')

        Returns:
            Interval in seconds
        """
        if not interval:
            # Default to 1 hour
            return 3600

        # Extract number and unit
        if interval[-1].isdigit():
            # No unit specified, assume seconds
            return int(interval)

        number = int(interval[:-1])
        unit = interval[-1].lower()

        # Convert to seconds
        if unit == 's':
            return number
        elif unit == 'm':
            return number * 60
        elif unit == 'h':
            return number * 3600
        elif unit == 'd':
            return number * 86400
        else:
            # Invalid unit, default to seconds
            logger.warning(f"Invalid interval unit: {unit}. Using seconds.")
            return number

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task to dictionary for serialization.

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.task_id,
            "name": self.name,
            "interval": self.interval,
            "command": self.command,
            "next_run": self.next_run.isoformat() if self.next_run else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScheduledTask':
        """
        Create task from dictionary.

        Args:
            data: Dictionary representation of the task

        Returns:
            ScheduledTask instance
        """
        next_run = None
        if data.get("next_run"):
            try:
                next_run = datetime.fromisoformat(data["next_run"])
            except ValueError:
                # If parsing fails, set to None
                next_run = None

        return cls(
            task_id=data["id"],
            name=data["name"],
            interval=data["interval"],
            command=data["command"],
            next_run=next_run
        )

    def update_next_run(self):
        """Update the next run time based on the interval."""
        self.next_run = datetime.now() + timedelta(seconds=self.interval_seconds)

    def is_due(self) -> bool:
        """
        Check if the task is due to run.

        Returns:
            True if the task is due, False otherwise
        """
        return datetime.now() >= self.next_run

    def __str__(self) -> str:
        """String representation of the task."""
        return f"Task {self.task_id}: {self.name} (every {self.interval}, next run: {self.next_run.strftime('%Y-%m-%d %H:%M:%S')})"

class Scheduler:
    """Scheduler for managing and running scheduled tasks."""

    def __init__(self, config_dir: str = None):
        """
        Initialize the scheduler.

        Args:
            config_dir: Directory to store configuration files
        """
        # Set config directory
        if config_dir:
            self.config_dir = config_dir
        else:
            # Default to user's home directory
            self.config_dir = os.path.join(os.path.expanduser("~"), ".gibgram")

        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)

        # Set config file path
        self.config_file = os.path.join(self.config_dir, "schedule.json")

        # Initialize tasks
        self.tasks: List[ScheduledTask] = []

        # Load tasks from config file
        self.load_tasks()

        # Flag to control the scheduler loop
        self.running = False

        # Thread for running the scheduler
        self.scheduler_thread = None

    def load_tasks(self):
        """Load tasks from config file."""
        if not os.path.exists(self.config_file):
            logger.info("No schedule config file found. Creating a new one.")
            self.tasks = []
            self.save_tasks()
            return

        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)

            self.tasks = [ScheduledTask.from_dict(task_data) for task_data in data]
            logger.info(f"Loaded {len(self.tasks)} scheduled tasks")
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            self.tasks = []

    def save_tasks(self):
        """Save tasks to config file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2)
            logger.info(f"Saved {len(self.tasks)} scheduled tasks")
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")

    def add_task(self, name: str, interval: str, command: List[str]) -> int:
        """
        Add a new scheduled task.

        Args:
            name: Name of the task
            interval: Interval string (e.g., '1h', '30m', '1d')
            command: Command to run

        Returns:
            ID of the new task
        """
        # Generate a new task ID
        task_id = 1
        if self.tasks:
            task_id = max(task.task_id for task in self.tasks) + 1

        # Create new task
        task = ScheduledTask(
            task_id=task_id,
            name=name,
            interval=interval,
            command=command
        )

        # Add to tasks list
        self.tasks.append(task)

        # Save tasks
        self.save_tasks()

        logger.info(f"Added new task: {task}")
        return task_id

    def remove_task(self, task_id: int) -> bool:
        """
        Remove a scheduled task.

        Args:
            task_id: ID of the task to remove

        Returns:
            True if the task was removed, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                logger.info(f"Removed task {task_id}")
                return True

        logger.warning(f"Task {task_id} not found")
        return False

    def get_task(self, task_id: int) -> Optional[ScheduledTask]:
        """
        Get a task by ID.

        Args:
            task_id: ID of the task

        Returns:
            ScheduledTask or None if not found
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task

        return None

    def list_tasks(self) -> List[ScheduledTask]:
        """
        Get all scheduled tasks.

        Returns:
            List of scheduled tasks
        """
        return self.tasks

    def run_task(self, task: ScheduledTask):
        """
        Run a scheduled task.

        Args:
            task: Task to run
        """
        logger.info(f"Running task {task.task_id}: {task.name}")

        try:
            # Run the command
            subprocess.run(task.command, check=True)
            logger.info(f"Task {task.task_id} completed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Task {task.task_id} failed with exit code {e.returncode}")
        except Exception as e:
            logger.error(f"Error running task {task.task_id}: {e}")

        # Update next run time
        task.update_next_run()
        self.save_tasks()

    def start(self):
        """Start the scheduler."""
        if self.running:
            logger.warning("Scheduler is already running")
            return

        self.running = True

        # Start scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

        logger.info("Scheduler started")

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def stop(self):
        """Stop the scheduler."""
        if not self.running:
            logger.warning("Scheduler is not running")
            return

        self.running = False

        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)

        logger.info("Scheduler stopped")

    def _scheduler_loop(self):
        """Main scheduler loop."""
        logger.info("Scheduler loop started")

        while self.running:
            # Check for due tasks
            for task in self.tasks:
                if task.is_due():
                    # Run the task in a separate thread
                    threading.Thread(target=self.run_task, args=(task,)).start()

            # Sleep for a short time
            time.sleep(10)

    def _signal_handler(self, sig, frame):
        """Handle signals for graceful shutdown."""
        logger.info(f"Received signal {sig}, shutting down...")
        self.stop()
        sys.exit(0)

def parse_interval(interval_str: str) -> int:
    """
    Parse interval string to seconds.

    Args:
        interval_str: Interval string (e.g., '1h', '30m', '1d')

    Returns:
        Interval in seconds
    """
    if not interval_str:
        # Default to 1 hour
        return 3600

    # Extract number and unit
    if interval_str[-1].isdigit():
        # No unit specified, assume seconds
        return int(interval_str)

    try:
        number = int(interval_str[:-1])
        unit = interval_str[-1].lower()

        # Convert to seconds
        if unit == 's':
            return number
        elif unit == 'm':
            return number * 60
        elif unit == 'h':
            return number * 3600
        elif unit == 'd':
            return number * 86400
        else:
            # Invalid unit, default to seconds
            logger.warning(f"Invalid interval unit: {unit}. Using seconds.")
            return number
    except ValueError:
        logger.warning(f"Invalid interval format: {interval_str}. Using 1 hour.")
        return 3600
