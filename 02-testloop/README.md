# Project 02: TestLoop

## 🎯 Overview

TestLoop is a demonstration of **Concept 5** (Conditional/Run-Until-Done Loop) and **Concept 11** (Maker-Checker Separation). This project shows how an AI worker can iteratively fix code until tests pass, with an independent test runner as the authority on completion.

## 🏗️ Core Concepts

### Concept 5: Conditional Loop (Run-Until-Done)

A conditional loop runs repeatedly until a specific condition is met, rather than for a fixed number of iterations.

In TestLoop:
- The loop continues while tests are failing
- The loop stops immediately when tests pass
- There's a maximum cap (6 attempts) to prevent infinite loops
- The stopping condition is externally verified, not self-declared

### Concept 11: Maker-Checker Separation

The maker-checker pattern separates the entity that does work from the entity that verifies the work is correct.

In TestLoop:
- **MAKER**: The loop controller that analyzes failures and fixes code
- **CHECKER**: pytest - an independent test runner that verifies correctness
- **CONTROLLER**: Loop logic that decides when to stop based on the checker's result

**Key principle**: The maker cannot approve its own work. Only the independent checker can declare completion.

## 📁 Project Structure

```
02-testloop/
├── calculator.py          # Implementation (initially buggy)
├── test_calculator.py     # Test suite (must NOT be modified)
├── loop_controller.py     # Main loop demonstrating Concept 5 & 11
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🧪 The Demo

### Initial State
The `calculator.py` file contains **intentional bugs**:
1. `add()` uses subtraction instead of addition
2. `multiply()` missing return statement
3. `divide()` doesn't check for division by zero

### Test Suite
`test_calculator.py` contains 3 tests:
- `test_add()` - Tests addition (initially fails)
- `test_multiply()` - Tests multiplication (initially fails)  
- `test_divide()` - Tests division including zero check (initially passes, will fail after fixes when zero check is tested)

**IMPORTANT**: These tests must NEVER be modified during the loop. They are the immutable acceptance criteria.

### The Loop

1. **CHECKER**: Run pytest
2. **EVALUATE**: Check if all tests passed
3. **If passed**: Stop immediately and report success
4. **If failed**: 
   - MAKER analyzes test output
   - MAKER fixes one bug in the implementation
   - Repeat from step 1
5. **Cap**: Maximum 6 attempts

## 🚀 Running the Demo

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Loop
```bash
cd 02-testloop
python loop_controller.py
```

### Expected Output
You should see:
- Each attempt clearly labeled
- pytest output showing which tests pass/fail
- Maker's analysis and fixes
- Controller's decisions
- Final completion when tests pass

## ✅ Acceptance Criteria

- [x] 2-3 meaningful tests exist
- [x] Tests initially fail for genuine reasons
- [x] Implementation can be fixed to pass tests
- [x] Loop runs pytest after each fix
- [x] Loop continues while pytest fails
- [x] Loop stops immediately when pytest passes
- [x] Success is determined by pytest exit code, not maker's opinion
- [x] Maximum 6 attempts enforced
- [x] Tests are never modified to fake success
- [x] Pytest output is visible for verification
- [x] Concept 5 (conditional loop) demonstrated
- [x] Concept 11 (maker-checker) demonstrated

## 🎓 Key Learnings

1. **External Verification**: The checker (pytest) is independent and cannot be influenced by the maker
2. **Clear Stopping Condition**: Tests passing is the ONLY success condition
3. **Attempt Cap**: Prevents infinite loops when bugs can't be fixed
4. **Transparency**: All test output is visible for verification
5. **Immutable Criteria**: Tests define success and must not change

## ⚠️ Anti-Patterns Avoided

- ❌ Maker declaring its own work complete
- ❌ Modifying tests to make them pass
- ❌ Claiming success when attempt cap is reached
- ❌ Hidden test results
- ❌ Weakening acceptance criteria

## 🔍 Verification

To verify this project works correctly:

1. Check initial state - tests should fail:
   ```bash
   python -m pytest test_calculator.py -v
   ```

2. Run the loop:
   ```bash
   python loop_controller.py
   ```

3. Verify:
   - Loop attempts to fix bugs
   - pytest output is shown each attempt
   - Loop stops when tests pass
   - Final message confirms pytest verification

## 📊 Example Successful Run

```
Attempt 1: 2 failed, 1 passed → Fix add()
Attempt 2: 1 failed, 2 passed → Fix multiply()  
Attempt 3: 0 failed, 3 passed → ✅ VERIFIED - Stop
```

## 🎯 Portfolio Value

This project demonstrates:
- Understanding of software verification patterns
- Ability to separate concerns (maker vs checker)
- Implementation of conditional control flow
- Test-driven development principles
- Clean, maintainable code structure
- Professional documentation

---

**Author**: Areeba Shafqat  
**Date**: 2026-08-30  
**Concepts**: Conditional Loops, Maker-Checker Separation
