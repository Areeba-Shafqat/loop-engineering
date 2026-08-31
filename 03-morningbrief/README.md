# Project 03: Morning Brief

## 🎯 Overview

Morning Brief demonstrates **Concept 6** (Unattended Scheduled Loop) and **Concept 12** (The Spine/Persistent Memory). It's a scheduled job that automatically scans the repository for TODOs, remembers what it has seen before, and reports only new discoveries.

## 🏗️ Core Concepts

### Concept 6: Unattended Scheduled Loop

An unattended scheduled loop runs automatically at predetermined times without human intervention.

**Key characteristics:**
- Runs on a schedule (daily, hourly, etc.)
- No manual trigger required
- Continues running over time
- Useful for monitoring, reporting, and maintenance tasks

**In Morning Brief:**
- Scheduled to run daily at 9:00 AM
- Scans repository for TODOs automatically
- Generates a brief without human involvement
- Can be triggered manually for testing

### Concept 12: The Spine/Persistent Memory

The spine is a persistent data store that maintains state across runs, allowing the system to build on previous knowledge rather than starting fresh each time.

**Key characteristics:**
- Survives between runs (file-based, not in-memory)
- Accumulates knowledge over time
- Enables comparison: "What's new?" vs "What did I already know?"
- Prevents duplicate work or notifications

**In Morning Brief:**
- `progress.md` is the spine
- Stores previously discovered TODOs
- Each run reads the spine first
- New runs build upon previous knowledge

## 📁 Project Structure

```
03-morningbrief/
├── morning_brief.py       # Main scheduled job
├── progress.md            # Persistent memory (spine)
├── example_with_todos.py  # Sample file with TODOs for testing
└── README.md             # This file
```

## 🔄 How It Works

### On Every Run

1. **Read Spine**: Load `progress.md` to see what TODOs were previously known
2. **Scan Repository**: Find all TODO comments in Python files
3. **Compare**: Identify which TODOs are new vs already known
4. **Generate Brief**: Print console report showing:
   - Total TODOs found
   - Previously known count
   - New discoveries (not in spine)
   - Sample of already-tracked items
5. **Update Spine**: Append run results to `progress.md`
   - Preserves history (doesn't overwrite)
   - Records date, findings, and cumulative state

### Persistent Memory Example

```
RUN 1 (Initial):
- Find: TODO A, TODO B, TODO C
- New: 3 items
- Spine: Records A, B, C

RUN 2 (Next day):
- Find: TODO A, TODO B, TODO C (same as before)
- New: 0 items
- Already known: 3 items
- Spine: Notes "no new TODOs"

(Developer adds TODO D)

RUN 3:
- Find: TODO A, TODO B, TODO C, TODO D
- New: 1 item (D)
- Already known: 3 items (A, B, C)
- Spine: Records D as new discovery
```

## 🚀 Usage

### Manual Run (For Testing)

```bash
cd 03-morningbrief
python morning_brief.py
```

### Scheduled Run (Automated)

#### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Morning Brief"
4. Trigger: Daily at 9:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `"F:\path\to\loop-engineering\03-morningbrief\morning_brief.py"`
   - Start in: `"F:\path\to\loop-engineering\03-morningbrief"`

#### Linux/Mac (cron)

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9:00 AM)
0 9 * * * cd /path/to/loop-engineering/03-morningbrief && python morning_brief.py >> brief.log 2>&1
```

## 📊 Demonstration Results

### Run 1: Initial State
```
Total TODOs found: 3
New discoveries: 3
Already known: 0

New TODOs:
- Add error handling for network timeouts
- Implement caching mechanism  
- Add unit tests for this module
```

### Run 2: No Changes
```
Total TODOs found: 3
New discoveries: 0
Already known: 3

[OK] No new TODOs since last run
```

### Run 3: New TODO Added
```
Total TODOs found: 4
New discoveries: 1
Already known: 3

New TODOs:
- Add logging for debugging purposes

Already tracked:
- Add error handling for network timeouts
- Implement caching mechanism
- Add unit tests for this module
```

## ✅ Acceptance Criteria Verification

- [x] **Scheduled job exists** - `morning_brief.py` can run via scheduler
- [x] **Job can run unattended** - Scheduling instructions provided
- [x] **Job reads progress.md before processing** - Loads spine first
- [x] **Job gathers repository information** - Scans for TODO comments
- [x] **First run records findings** - Run 1 recorded 3 TODOs
- [x] **progress.md persists between runs** - File survives, accumulates
- [x] **Second run uses first run's info** - Run 2 recognized 3 as known
- [x] **Previously recorded items not reported as new** - Run 2: 0 new
- [x] **Newly discovered items detected** - Run 3: found 1 new TODO
- [x] **progress.md updated after second run** - History appended
- [x] **Console shows new vs known** - Clear distinction in output
- [x] **Two-run demonstration tested** - Runs 1, 2, 3 all verified
- [x] **README explains concepts** - This document
- [x] **No unnecessary complexity** - Simple, focused implementation

## 🎓 Key Learnings

### Concept 6: Unattended Scheduled Loop

**Benefits:**
- Automation reduces manual work
- Consistent monitoring without human intervention
- Can run during off-hours
- Scales to many tasks

**Considerations:**
- Must handle failures gracefully
- Logging is essential for debugging
- Need to prevent duplicate notifications
- Resource usage must be reasonable

### Concept 12: The Spine/Persistent Memory

**Benefits:**
- Enables incremental processing
- Avoids duplicate work
- Provides context across runs
- Allows trend analysis over time

**Considerations:**
- File must be reliably read/written
- Data format must be stable
- Need strategy for old data (archive? prune?)
- Corruption recovery plan helpful

## 🔍 Technical Details

### TODO Detection

The job scans Python files for comments matching:
```python
# TODO: Some task description
```

It extracts the text after `TODO:` and tracks it in the spine.

### Spine Format

`progress.md` uses markdown with a simple structure:
```markdown
---
## Run: YYYY-MM-DD HH:MM:SS

### Summary
- Total TODOs found: X
- New TODOs this run: Y
- Previously known: Z

### New Discoveries
- `TODO text` - file:line

### All TODOs (Cumulative)
- `TODO text` - file:line
```

Each run appends to the file, preserving complete history.

## 🎯 Portfolio Value

This project demonstrates:
- Automation and scheduling
- Persistent state management
- File I/O and parsing
- Incremental data processing
- Change detection algorithms
- Professional tool development
- Clear documentation

---

**Author**: Areeba Shafqat  
**Date**: 2026-08-31  
**Concepts**: Unattended Scheduled Loop, Persistent Memory (Spine)
