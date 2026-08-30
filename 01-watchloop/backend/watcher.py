"""
Watcher - The WatchLoop implementation that monitors task status
"""
import time
import threading
from datetime import datetime
from state_manager import (
    load_state,
    update_watcher_status,
    add_event,
    increment_check_count
)


class WatchLoop:
    def __init__(self, check_interval=60):
        """
        Initialize WatchLoop

        Args:
            check_interval: Seconds between status checks (default 60)
        """
        self.check_interval = check_interval
        self.watcher_thread = None
        self.should_stop = False
        self.is_running = False

    def start(self):
        """Start the watcher loop"""
        if self.is_running:
            return False, "Watcher already running"

        self.should_stop = False
        self.is_running = True

        # Update watcher state
        update_watcher_status(
            "active",
            check_count=0,
            last_check_time=None,
            completion_notified=False
        )

        add_event("watcher_started", "WatchLoop monitoring started")

        # Start watcher in background thread
        self.watcher_thread = threading.Thread(
            target=self._watch_loop,
            daemon=True
        )
        self.watcher_thread.start()

        return True, "Watcher started"

    def stop(self):
        """Stop the watcher loop"""
        if not self.is_running:
            return False, "Watcher not running"

        self.should_stop = True
        self.is_running = False

        update_watcher_status("stopped")
        add_event("watcher_stopped", "WatchLoop monitoring stopped")

        return True, "Watcher stopped"

    def _watch_loop(self):
        """
        Main watcher loop - checks task status every check_interval seconds
        """
        try:
            while not self.should_stop:
                # Wait for the check interval
                for _ in range(self.check_interval):
                    if self.should_stop:
                        break
                    time.sleep(1)

                if self.should_stop:
                    break

                # Perform status check
                self._check_task_status()

        except Exception as e:
            add_event("watcher_error", f"Watcher error: {str(e)}")
            update_watcher_status("stopped")
            self.is_running = False

    def _check_task_status(self):
        """Check the task status and handle completion"""
        state = load_state()
        task_status = state["task"]["status"]
        completion_notified = state["watcher"]["completion_notified"]

        # Increment check count
        check_num = increment_check_count()

        add_event(
            "status_check",
            f"Check #{check_num}: Task status is '{task_status}'"
        )

        # Check if task has completed
        if task_status in ["finished", "failed", "cancelled"]:
            # Only notify once
            if not completion_notified:
                self._handle_completion(task_status)

                # Mark as notified to prevent duplicate notifications
                update_watcher_status(
                    "stopped",
                    completion_notified=True
                )

                # Stop the watcher loop
                self.should_stop = True
                self.is_running = False

    def _handle_completion(self, final_status):
        """Handle task completion - report exactly once"""
        messages = {
            "finished": "[OK] Task completed successfully!",
            "failed": "[FAIL] Task failed",
            "cancelled": "[CANCEL] Task was cancelled"
        }

        message = messages.get(final_status, f"Task ended with status: {final_status}")

        add_event("completion_detected", message)

        print(f"\n{'='*60}")
        print(f"  WATCHLOOP COMPLETION NOTIFICATION")
        print(f"{'='*60}")
        print(f"  {message}")
        print(f"  WatchLoop monitoring stopped.")
        print(f"{'='*60}\n")


# Global watcher instance with configurable check interval
# Use environment variable for testing, default to 60 seconds for production
import os
CHECK_INTERVAL = int(os.environ.get('WATCHLOOP_CHECK_INTERVAL', '60'))
watch_loop = WatchLoop(check_interval=CHECK_INTERVAL)
