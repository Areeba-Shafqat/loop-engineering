"""
Task Runner - Simulates a long-running task
"""
import time
import threading
from datetime import datetime
from state_manager import update_task_status, add_event


class TaskRunner:
    def __init__(self):
        self.task_thread = None
        self.should_stop = False

    def start_task(self, duration_seconds):
        """Start a long-running task"""
        if self.task_thread and self.task_thread.is_alive():
            return False, "Task already running"

        self.should_stop = False

        # Initialize task state
        update_task_status(
            "running",
            start_time=datetime.utcnow().isoformat() + "Z",
            completion_time=None,
            duration=duration_seconds,
            error=None
        )

        add_event("task_started", f"Task started with duration {duration_seconds}s")

        # Start task in background thread
        self.task_thread = threading.Thread(
            target=self._run_task,
            args=(duration_seconds,),
            daemon=True
        )
        self.task_thread.start()

        return True, "Task started"

    def _run_task(self, duration):
        """Execute the long-running task"""
        try:
            # Simulate work by sleeping in small increments to allow cancellation
            elapsed = 0
            while elapsed < duration and not self.should_stop:
                time.sleep(min(1, duration - elapsed))
                elapsed += 1

            if self.should_stop:
                # Task was cancelled
                update_task_status(
                    "cancelled",
                    completion_time=datetime.utcnow().isoformat() + "Z"
                )
                add_event("task_cancelled", "Task was cancelled")
            else:
                # Task completed successfully
                update_task_status(
                    "finished",
                    completion_time=datetime.utcnow().isoformat() + "Z"
                )
                add_event("task_finished", f"Task completed after {duration}s")

        except Exception as e:
            # Task failed
            update_task_status(
                "failed",
                completion_time=datetime.utcnow().isoformat() + "Z",
                error=str(e)
            )
            add_event("task_failed", f"Task failed: {str(e)}")

    def cancel_task(self):
        """Cancel the running task"""
        if self.task_thread and self.task_thread.is_alive():
            self.should_stop = True
            return True, "Task cancellation requested"
        return False, "No task running"


# Global task runner instance
task_runner = TaskRunner()
