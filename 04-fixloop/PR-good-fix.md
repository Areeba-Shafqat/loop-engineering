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
- Both functions now raise meaningful ValueError exceptions with clear messages

## Test Results

All 7 tests pass:
```
test_calculator.py::TestBasicOperations::test_add PASSED
test_calculator.py::TestBasicOperations::test_subtract PASSED
test_calculator.py::TestBasicOperations::test_multiply PASSED
test_calculator.py::TestDivide::test_divide_normal PASSED
test_calculator.py::TestDivide::test_divide_by_zero_raises_value_error PASSED ✓
test_calculator.py::TestAverage::test_average_normal PASSED
test_calculator.py::TestAverage::test_average_empty_list_raises_value_error PASSED ✓
```

Both regression tests now pass (marked with ✓).

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

This PR demonstrates **Concept 11: Maker-Checker Separation**:
- ✅ Implementer fixed bugs in isolated branch
- ✅ Independent reviewer evaluated the fix
- ✅ Reviewer returned PASS verdict
- ✅ PR opened only after PASS received

## Concepts Demonstrated

- **Concept 8**: Branch isolation (worked in `fix/good-calculator-bugs`)
- **Concept 9**: Reusable skill (followed fix-bug-skill.md procedure)
- **Concept 11**: Maker-checker separation (independent review required)

---

**Implementer**: Claude (maker)  
**Reviewer**: Independent reviewer agent (checker)  
**Review Status**: ✅ PASS - Ready to merge

🤖 Generated with [Claude Code](https://claude.com/claude-code)
