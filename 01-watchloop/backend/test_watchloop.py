"""
Test Script - Comprehensive end-to-end testing of WatchLoop
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

def start_task(duration=60):
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

def run_tests():
    """Run comprehensive tests"""
    print_header("WATCHLOOP END-TO-END TESTING")

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

    # Test 3: Start task
    print_header("TEST 3: Start Task (60 second duration)")
    task_result = start_task(60)
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
        if watcher_status == "active":
            print_status("PASS", "Watcher is active")
            results["passed"].append("Watcher active")
        else:
            print_status("FAIL", f"Watcher status: {watcher_status}")
            results["failed"].append("Watcher active")

    # Test 5: Monitor checks over time
    print_header("TEST 5: Monitor Status Checks (waiting 70 seconds)")
    print_status("INFO", "Waiting for at least one check cycle (60s interval)...")

    initial_status = get_status()
    initial_check_count = initial_status["data"]["watcher"]["check_count"] if initial_status else 0

    # Wait 70 seconds to ensure at least one check happens
    for i in range(70):
        time.sleep(1)
        if (i + 1) % 10 == 0:
            status = get_status()
            if status and status.get("success"):
                check_count = status["data"]["watcher"]["check_count"]
                task_status = status["data"]["task"]["status"]
                print_status("INFO", f"{i+1}s elapsed - Checks: {check_count}, Task: {task_status}")

    final_status = get_status()
    if final_status and final_status.get("success"):
        final_check_count = final_status["data"]["watcher"]["check_count"]
        if final_check_count > initial_check_count:
            print_status("PASS", f"Status checks occurred ({initial_check_count} -> {final_check_count})")
            results["passed"].append("Status checks occur")
        else:
            print_status("FAIL", f"No status checks detected")
            results["failed"].append("Status checks occur")

    # Test 6: Wait for completion
    print_header("TEST 6: Wait for Task Completion")
    print_status("INFO", "Task should complete soon (60s total duration)...")

    completion_detected = False
    watcher_stopped = False
    max_wait = 30  # Additional 30 seconds

    for i in range(max_wait):
        time.sleep(1)
        status = get_status()

        if status and status.get("success"):
            data = status["data"]
            task_status = data["task"]["status"]
            watcher_status = data["watcher"]["status"]
            completion_notified = data["watcher"]["completion_notified"]

            # Check for completion event
            events = data.get("events", [])
            completion_events = [e for e in events if e["type"] == "completion_detected"]

            if task_status in ["finished", "failed", "cancelled"]:
                print_status("PASS", f"Task completed with status: {task_status}")

                if completion_events:
                    print_status("PASS", f"Completion notification found: {completion_events[-1]['message']}")
                    completion_detected = True

                    # Verify single notification
                    if len(completion_events) == 1:
                        print_status("PASS", "Completion notified EXACTLY ONCE")
                        results["passed"].append("Single completion notification")
                    else:
                        print_status("FAIL", f"Multiple completion notifications detected: {len(completion_events)}")
                        results["failed"].append("Single completion notification")

                if watcher_status == "stopped" and completion_notified:
                    print_status("PASS", "Watcher stopped after completion")
                    watcher_stopped = True

                results["passed"].append("Task completion detected")
                results["passed"].append("Watcher stopped after completion")
                break

        if (i + 1) % 5 == 0:
            print_status("INFO", f"Still waiting... {i+1}s")

    if not completion_detected:
        print_status("FAIL", "Completion was not detected")
        results["failed"].append("Task completion detected")

    if not watcher_stopped:
        print_status("FAIL", "Watcher did not stop")
        results["failed"].append("Watcher stopped after completion")

    # Test 7: Test manual stop (after reset)
    print_header("TEST 7: Test Manual Watcher Stop")
    reset_system()
    time.sleep(2)

    start_task(300)  # Long task
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

    # Test 8: Final reset
    print_header("TEST 8: Final System Reset")
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
        exit_code = run_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nTest suite error: {e}")
        sys.exit(1)
