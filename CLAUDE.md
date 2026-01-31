# Popping Lab

A standalone falsification laboratory for ideas.

## What This Is

Popping Lab tests claims against reality. Ideas enter as hypotheses. They leave as **KILLED**, **SURVIVED**, or **UNCERTAIN**.

## Commands

- `/test-claim <idea-or-path>` — Test a claim or project
- `/extract-claims <path>` — Extract claims from codebase
- `/jester [koan]` — Zen reflection

## Architecture

```
.claude/
├── commands/     # Slash commands
├── agents/       # Agent definitions
└── skills/       # Procedural knowledge

lab/              # Experiment output (per experiment)
└── <name>/
    ├── experiment.ipynb
    ├── claims.yaml
    └── poc/
```

## Claim Types

| Type | What It Is | How It's Tested |
|------|------------|-----------------|
| **contract** | Code behavior | Run tests, API calls |
| **belief** | Assumption | Gather evidence |
| **spark** | Feasibility | Build POC |

## Agents

| Agent | Role |
|-------|------|
| **popper** | Orchestrates the experiment |
| **claimer** | Refines claims |
| **falsifier** | Tests and renders verdict |
| **jester** | Zen reflection |

## Verdicts

- **KILLED** — Falsification criteria met
- **SURVIVED** — Criteria not met, test valid
- **UNCERTAIN** — Inconclusive

## Key Principles

1. **Claims must be falsifiable** — Specific enough to be wrong
2. **State kill criteria before testing** — No moving goalposts
3. **Seek the strongest attack** — Try to kill the claim
4. **Context isolation** — Agents only see what they need
5. **Capture everything** — Raw observations matter
