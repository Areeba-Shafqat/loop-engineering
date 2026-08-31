"""
Morning Brief - Scheduled Job with Persistent Memory
Demonstrates Concept 6 (unattended scheduled loop) and Concept 12 (spine/persistent memory)
"""
import os
import re
from datetime import datetime
from pathlib import Path


def read_spine():
    """
    Read the persistent memory (spine) from progress.md
    Returns dict with previously known TODOs
    """
    spine_file = Path("progress.md")

    if not spine_file.exists():
        return {"known_todos": set(), "run_history": []}

    content = spine_file.read_text(encoding='utf-8')

    # Extract known TODOs from the spine
    known_todos = set()

    for line in content.split('\n'):
        # Look for TODO entries in markdown list format with backticks
        if line.strip().startswith('-') and '`' in line:
            # Extract the TODO text from backticks
            match = re.search(r'- `([^`]+)`', line)
            if match:
                known_todos.add(match.group(1))

    return {
        "known_todos": known_todos,
        "run_history": content.split('\n---\n') if '---' in content else []
    }


def find_todos_in_repo():
    """
    Scan repository for TODO comments
    Returns dict mapping file:line to TODO text
    """
    todos = {}
    repo_root = Path("..").resolve()

    # Scan Python files for TODO comments
    for py_file in repo_root.rglob("*.py"):
        # Skip virtual environments and cache
        if any(part.startswith('.') or part in ['venv', '__pycache__', 'node_modules']
               for part in py_file.parts):
            continue

        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    # Look for TODO comments
                    if 'TODO' in line:
                        # Extract the TODO text
                        match = re.search(r'#\s*TODO:?\s*(.+)', line, re.IGNORECASE)
                        if match:
                            todo_text = match.group(1).strip()
                            rel_path = py_file.relative_to(repo_root)
                            location = f"{rel_path}:{line_num}"
                            todos[location] = todo_text
        except Exception as e:
            continue

    return todos


def generate_brief(spine_data, current_todos):
    """
    Generate the morning brief comparing current state with spine
    """
    known = spine_data["known_todos"]

    # Identify new and already-known TODOs
    current_todo_set = set(current_todos.values())
    new_todos = {}
    known_todos = {}

    for location, todo_text in current_todos.items():
        if todo_text in known:
            known_todos[location] = todo_text
        else:
            new_todos[location] = todo_text

    # Generate brief
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "="*70)
    print(" "*20 + "MORNING BRIEF")
    print("="*70)
    print(f"Generated: {timestamp}")
    print(f"Previous runs: {len(spine_data['run_history'])}")
    print("="*70)

    print(f"\nREPOSITORY STATUS")
    print(f"   Total TODOs found: {len(current_todos)}")
    print(f"   Already known: {len(known_todos)}")
    print(f"   New discoveries: {len(new_todos)}")

    if new_todos:
        print(f"\n[NEW] TODOs not in previous runs:")
        for location, todo_text in sorted(new_todos.items()):
            print(f"   * {location}")
            print(f"     -> {todo_text}")
    else:
        print(f"\n[OK] No new TODOs since last run")

    if known_todos:
        print(f"\n[TRACKED] Already known ({len(known_todos)} items):")
        for location, todo_text in sorted(list(known_todos.items())[:3]):
            print(f"   * {location}: {todo_text}")
        if len(known_todos) > 3:
            print(f"   ... and {len(known_todos) - 3} more")

    print("\n" + "="*70)

    return new_todos, known_todos


def update_spine(new_todos, all_todos):
    """
    Update progress.md with new run information
    Preserves history instead of overwriting
    """
    spine_file = Path("progress.md")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read existing content
    existing_content = ""
    if spine_file.exists():
        existing_content = spine_file.read_text(encoding='utf-8')

    # Create new run entry
    new_entry = f"""
---

## Run: {timestamp}

### Summary
- Total TODOs found: {len(all_todos)}
- New TODOs this run: {len(new_todos)}
- Previously known: {len(all_todos) - len(new_todos)}

"""

    if new_todos:
        new_entry += "### New Discoveries\n"
        for location, todo_text in sorted(new_todos.items()):
            new_entry += f"- `{todo_text}` - {location}\n"
        new_entry += "\n"

    new_entry += "### All TODOs (Cumulative)\n"
    for location, todo_text in sorted(all_todos.items()):
        new_entry += f"- `{todo_text}` - {location}\n"

    # Append to existing content
    if existing_content:
        updated_content = existing_content + new_entry
    else:
        # First run - create initial structure
        updated_content = f"""# Morning Brief - Progress Spine

This file serves as persistent memory (Concept 12) between scheduled runs.
Each run appends its findings here instead of starting from scratch.

{new_entry}
"""

    spine_file.write_text(updated_content, encoding='utf-8')
    print(f"\n[SAVED] Updated progress.md (spine)")


def main():
    """
    Main morning brief job
    """
    print("\n[MORNING BRIEF] Starting Morning Brief Job...")

    # STEP 1: Read persistent memory (spine)
    print("\n[SPINE] Reading persistent memory from progress.md...")
    spine_data = read_spine()
    print(f"   Loaded {len(spine_data['known_todos'])} previously known TODOs")

    # STEP 2: Scan repository for TODOs
    print("\n[SCAN] Scanning repository for TODOs...")
    current_todos = find_todos_in_repo()
    print(f"   Found {len(current_todos)} TODO comments")

    # STEP 3: Generate brief (compare with spine)
    new_todos, known_todos = generate_brief(spine_data, current_todos)

    # STEP 4: Update spine
    update_spine(new_todos, current_todos)

    print(f"\n[COMPLETE] Morning Brief complete!\n")


if __name__ == "__main__":
    main()
