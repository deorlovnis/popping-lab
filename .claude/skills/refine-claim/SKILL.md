---
name: refine-claim
description: "Sharpen fuzzy ideas into testable, falsifiable claims. Use when claimer needs to transform raw ideas or extract claims from projects. Supports contract (code behavior), belief (assumptions), and spark (feasibility) types."
---

# Refine Claim

Transform fuzzy ideas into sharp, falsifiable claims.

## Process

1. Determine claim type (use `scripts/classify.py` if unclear)
2. Load appropriate reference:
   - `references/contract.md` for code behavior claims
   - `references/belief.md` for assumption claims
   - `references/spark.md` for feasibility claims
3. Follow the refinement process in that reference

## Key Principles

### Falsifiability

A claim must be specific enough to be wrong.

Bad: "Caching helps performance"
Good: "Redis caching reduces p95 latency by >40% for read-heavy endpoints"

### Kill Criteria

State what would prove the claim false BEFORE testing.

Examples:
- "This claim dies if latency improvement is <20%"
- "This claim dies if the API returns any 2xx status"
- "This claim dies if accuracy is below random chance"

### Minimum Scope

Find the smallest version that answers the core question.

- Strip nice-to-haves
- Focus on core hypothesis
- Time-box the test

## Scripts

- `scripts/classify.py` — Auto-classify claim type

## References

- `references/contract.md` — Contract claim refinement
- `references/belief.md` — Belief claim refinement
- `references/spark.md` — Spark claim refinement
