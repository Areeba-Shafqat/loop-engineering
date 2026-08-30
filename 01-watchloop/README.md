# WatchLoop - Agent Loop Monitoring System

A portfolio project demonstrating an in-session agent loop that watches long-running tasks, similar in concept to Claude's `/loop` command.

## Overview

WatchLoop showcases how an AI agent can autonomously monitor a long-running task by checking its status periodically, detecting completion exactly once, and stopping cleanly without requiring constant user supervision.

## Key Features

- **Autonomous Task Monitoring**: Checks task status every 60 seconds (configurable for testing)
- **Single Completion Notification**: Detects and reports task completion exactly once
- **Clean Lifecycle Management**: Start, stop, and reset operations
- **Real-time Dashboard**: Visual monitoring of task and watcher states
- **Error Handling**: Graceful handling of failures, cancellations, and edge cases

## Architecture

### Backend (Python + Flask)
- **Task Runner**: Simulates long-running tasks with configurable duration
- **State Manager**: File-based state tracking (`task_state.json`)
- **Watcher Loop**: Background thread that polls task status periodically
- **REST API**: Minimal endpoints for frontend communication

### Frontend (React + Vite + Tailwind CSS)
- **Status Dashboard**: Real-time display of task and watcher states
- **Control Panel**: Start/stop/reset buttons
- **Activity Log**: Event history with timestamps
- **Countdown Timer**: Shows next check time

### The WatchLoop Concept

The watcher operates as an in-session loop:
1. Task starts → Watcher activates automatically
2. Every 60 seconds, check task status
3. While incomplete → continue checking
4. On completion → report exactly once, then stop
5. Prevent duplicate notifications with state flags

## Project Structure

```
wacth loop/
├── backend/
│   ├── app.py              # Flask server & API endpoints
│   ├── task_runner.py      # Long-running task simulation
│   ├── watcher.py          # WatchLoop implementation
│   ├── state_manager.py    # State persistence
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main dashboard component
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Tailwind styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs on `http://localhost:5000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`

## How to Demonstrate

### Basic Flow
1. Open the dashboard at `http://localhost:5173`
2. Click **"Start Task"** - this starts a 3-minute demo task
3. Observe the **WatchLoop** activate automatically
4. Watch the check counter increment every 60 seconds
5. See the countdown timer until next check
6. When task completes, see the **completion notification appear exactly once**
7. WatchLoop stops automatically after reporting completion

### Testing Different Scenarios

**Clean Completion**:
- Start task → Wait for completion → Verify single notification

**Manual Stop**:
- Start task → Click "Stop Watcher" → Verify watcher stops cleanly

**Reset & Restart**:
- After completion → Click "Reset" → Start again

**Fast Testing Mode**:
- For rapid testing, the task duration can be configured in `backend/task_runner.py`
- Check interval can be adjusted in `backend/watcher.py` (defaults to 60s)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/start-task` | POST | Start a new task (duration in seconds) |
| `/api/status` | GET | Get current task and watcher status |
| `/api/stop-watcher` | POST | Manually stop the watcher loop |
| `/api/reset` | POST | Reset all state to initial |

## State Model

### Task States
- `idle`: No task running
- `running`: Task in progress
- `finished`: Task completed successfully
- `failed`: Task encountered an error
- `cancelled`: Task was cancelled

### Watcher States
- `stopped`: Not monitoring
- `active`: Actively checking task status

## Design Decisions

### Why File-Based State?
Simple, debuggable, and sufficient for demonstrating the concept without external dependencies.

### Why 60-Second Intervals?
Balances responsiveness with resource efficiency. Long enough to be practical, short enough to demonstrate quickly.

### Why Threading Instead of Celery/Background Jobs?
Demonstrates the in-session loop concept more clearly. The watcher is part of the application lifecycle, not a separate worker system.

### Why Single Completion Notification?
Critical for agent loops - prevents spam and clearly shows the loop detected the state transition exactly when it happened.

## Acceptance Criteria ✅

**Status: ALL CRITERIA PASSED (13/13)**

- [x] Long task can be started ✅
- [x] In-session watcher loop checks periodically ✅
- [x] Default check interval is 60 seconds ✅
- [x] Loop detects task completion ✅
- [x] Completion is announced exactly once ✅
- [x] Loop stops cleanly after completion ✅
- [x] Watcher can be stopped cleanly ✅
- [x] User does not need to watch the terminal ✅
- [x] Frontend clearly visualizes the process ✅
- [x] Error/cancel states are handled ✅
- [x] End-to-end flow has been tested ✅
- [x] README explains the concept ✅
- [x] Project is portfolio-ready ✅

**Test Results**: See `backend/test_acceptance.py` - All tests passing  
**Last Validated**: 2026-08-30

## Technical Highlights

- **Race Condition Prevention**: Completion notification uses a flag to prevent duplicates
- **Thread Safety**: Lock-based state access for concurrent operations
- **Graceful Shutdown**: Clean thread termination on watcher stop
- **Responsive UI**: Real-time updates with polling and countdown timers
- **Error Resilience**: Handles missing files, invalid states, and API failures

## Example Flow

```
User: Clicks "Start Task"
  ↓
Backend: Creates task, saves state, starts watcher thread
  ↓
Watcher: Checks every 60s → status is "running"
  ↓
Task: Completes after N seconds, writes "finished" to state
  ↓
Watcher: Next check detects "finished", sets completion_notified flag
  ↓
Watcher: Adds completion event, stops loop
  ↓
Frontend: Polls status, displays completion notification once
  ↓
User: Sees "Task completed!" in activity log
```

## Portfolio Value

This project demonstrates:
- Full-stack development (React + Python)
- Concurrent programming (threading, state management)
- System design (agent loop pattern)
- Clean UI/UX design
- Production-ready error handling
- Clear documentation

---

**Built with**: React, Vite, Tailwind CSS, Python, Flask
