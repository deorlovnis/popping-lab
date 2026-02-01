---
name: refine-claim
description: "Sharpen fuzzy ideas into testable, falsifiable claims. Use when claimer needs to transform raw ideas or extract claims from projects. Supports property-based types: equality, invariant, membership, ordering, grounding, feasibility."
---

# Refine Claim

Transform fuzzy ideas into sharp, falsifiable claims.

## Process

1. Determine claim type (use `scripts/classify.py` if unclear)
2. Load appropriate reference:
   - `references/equality.md` for comparison claims (X = Y)
   - `references/invariant.md` for constraint claims (P always holds)
   - `references/membership.md` for validation claims (X ∈ S)
   - `references/ordering.md` for ranking claims (X ≤ Y)
   - `references/grounding.md` for attribution claims (X supported by Y)
   - `references/feasibility.md` for POC claims (Can X work?)
3. Follow the refinement process in that reference

## Property Types

| Type | What It Tests | Kill Criteria |
|------|---------------|---------------|
| equality | X = Y | Find input where X ≠ Y |
| invariant | P always holds | Find state where ¬P |
| membership | X ∈ S | Find X ∉ S |
| ordering | X ≤ Y | Find order violation |
| grounding | X supported by Y | Find ungrounded X |
| feasibility | Can X work? | Show blocker |

## Key Principles

### Falsifiability

A claim must be specific enough to be wrong.

Bad: "Caching helps performance"
Good: "Redis caching reduces p95 latency by >40% for read-heavy endpoints"

### Kill Criteria

State what would prove the claim false BEFORE testing.

Examples:
- "Dies if X ≠ Y for any tested input"
- "Dies if invariant P violated in any state"
- "Dies if element found outside valid set"

### Minimum Scope

Find the smallest version that answers the core question.

- Strip nice-to-haves
- Focus on core hypothesis
- Time-box the test

## Scripts

- `scripts/classify.py` — Auto-classify claim type

## References

- `references/equality.md` — Equality claim refinement (X = Y)
- `references/invariant.md` — Invariant claim refinement (P holds)
- `references/membership.md` — Membership claim refinement (X ∈ S)
- `references/ordering.md` — Ordering claim refinement (X ≤ Y)
- `references/grounding.md` — Grounding claim refinement (attribution)
- `references/feasibility.md` — Feasibility claim refinement (POCs)
