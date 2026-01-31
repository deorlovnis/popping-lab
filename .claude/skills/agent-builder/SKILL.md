---
name: agent-builder
description: "Create new agent definitions for Popping Lab. Use when adding or modifying agents. Ensures proper context isolation and handoff protocols."
---

# Agent Builder

Create agent definitions with proper context isolation.

## Agent Anatomy

```markdown
---
name: agent-name
description: "What it does. When to invoke it."
---

# Agent Name

Brief role description.

## Input

What it receives (be specific about context)

## Process

Step by step

## Output

What it produces

## Rules

Constraints and guidelines
```

## Key Principle: Context Isolation

Each agent receives ONLY what it needs:
- Prevents bias contamination
- Enables fresh perspective
- Reduces context bloat

## Process

1. Define the agent's role (one clear purpose)
2. Specify exact inputs (what context it receives)
3. Document the process (step by step)
4. Define outputs (structured where possible)
5. Set rules (constraints, what NOT to do)

## Agent Types in Popping Lab

| Agent | Role | Context Receives |
|-------|------|------------------|
| popper | Orchestrator | Full user input |
| claimer | Refine claims | Input + skill |
| falsifier | Test claims | claims.yaml + skill |
| jester | Reflect | 3-sentence brief ONLY |

## References

- `references/context-isolation.md` — What to pass, what NOT to pass
