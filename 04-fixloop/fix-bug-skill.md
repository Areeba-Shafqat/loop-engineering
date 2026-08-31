# Fix Bug Skill

This skill implements a maker-checker workflow for fixing bugs using isolated Git worktrees/branches.

## Procedure

### 1. Understand the Bug
- Read the bug description or issue
- Identify the expected behavior
- Identify the actual (incorrect) behavior
- Determine the scope of the fix

### 2. Reproduce the Problem
- Run existing tests that demonstrate the bug
- Capture the failure output
- Confirm the bug is reproducible
- Document the reproduction steps

### 3. Set Up Isolated Branch/Worktree
- Create a new Git branch or worktree for the fix
- Use a descriptive name (e.g., `fix/divide-by-zero`)
- Work in isolation to avoid affecting the main branch
- This demonstrates **Concept 8: Worktree/Branch isolation**

### 4. Locate Relevant Code
- Find the source file(s) containing the bug
- Identify the specific function(s) affected
- Review surrounding code for context
- Check for similar issues elsewhere

### 5. Implement the Fix
- Make the **smallest appropriate fix** that solves the problem
- Do not refactor unrelated code
- Preserve existing behavior for valid cases
- Add clear comments if the fix is non-obvious

### 6. Add/Update Regression Test
- Ensure a test exists that would catch this bug
- If no test exists, add one
- Run the test to confirm it fails before the fix
- Run the test to confirm it passes after the fix

### 7. Run Relevant Tests
- Run the full test suite (or relevant subset)
- Capture test output
- Confirm no regressions introduced
- Document test results

### 8. Prepare for Review
- Commit the changes with a clear message
- Collect evidence:
  - The diff
  - Test output showing the fix works
  - Reproduction steps
- Submit to independent reviewer
- **Never approve your own fix** (**Concept 11: Maker-Checker**)

### 9. Reviewer Decision Gate
- Wait for independent reviewer verdict
- Reviewer returns either `PASS` or `FAIL`
- If `PASS`: proceed to open PR
- If `FAIL`: address feedback and repeat from step 5

### 10. Open Pull Request
- **Only open PR after reviewer returns PASS**
- Include clear description of:
  - The bug
  - The fix
  - Test results
  - Reviewer verdict
- Link to any related issues

## Maker-Checker Separation (Concept 11)

**The implementer (maker) must never:**
- Approve their own work
- Override the reviewer's FAIL verdict
- Modify tests to make a bad fix pass
- Skip the review step

**The reviewer (checker) must:**
- Independently evaluate the fix
- Check that tests actually validate the fix
- Return FAIL if the fix is incorrect or incomplete
- Provide specific reasons for FAIL verdicts
- Never edit the implementation themselves

## Safety Rules

- Never merge to main without review
- Never weaken tests to pass
- Never bypass the reviewer gate
- Preserve main branch integrity
- Work in isolated branches/worktrees

---

This skill demonstrates:
- **Concept 8**: Worktree/branch isolation
- **Concept 9**: Reusable skill
- **Concept 11**: Maker-checker separation
