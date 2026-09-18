---
name: java-refactoring-coach
description: "Review Java code while it is being written and surface the next small, behavior-preserving refactoring from clean-code, object-oriented design, and SOLID perspectives. Use for quick feedback on a current diff, class, method, responsibility split, conditional, dependency, or testability concern. Use code-review instead for a completed branch or PR audit against standards and a spec."
---

# Java Refactoring Coach

Give the developer one useful next move while the code is still taking shape. Treat Clean Code and
SOLID as lenses for diagnosing concrete costs, not rules to maximize.

## Inspect

Use the target the user names. Otherwise inspect the current Java diff and enough callers, tests,
and neighboring types to understand its behavior. If there is no diff, ask for a class, method, or
design concern rather than reviewing the whole repository.

Establish the code's present responsibility and observable behavior. Then look for the highest-value
pressure point among:

- names and control flow that hide intent;
- responsibilities that change for different reasons;
- behavior living beside the data it uses rather than with it;
- exposed mutable state or invariants enforced outside their owner;
- dependencies that make behavior hard to isolate or substitute;
- repeated conditionals that signal a missing concept;
- tests that are difficult because time, I/O, construction, or policy is entangled;
- abstractions whose current cost exceeds their demonstrated use.

Check Java-specific correctness when it bears on the design, including collection mutability,
nullability, equality, exceptions, transaction boundaries, and framework lifecycle. Do not turn this
into an exhaustive defect audit; route a completed branch or PR audit to `code-review`.

## Judge

Recommend a refactoring only when the current code shows a concrete cost: duplicated decisions,
scattered change, invalid states, unclear ownership, difficult tests, or a dependency pointing the
wrong way. Explain that cost before naming a principle or pattern.

Prefer the smallest behavior-preserving move. Extract an interface only when a real boundary,
substitution, or testing need exists. Introduce polymorphism only when recurring variation repays its
indirection. Keep a direct implementation when the alternative merely anticipates future change.
`Keep as is` is a valid conclusion.

Do not score SOLID compliance or optimize for counts of classes, methods, or interfaces. Distinguish
a demonstrated problem from a possible future pressure. If behavior is not protected well enough
for the proposed change, make the next move a focused characterization test.

## Respond

Lead with the single most valuable insight. Use at most three only when they are independent and
material. For each, give:

1. **Pressure**: the exact code and change cost observed.
2. **Why**: the relevant object-oriented idea in plain language; name the Clean Code or SOLID concept
   only when it sharpens the explanation.
3. **Move**: the smallest refactoring, with a compact before/after sketch when useful.
4. **Stop condition**: when to keep the current design or stop extracting.

End with one verification that shows behavior stayed intact. Keep ordinary feedback compact so the
developer can return to coding immediately.

When the user asks only for insight, do not edit. When they ask to refactor, apply the smallest move,
run the focused tests, and report the design improvement and remaining tradeoff without expanding
into unrelated cleanup.
