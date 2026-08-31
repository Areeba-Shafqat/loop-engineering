## Project 4: FixLoop - PR Creation Evidence

### Good Fix PR - OPENED ✅

**Branch**: `fix/good-calculator-bugs`  
**Reviewer Verdict**: PASS  
**PR Status**: CREATED

**Create PR at**: https://github.com/Areeba-Shafqat/loop-engineering/pull/new/fix/good-calculator-bugs

**PR Title**: Fix calculator bugs: Handle zero division properly

**PR Body**:
```markdown
# Fix Calculator Bugs: Handle Zero Division Properly

## Summary
This PR fixes two bugs in the calculator module where functions raised the wrong exception type for edge cases.

## Bugs Fixed

### Bug 1: divide() - Wrong Exception Type
**Before:** Raised `ZeroDivisionError` when dividing by zero  
**After:** Raises `ValueError("Cannot divide by zero")`

### Bug 2: average() - Wrong Exception Type  
**Before:** Raised `ZeroDivisionError` on empty list  
**After:** Raises `ValueError("Cannot calculate average of empty list")`

## Changes Made
- Added validation in `divide()` to check if `b == 0` before dividing
- Added validation in `average()` to check if list is empty before calculating
- Updated docstrings with proper Args, Returns, and Raises sections

## Test Results
All 7 tests pass:
- test_divide_by_zero_raises_value_error PASSED ✓
- test_average_empty_list_raises_value_error PASSED ✓
- All other tests PASSED

## Independent Review
**Reviewer Verdict: PASS**

**Reasoning:**
1. ✅ Both bugs addressed completely
2. ✅ Error messages match requirements exactly
3. ✅ Implementation correct with proper validation
4. ✅ All 7 tests pass including both regression tests
5. ✅ No regressions introduced
6. ✅ Fix is minimal and focused

## Maker-Checker Verification
- ✅ Implementer fixed bugs in isolated branch
- ✅ Independent reviewer evaluated the fix
- ✅ Reviewer returned PASS verdict
- ✅ PR opened only after PASS received

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

### Bad Fix PR - NOT OPENED ❌

**Branch**: `fix/bad-calculator-bugs`  
**Reviewer Verdict**: FAIL  
**PR Status**: NOT CREATED (blocked by FAIL verdict)

**Why PR was NOT created:**

Independent reviewer returned **FAIL** with the following reasons:

**VERDICT: FAIL**

**REASONING:**
1. ❌ INCOMPLETE: Only 1 of 2 bugs fixed
   - divide() correctly raises ValueError ✓
   - average() still raises ZeroDivisionError ✗
2. ❌ Test failure: test_average_empty_list_raises_value_error still fails
3. ❌ Does not meet requirements: Bug report specified BOTH functions must be fixed
4. ❌ Still has the original bug in average()
5. ❌ Cannot merge: Would leave known bug in codebase

**SPECIFIC ISSUES:**
- Line 41 in calculator.py: `return sum(numbers) / len(numbers)` still raises ZeroDivisionError on empty list
- Missing validation: No check for `if not numbers:` before calculating average
- Test output shows: "ZeroDivisionError: division by zero" instead of required "ValueError: Cannot calculate average of empty list"

**Test Results**: 1 failed, 6 passed

The PR gate correctly blocked this incomplete fix from being merged.

---

## PR Gate Enforcement Summary

✅ **Good fix → PASS → PR OPENED**  
❌ **Bad fix → FAIL → NO PR OPENED**

This demonstrates Concept 11 (Maker-Checker Separation) working correctly.
