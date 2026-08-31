"""
TestLoop - Conditional Loop Controller
Demonstrates Concept 5 (run-until-done loop) and Concept 11 (maker-checker separation)

The MAKER (this script) fixes code.
The CHECKER (pytest) independently verifies completion.
The CONTROLLER (this script's loop logic) decides when to stop based on pytest results.
"""
import subprocess
import sys
import os


def run_pytest():
    """
    CHECKER: Run pytest and return results
    This is the independent authority that decides if work is complete
    """
    print("\n" + "="*60)
    print("CHECKER: Running pytest...")
    print("="*60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test_calculator.py", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    # Parse results
    passed = result.stdout.count(" PASSED")
    failed = result.stdout.count(" FAILED")

    print(f"\nCHECKER RESULT: {passed} passed, {failed} failed")
    print(f"Exit code: {result.returncode}")

    return {
        "success": result.returncode == 0,
        "exit_code": result.returncode,
        "passed": passed,
        "failed": failed,
        "output": result.stdout + result.stderr
    }


def analyze_and_fix(attempt_num, test_output):
    """
    MAKER: Analyze test failures and fix the implementation
    """
    print("\n" + "="*60)
    print(f"MAKER: Analyzing failures for attempt {attempt_num}...")
    print("="*60)

    with open("calculator.py", 'r') as f:
        code = f.read()

    # Track what we fix
    fix_applied = None

    # Fix 1: add function (wrong operator)
    if "return a - b" in code and "def add" in code:
        print("MAKER: Found bug in add() - using subtraction instead of addition")
        code = code.replace(
            "def add(a, b):\n    \"\"\"Add two numbers\"\"\"\n    # BUG: Wrong operator\n    return a - b",
            "def add(a, b):\n    \"\"\"Add two numbers\"\"\"\n    return a + b"
        )
        fix_applied = "Fixed add() function: Changed - to +"
        print(f"MAKER: Applied fix - {fix_applied}")

    # Fix 2: multiply function (missing return)
    elif "result = a * b" in code and "def multiply" in code and "return a * b" not in code:
        print("MAKER: Found bug in multiply() - missing return statement")
        code = code.replace(
            "def multiply(a, b):\n    \"\"\"Multiply two numbers\"\"\"\n    # BUG: Missing return statement\n    result = a * b",
            "def multiply(a, b):\n    \"\"\"Multiply two numbers\"\"\"\n    return a * b"
        )
        fix_applied = "Fixed multiply() function: Added return statement"
        print(f"MAKER: Applied fix - {fix_applied}")

    # Fix 3: divide function (no zero check)
    elif "def divide(a, b):" in code and "if b == 0:" not in code:
        print("MAKER: Found bug in divide() - missing zero division check")
        code = code.replace(
            "def divide(a, b):\n    \"\"\"Divide two numbers\"\"\"\n    # BUG: No zero division check\n    return a / b",
            "def divide(a, b):\n    \"\"\"Divide two numbers\"\"\"\n    if b == 0:\n        raise ZeroDivisionError(\"Cannot divide by zero\")\n    return a / b"
        )
        fix_applied = "Fixed divide() function: Added zero division check"
        print(f"MAKER: Applied fix - {fix_applied}")

    else:
        fix_applied = "No new fixes applied (all known bugs already fixed)"
        print(f"MAKER: {fix_applied}")

    # Write the fixed code
    with open("calculator.py", 'w') as f:
        f.write(code)

    return fix_applied


def main():
    """
    CONTROLLER: Main conditional loop
    Runs until pytest passes OR max attempts reached
    """
    MAX_ATTEMPTS = 6

    print("\n" + "="*70)
    print(" "*20 + "TESTLOOP DEMONSTRATION")
    print("="*70)
    print("Concept 5: Conditional Loop (run-until-done)")
    print("Concept 11: Maker-Checker Separation")
    print("="*70)
    print(f"\nMax attempts: {MAX_ATTEMPTS}")
    print("Stopping condition: pytest must pass (exit code 0)")
    print("\n" + "="*70)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n{'='*70}")
        print(f" ATTEMPT {attempt} / {MAX_ATTEMPTS}")
        print('='*70)

        # STEP 1: CHECKER runs pytest (independent verification)
        test_result = run_pytest()

        # CONTROLLER DECISION: Check if tests passed
        if test_result["success"]:
            print("\n" + "="*70)
            print(" "*15 + "[SUCCESS] LOOP COMPLETED SUCCESSFULLY")
            print("="*70)
            print(f"\nStopping reason: VERIFIED - All tests passed on attempt {attempt}")
            print("The CHECKER (pytest) confirmed completion.")
            print(f"Exit code: {test_result['exit_code']}")
            print(f"Tests: {test_result['passed']} passed, {test_result['failed']} failed")
            print("\nThe maker-checker pattern ensured:")
            print("- MAKER fixed the implementation")
            print("- CHECKER independently verified correctness")
            print("- CONTROLLER stopped based on checker's result")
            print("="*70)
            return 0

        # Tests failed - continue to next attempt
        print(f"\nCONTROLLER: Tests failed. Continuing to fix...")

        # STEP 2: MAKER analyzes and fixes
        fix_description = analyze_and_fix(attempt, test_result["output"])

        # Check if we've reached max attempts
        if attempt == MAX_ATTEMPTS:
            print("\n" + "="*70)
            print(" "*15 + "[FAILED] LOOP STOPPED - MAX ATTEMPTS REACHED")
            print("="*70)
            print(f"\nStopping reason: Maximum {MAX_ATTEMPTS} attempts reached")
            print("Completion was NOT proven - tests still failing")
            print(f"Final state: {test_result['passed']} passed, {test_result['failed']} failed")
            print("\nThe conditional loop correctly:")
            print("- Did NOT claim success when tests failed")
            print("- Stopped at the attempt cap")
            print("- Reported failure clearly")
            print("="*70)
            return 1

        print(f"\nCONTROLLER: Proceeding to attempt {attempt + 1}...")

    return 1


if __name__ == "__main__":
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    exit_code = main()
    sys.exit(exit_code)
