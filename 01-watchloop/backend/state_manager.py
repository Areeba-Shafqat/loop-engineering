"""
State Manager - Handles persistent state for task and watcher
"""
import json
import os
from datetime import datetime
from threading import Lock

STATE_FILE = "task_state.json"
state_lock = Lock()


def get_initial_state():
    """Return the default initial state"""
    return {
        "task": {
            "status": "idle",
            "start_time": None,
            "completion_time": None,
            "duration": None,
            "error": None
        },
        "watcher": {
            "status": "stopped",
            "check_count": 0,
            "last_check_time": None,
            "completion_notified": False
        },
        "events": []
    }


def load_state():
    """Load state from file, return initial state if file doesn't exist"""
    with state_lock:
        if not os.path.exists(STATE_FILE):
            return get_initial_state()

        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return get_initial_state()


def save_state(state):
    """Save state to file"""
    with state_lock:
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
        except IOError as e:
            print(f"Error saving state: {e}")


def update_task_status(status, **kwargs):
    """Update task status and optional fields"""
    state = load_state()
    state["task"]["status"] = status

    for key, value in kwargs.items():
        if key in state["task"]:
            state["task"][key] = value

    save_state(state)
    return state


def update_watcher_status(status, **kwargs):
    """Update watcher status and optional fields"""
    state = load_state()
    state["watcher"]["status"] = status

    for key, value in kwargs.items():
        if key in state["watcher"]:
            state["watcher"][key] = value

    save_state(state)
    return state


def add_event(event_type, message):
    """Add an event to the history"""
    state = load_state()
    event = {
        "type": event_type,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    state["events"].append(event)

    # Keep only last 50 events
    state["events"] = state["events"][-50:]

    save_state(state)
    return event


def reset_state():
    """Reset to initial state"""
    state = get_initial_state()
    save_state(state)
    return state


def increment_check_count():
    """Increment watcher check count and update last check time"""
    state = load_state()
    state["watcher"]["check_count"] += 1
    state["watcher"]["last_check_time"] = datetime.utcnow().isoformat() + "Z"
    save_state(state)
    return state["watcher"]["check_count"]
