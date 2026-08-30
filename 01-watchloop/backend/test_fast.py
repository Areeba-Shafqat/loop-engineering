"""
Fast Test Script - Quick validation with reduced intervals
"""
import time
import requests
import sys

API_BASE = "http://localhost:5000/api"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_status(label, value):
    print(f"  [{label}] {value}")

def get_status():
    """Fetch current status"""
    try:
        response = requests.get(f"{API_BASE}/status", timeout=5)
        return response.json()
    except Exception as e:
        print_status("ERROR", f"Failed to get status: {e}")
        return None

def start_task(duration=15):
    """Start a task"""
    try:
        response = requests.post(
            f"{API_BASE}/start-task",
            json={"duration": duration},
            timeout=5
        )
        return response.json()
    except Exception as e:
        print_status("ERROR", f"Failed to start task: {e}")
        return None

def stop_watcher():
    """Stop the watcher"""
    try:
        response = requests.post(f"{API_BASE}/stop-watcher", timeout=5)
        return response.json()
    except Exception as e:
        print_status("ERROR", f"Failed to stop watcher: {e}")
        return None

def reset_system():
    """Reset the system"""
    try:
        response = requests.post(f"{API_BASE}/reset", timeout=5)
        return response.json()
    except Exception as e:
        print_status("ERROR", f"Failed to reset: {e}")
        return None

def run_fast_tests():
    """Run fast tests with reduced wait times"""
    print_header("WATCHLOOP FAST TEST MODE")
    print_status("NOTE", "Using 15s task duration for quick validation")
    print_status("NOTE", "Watcher still checks every 60s (production setting)")

    results = {
        "passed": [],
        "failed": []
    }

    # Test 1: Reset system
    print_header("TEST 1: Reset System")
    reset_result = reset_system()
    if reset_result and reset_result.get("success"):
        print_status("PASS", "System reset successful")
        results["passed"].append("Reset system")
    else:
        print_status("FAIL", "System reset failed")
        results["failed"].append("Reset system")
        return results

    time.sleep(2)

    # Test 2: Verify initial state
    print_header("TEST 2: Verify Initial State")
    status = get_status()
    if status and status.get("success"):
        data = status["data"]
        task_status = data["task"]["status"]
        watcher_status = data["watcher"]["status"]

        if task_status == "idle" and watcher_status == "stopped":
            print_status("PASS", f"Task: {task_status}, Watcher: {watcher_status}")
            results["passed"].append("Initial state correct")
        else:
            print_status("FAIL", f"Unexpected state - Task: {task_status}, Watcher: {watcher_status}")
            results["failed"].append("Initial state correct")
    else:
        print_status("FAIL", "Failed to get status")
        results["failed"].append("Initial state correct")

    # Test 3: Start task with short duration
    print_header("TEST 3: Start Task (15 second duration)")
    task_result = start_task(15)
    if task_result and task_result.get("success"):
        print_status("PASS", "Task started successfully")
        print_status("INFO", f"Watcher auto-started: {task_result.get('watcher_started')}")
        results["passed"].append("Start task")
    else:
        print_status("FAIL", "Task start failed")
        results["failed"].append("Start task")
        return results

    time.sleep(2)

    # Test 4: Verify watcher is active
    print_header("TEST 4: Verify Watcher Active")
    status = get_status()
    if status and status.get("success"):
        watcher_status = status["data"]["watcher"]["status"]
        task_status = status["data"]["task"]["status"]
        if watcher_status == "active":
            print_status("PASS", f"Watcher is active, task is {task_status}")
            results["passed"].append("Watcher active")
        else:
            print_status("FAIL", f"Watcher status: {watcher_status}")
            results["failed"].append("Watcher active")

    # Test 5: Wait for task completion and watcher detection
    print_header("TEST 5: Wait for Task Completion (monitoring)")
    print_status("INFO", "Waiting for task to complete and watcher to detect (15s task + check cycles)...")

    completion_detected = False
    watcher_stopped = False
    task_completed = False
    max_wait = 40  # 15s task + up to 25s for watcher detection

    for i in range(max_wait):
        time.sleep(1)
        status = get_status()

        if status and status.get("success"):
            data = status["data"]
            task_status = data["task"]["status"]
            watcher_status = data["watcher"]["status"]
            completion_notified = data["watcher"]["completion_notified"]
            check_count = data["watcher"]["check_count"]

            # Check for completion event
            events = data.get("events", [])
            completion_events = [e for e in events if e["type"] == "completion_detected"]

            if (i + 1) % 5 == 0:
                print_status("INFO", f"{i+1}s elapsed - Task: {task_status}, Checks: {check_count}, Watcher: {watcher_status}")

            # First, detect when task completes
            if task_status in ["finished", "failed", "cancelled"] and not task_completed:
                print_status("PASS", f"Task completed with status: {task_status} at {i+1}s")
                results["passed"].append("Task completion detected")
                task_completed = True

            # Then wait for watcher to detect it
            if task_completed and completion_events and not completion_detected:
                print_status("PASS", f"Watcher detected completion: {completion_events[-1]['message']}")
                completion_detected = True

                # Verify single notification
                if len(completion_events) == 1:
                    print_status("PASS", "Completion notified EXACTLY ONCE")
                    results["passed"].append("Single completion notification")
                else:
                    print_status("FAIL", f"Multiple notifications: {len(completion_events)}")
                    results["failed"].append("Single completion notification")

            # Check if watcher stopped properly
            if completion_detected and watcher_status == "stopped" and completion_notified and not watcher_stopped:
                print_status("PASS", "Watcher stopped after completion")
                results["passed"].append("Watcher stopped after completion")
                watcher_stopped = True

            # Once everything is complete, check for status checks
            if watcher_stopped:
                if check_count > 0:
                    print_status("PASS", f"Watcher performed {check_count} status check(s)")
                    results["passed"].append("Status checks occurred")
                else:
                    print_status("FAIL", "No status checks performed")
                    results["failed"].append("Status checks occurred")
                break

    if not task_completed:
        print_status("FAIL", "Task did not complete within timeout")
        results["failed"].append("Task completion detected")

    if task_completed and not completion_detected:
        print_status("FAIL", "Watcher did not detect completion within timeout")
        results["failed"].append("Completion notification exists")

    if completion_detected and not watcher_stopped:
        print_status("FAIL", "Watcher did not stop after detecting completion")
        results["failed"].append("Watcher stopped after completion")

    # Test 6: Test manual stop (after reset)
    print_header("TEST 6: Test Manual Watcher Stop")
    reset_system()
    time.sleep(2)

    start_task(60)  # Longer task
    time.sleep(3)

    stop_result = stop_watcher()
    if stop_result and stop_result.get("success"):
        print_status("PASS", "Watcher stopped manually")

        status = get_status()
        if status and status["data"]["watcher"]["status"] == "stopped":
            print_status("PASS", "Watcher status confirmed stopped")
            results["passed"].append("Manual watcher stop")
        else:
            print_status("FAIL", "Watcher status not updated")
            results["failed"].append("Manual watcher stop")
    else:
        print_status("FAIL", "Manual stop failed")
        results["failed"].append("Manual watcher stop")

    # Test 7: Final reset
    print_header("TEST 7: Final System Reset")
    reset_result = reset_system()
    if reset_result and reset_result.get("success"):
        print_status("PASS", "Final reset successful")
        results["passed"].append("Reset functionality")
    else:
        print_status("FAIL", "Final reset failed")
        results["failed"].append("Reset functionality")

    # Summary
    print_header("TEST SUMMARY")
    print(f"\n  PASSED: {len(results['passed'])} tests")
    for test in results["passed"]:
        print(f"    + {test}")

    print(f"\n  FAILED: {len(results['failed'])} tests")
    for test in results["failed"]:
        print(f"    - {test}")

    print_header("FINAL VERDICT")
    if not results["failed"]:
        print_status("SUCCESS", "All tests passed!")
        return 0
    else:
        print_status("FAILURE", f"{len(results['failed'])} test(s) failed")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_fast_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nTest suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
