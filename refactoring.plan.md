# Overview

This project is a small pygame simulation where colored squares move inside a window, bounce on borders, flee from larger squares, and are replaced when their lifespan ends.

The code is functional and readable in many places, but there are beginner-friendly improvements that can make it easier to maintain:
- Naming consistency issues (for example, handle_chassing typo).
- One behavior function (handle_chassing) computes values but does not apply them.
- Some responsibilities are mixed inside large functions.
- A few magic numbers and duplicate patterns can be made clearer with helper functions/constants.
- The README and runtime values are out of sync (10 vs 20 squares).

# Refactoring Goals

1. Improve readability with clearer names and smaller helper functions.
2. Improve correctness by making chase behavior actually affect movement.
3. Reduce duplication in vector and normalization logic.
4. Preserve current program structure and gameplay flow (no full redesign).
5. Make future debugging easier through targeted inline comments.

# Step-by-Step Refactoring Plan

## Step 1: Add a Safety Baseline Before Refactoring

What to do:
- Run the program and note current behavior (spawn count, movement style, FPS display, flee behavior, lifespan replacement).
- Keep this baseline as a checklist so each later change can be verified.

Why this helps:
- Beginners can accidentally change behavior while cleaning code.
- A baseline makes it easier to confirm that refactoring improved code quality without breaking the simulation.

Inline comment requirement for final code:
- Add a short comment near the main loop describing which behaviors must remain unchanged after refactoring.
- Comment should explain that this is a behavior-preservation checkpoint.

Optional before/after snippet:
- Before: no explicit note about expected behavior.
- After: short comment in main() listing stable behaviors (movement, bounce, expiration, draw FPS).

## Step 2: Fix Naming Consistency and Typos

What to do:
- Rename handle_chassing to handle_chasing everywhere.
- Keep method/function names in one style (verb phrase + behavior).
- Optionally rename very short temporary names only when the new names are clearly easier for beginners.

Why this helps:
- Correct, consistent names reduce confusion and make search/navigation easier.
- Beginners learn faster when names match intent.

Inline comment requirement for final code:
- Add a short comment above the renamed function explaining that the rename improves discoverability and avoids typo-related confusion.

Optional before/after snippet:
Before: handle_chassing(squares)
After: handle_chasing(squares)

## Step 3: Complete Chase Behavior Without Changing Architecture

What to do:
- In the chase function, keep the current vector computation pattern.
- Actually apply the final chase direction to square.vx and square.vy (the missing assignment).
- Keep flee behavior and chase behavior order explicit and intentional.

Why this helps:
- The current chase logic computes direction but does not affect movement, which is a correctness gap.
- Completing this step aligns behavior with function intent.

Inline comment requirement for final code:
- Add a concise comment where velocity is assigned, explaining:
  - What changed (now writing vx, vy).
  - Why it improves correctness (chase logic now has visible effect).
  - Relevant concept (state mutation in a simulation loop).

## Step 4: Extract Tiny Vector Helper Functions

What to do:
- Add beginner-friendly helpers for repeated operations (for example normalize vector and compute distance).
- Replace duplicated math.hypot + divide-by-length patterns with helpers.
- Keep helpers simple and local to this file.

Why this helps:
- Reduces copy-paste math code and potential mistakes.
- Makes behavior functions shorter and easier to read.

Inline comment requirement for final code:
- Add a comment above each helper describing the programming concept (decomposition and code reuse).
- Add one short note about safe normalization (avoid division by zero).

Optional before/after snippet:
Before: repeated normalize blocks using length checks and division.
After: helper usage such as normalize_vector(x, y).

## Step 5: Simplify main() by Grouping Loop Phases

What to do:
- Keep one while running loop, but group it into clear phases in order:
  1) input/events,
  2) behavior update,
  3) movement/update lifespan,
  4) rendering.
- Optionally extract one small helper per phase if it stays beginner-friendly.

Why this helps:
- Students can mentally trace the frame lifecycle more easily.
- Debugging becomes simpler because each phase has one responsibility.

Inline comment requirement for final code:
- Add short phase comments in the loop explaining what each block does and why order matters.

## Step 6: Clarify Constants and Documentation Alignment

What to do:
- Keep constants centralized at the top.
- Ensure README matches runtime defaults (for example square count).
- Add brief, clear comments only for non-obvious constants (like milliseconds-based timing or behavior strength).

Why this helps:
- Prevents confusion between documentation and actual behavior.
- Makes tuning easier for experiments.

Inline comment requirement for final code:
- Add concise comments for constants that affect behavior feel (distance threshold, randomness strength, lifespan range), including why the constant exists.

## Step 7: Add Defensive Checks for Edge Cases (Lightweight)

What to do:
- Keep existing zero-distance safeguards.
- Add minimal guards where needed (for example when normalizing vectors) without overengineering.
- Avoid introducing advanced error-handling frameworks.

Why this helps:
- Prevents unstable movement from rare math edge cases.
- Teaches robust programming basics.

Inline comment requirement for final code:
- Add one-line comments at guards explaining what failure is prevented (for example division by zero).

## Step 8: Verify Refactor Incrementally

What to do:
- After each step, run the app and compare with Step 1 baseline.
- Confirm no regressions in:
  - window launch,
  - smooth movement,
  - border bounce,
  - flee/chase responses,
  - expiration replacement,
  - FPS display.

Why this helps:
- Incremental verification is safer than doing many changes at once.
- Builds debugging discipline for first-year students.

Inline comment requirement for final code:
- Add a small verification comment block near main() listing the key runtime checks used after refactoring.

# Final Output Requirements (Mandatory)

When this plan is executed, the output MUST:
- Contain only the refactored code.
- Include inline comments that explain:
  - what changed,
  - why the change improves readability/maintainability/correctness,
  - relevant programming concepts.
- Keep all inline explanations concise and beginner-friendly.
- Preserve original behavior as much as possible, except the intended chase-correction fix.

# Key Concepts for Students

- Single-responsibility thinking: each function should do one clear job.
- State mutation: changing vx, vy, x, y drives simulation behavior.
- Vector normalization: converting direction vectors to unit vectors safely.
- Time-based simulation: using delta time and tick timestamps instead of frame-count assumptions.
- Refactoring vs rewriting: improving internal code quality without changing core program structure.

# Safety Notes

- Test after every small step, not only at the end.
- Do not combine naming changes and behavior changes in one large edit.
- Keep fallback guards for zero-length vectors to avoid runtime math errors.
- Preserve the order of update phases in the game loop unless intentionally tested.
- If behavior changes unexpectedly, revert only the latest small step and retest.
