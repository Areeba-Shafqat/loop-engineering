# Project 04: FixLoop - Maker-Checker Bug Fix Workflow

## 🎯 Overview

FixLoop demonstrates **Concept 8** (Worktree/Branch Isolation), **Concept 9** (Reusable Skills), and **Concept 11** (Maker-Checker Separation). It implements a workflow where an implementer fixes bugs in isolation, and an independent reviewer must approve the fix before a PR can be opened.

## 🏗️ Core Concepts

### Concept 8: Worktree/Branch Isolation

Work on fixes in isolated Git branches or worktrees to avoid affecting the main codebase.

**Key characteristics:**
- Changes are isolated from main branch
- Multiple fixes can be worked on independently
- Easy to discard failed attempts
- Safe experimentation without risk

**In FixLoop:**
- Implementer works in dedicated fix branches
- Main branch remains stable during development
- Each fix attempt is fully isolated

### Concept 9: Reusable Skills

Skills are reusable procedures that codify best practices for common tasks.

**Key characteristics:**
- Documented, repeatable procedures
- Can be invoked by name
- Encapsulate domain knowledge
- Reduce cognitive load

**In FixLoop:**
- `.claude/skills/fix-bug/SKILL.md` defines the fix procedure
- Standardizes approach across all bug fixes
- Ensures consistent quality

### Concept 11: Maker-Checker Separation

The person who implements work (maker) cannot approve their own work (checker).

**Key characteristics:**
- Implementer and reviewer are independent
- Prevents self-approval bias
- Catches mistakes before merge
- Enforces objective quality gates

**In FixLoop:**
- Implementer fixes bugs but cannot approve
- Separate reviewer agent evaluates independently
- PR only opens after reviewer PASS verdict
- FAIL verdict blocks PR creation

## 📁 Project Structure

```
04-fixloop/
├── calculator.py           # Module with bugs (then fixed)
├── test_calculator.py      # Tests demonstrating bugs
├── README.md              # This file
└── (branches for fixes)
```

## 🐛 The Bugs

The calculator module has two bugs related to error handling:

### Bug 1: divide() - Wrong Exception Type
**Expected**: `ValueError("Cannot divide by zero")`  
**Actual**: `ZeroDivisionError`

### Bug 2: average() - Wrong Exception Type
**Expected**: `ValueError("Cannot calculate average of empty list")`  
**Actual**: `ZeroDivisionError`

Both bugs are real, reproducible issues with failing regression tests.

## 🔄 The Workflow

### 1. Implementer (Maker)

The implementer:
1. Works in isolated branch (`fix/good-calculator-bugs`)
2. Reproduces the bugs (runs failing tests)
3. Implements the fix
4. Runs tests to verify fix works
5. Commits changes
6. Submits to reviewer

**The implementer NEVER:**
- Approves their own fix
- Opens PR without reviewer PASS
- Modifies tests to pass

### 2. Independent Reviewer (Checker)

The reviewer agent:
1. Receives the diff and test evidence
2. Evaluates against original bug requirements
3. Checks implementation correctness
4. Verifies test coverage
5. Returns `PASS` or `FAIL` with reasoning

**The reviewer NEVER:**
- Trusts implementer's claims without verification
- Edits the implementation
- Passes incomplete fixes

### 3. PR Gate

- Reviewer = `PASS` → PR may be opened
- Reviewer = `FAIL` → PR must NOT be opened

## 🧪 Two-Scenario Demonstration

### Scenario 1: Good Fix (PASS)

**Implementer Actions:**
```bash
# Create isolated branch
git checkout -b fix/good-calculator-bugs

# Implement correct fix
# - divide(): Add check for b == 0
# - average(): Add check for empty list

# Run tests
pytest test_calculator.py -v
# Result: 7 passed
```

**Reviewer Evaluation:**
- Reviews diff showing proper zero/empty checks
- Confirms error messages match requirements
- Verifies all tests pass
- Returns: `PASS` ✅

**Outcome:**
✅ PR opened: "Fix calculator bugs: Handle zero division properly"

### Scenario 2: Bad Fix (FAIL)

**Implementer Actions:**
```bash
# Create isolated branch
git checkout -b fix/bad-calculator-bugs

# Implement INCORRECT fix (deliberately)
# - Only fixes divide(), ignores average()
# OR
# - Wrong error message
# OR
# - Incomplete validation

# Run tests
pytest test_calculator.py -v
# Result: Tests still fail or wrong behavior
```

**Reviewer Evaluation:**
- Reviews diff
- Identifies missing fix for average()
- Confirms fix is incomplete
- Returns: `FAIL` ❌ with specific reasons

**Outcome:**
❌ NO PR opened - fix must be corrected first

## ✅ Acceptance Criteria Verification

- [x] **Real reproducible bug exists** - Two bugs with failing tests
- [x] **Implementer uses isolated branch** - `fix/good-calculator-bugs`
- [x] **Reusable skill exists** - `.claude/skills/fix-bug/SKILL.md`
- [x] **Implementer fixes the bug** - Both divide() and average() fixed
- [x] **Regression tests exist** - test_divide_by_zero, test_average_empty_list
- [x] **Separate reviewer agent exists** - Independent evaluation
- [x] **Reviewer evaluates independently** - Does not trust claims
- [ ] **Good fix receives PASS** - Pending reviewer verdict
- [ ] **Good fix produces PR** - After PASS received
- [ ] **Bad fix receives FAIL** - To be demonstrated
- [ ] **Bad fix produces no PR** - After FAIL received
- [ ] **PR gated by PASS** - Enforced by workflow
- [x] **README explains concepts** - This document
- [ ] **Both scenarios run** - In progress

## 🔑 Key Learnings

### Concept 8: Isolation

**Benefits:**
- Safe experimentation
- Parallel work streams
- Easy rollback
- No main branch pollution

**Implementation:**
- Use dedicated branches
- Keep changes focused
- Clean up after merge

### Concept 9: Reusable Skills

**Benefits:**
- Consistent quality
- Reduced training time
- Best practices codified
- Easy to improve over time

**Implementation:**
- Document procedures clearly
- Make skills discoverable
- Keep skills focused

### Concept 11: Maker-Checker

**Benefits:**
- Catches mistakes early
- Reduces bias
- Enforces quality standards
- Builds confidence

**Implementation:**
- Independent reviewer required
- Explicit PASS/FAIL gate
- No self-approval
- Specific failure reasons

## 🚨 Safety Rules

1. **Never merge without review PASS**
2. **Never weaken tests to pass**
3. **Never bypass the reviewer gate**
4. **Never self-approve fixes**
5. **Always work in isolated branches**
6. **Preserve main branch integrity**

## 🎓 Portfolio Value

This project demonstrates:
- Systematic bug fixing workflow
- Maker-checker separation pattern
- Independent code review
- Branch-based isolation
- Test-driven validation
- Quality gate enforcement
- Professional software practices

---

**Author**: Areeba Shafqat  
**Date**: 2026-08-31  
**Concepts**: Worktree Isolation, Reusable Skills, Maker-Checker Separation
