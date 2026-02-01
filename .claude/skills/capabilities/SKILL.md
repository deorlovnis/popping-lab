---
name: capabilities
description: "Registry-based capability detection. Answers 'Can I test this claim?' by checking claim types and tool availability. Use before routing to claimer."
---

# Capabilities

Check testability before execution.

## Functions

### Check Testability

Given a claim and its property type, determine testability level.

1. **Lookup claim type** in `registry/claim_types.yaml`
   - FOUND → get verification method and kill template
   - NOT FOUND → return `skill_gap: true`

2. **Check required tools** in `registry/tools.yaml`
   - Run each tool's `check` command
   - Collect available/missing/installable

3. **Determine level:**
   - `full` — type known, all tools available
   - `partial` — type known, some tools missing but has fallbacks
   - `manual` — type known, no automated tools
   - `unknown` — type not in registry
   - `blocked` — required tool missing, not installable

### Extend Registry

When type not found, run extension protocol (3 questions):

1. What makes this claim TRUE?
2. What makes this claim FALSE?
3. How do we measure it?

Validate against `registry/schema.yaml` and add to `registry/claim_types.yaml`.

## Output Schema

```yaml
testability:
  level: full | partial | manual | unknown | blocked
  claim_type: equality | invariant | membership | ordering | grounding | feasibility | null
  kill_template: "Find input where X ≠ Y"
  tools:
    available: [pytest, hypothesis]
    missing: []
    installable: [z3-solver]
  gaps:
    skill_gap: false
    tool_gap: false
  actions:
    - type: proceed | install | extend | block
      details: "string"
```

## Registry Files

- `registry/schema.yaml` — Validation rules for registry entries
- `registry/claim_types.yaml` — Property types and verification methods
- `registry/tools.yaml` — Tool definitions and availability checks
