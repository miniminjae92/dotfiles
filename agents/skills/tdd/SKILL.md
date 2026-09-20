---
name: tdd
description: Test-driven development for features, bug fixes, and test design. Use when the user wants to write or refactor unit or integration tests, derive a public interface from tests, work test-first, or run a red-green loop, including Java test work.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle — consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

테스트 이름은 테스트가 관찰하는 경계의 언어로 작성한다.

Treat one test responsibility as one observable behavior that can change independently. Splitting assertions against the same broad interface does not create smaller responsibilities by itself.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Derive the interface from behavior

Use this order for a new behavior:

1. Express the required observable behavior as a failing test.
2. Derive the cohesive module and public interface that can provide that behavior.
3. Add only enough implementation to pass the test.

The test drives the public interface. Add a public method when it expresses a cohesive capability for callers, not merely to expose an internal step to tests. Verify behavior through that interface and leave private implementation free to change.

When starting from a `test-list`, take one unchecked observable behavior into this loop. Do not implement the whole list horizontally.

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything — agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

When the shape of that interface is itself in question — how deep the module is, where the seam belongs, what the interface should expose — use the `/codebase-design` skill for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

For a new behavior, let the test drive the smallest cohesive module and public interface needed by that behavior. Do not add public methods only to expose private implementation to tests. If only a broad public interface exists, repeated focused tests at that same interface may improve failure messages, but they do not prove that responsibility has been decomposed.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead — one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Existing behavior

When code already implements the behavior, first identify its current public interface and existing evidence.

- A test added after the implementation is a regression test or characterization test, not a Red in a TDD loop.
- Repeating the same large public interface with one assertion per test does not create smaller responsibilities.
- Derive a new module and public interface only when an independently changing behavior needs a cohesive owner.
- Keep test parsing, fixture construction, and other observation mechanics in test support code rather than promoting them to product responsibilities.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Classify honestly.** A test added after the behavior exists is a regression or characterization test, not a TDD cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.
