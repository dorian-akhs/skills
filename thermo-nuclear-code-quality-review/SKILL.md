---
name: thermo-nuclear-code-quality-review
description: Perform an unusually strict structural code-quality review.
disable-model-invocation: true
---

# Thermo-Nuclear Code Quality Review

Establish the user's requested scope and fixed baseline, then read and apply
[structural review standards](references/structural-standards.md) in full.
Inspect the scoped code and its affected callers. Report evidenced findings,
actionable remedies, verification performed, and limitations against the
approval bar. Apply changes only when the user's scope authorizes them.

The standards are plain reference material that other workflows may read without
invoking this user-only skill. The `loop-*.md` references support `feature-loop`
and `review-loop`; standalone structural reviews do not need them.
