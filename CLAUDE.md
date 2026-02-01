# Popping Lab

A standalone falsification laboratory for ideas.

## What This Is

Popping Lab tests claims against reality. Ideas enter as hypotheses. They leave as **KILLED**, **SURVIVED**, or **UNCERTAIN**.

## Architecture: Command-Level Orchestration

The `/test-claim` command orchestrates experiments by invoking agents sequentially. The main conversation acts as orchestrator—agents do NOT spawn other agents.

### Orchestration Flow

```
/test-claim
    │
    ├─→ Task(popper, opus) ─→ triage result
    │
    ├─→ Task(technician, sonnet) ─→ testability report
    │
    ├─→ Task(claimer, sonnet) ─→ claims.yaml + POC/tests
    │
    ├─→ Task(falsifier, opus) ─→ verdicts
    │
    ├─→ Task(jester, opus) ─→ reflection
    │
    └─→ Generate experiment.ipynb
```

### Visible Handoffs

The user MUST see which agent is doing what. Show:
- Agent name at each transition
- What was passed to the agent
- What the agent produced

**Anti-pattern (WRONG):**
```
I'll test 2+2=4...
[runs python]
Result: 4. SURVIVED.
```

**Correct pattern:**
```
POPPER: Received "2+2=4", classifying as equality...
→ Triage complete

TECHNICIAN: Checking capabilities...
[testability: full, tools: pytest available]
→ Validation complete

CLAIMER: Building claims and tests...
[claims.yaml created]
→ Build complete

FALSIFIER: Attacking claims...
[observations and verdict]

JESTER: [reflection]
```

## Commands

- `/test-claim <idea-or-path>` — Test a claim or project
- `/extract-claims <path>` — Extract claims from codebase
- `/jester [koan]` — Zen reflection

## Directory Structure

```
.claude/
├── commands/     # Slash commands
├── agents/       # Agent definitions
└── skills/       # Procedural knowledge
    └── capabilities/
        └── registry/   # Claim types and tools registry

lab/              # Experiment output (per experiment)
└── <name>/
    ├── experiment.ipynb
    ├── claims.yaml
    └── poc/
```

## Claim Types (Property-Based)

| Type | What It Tests | Kill Criteria |
|------|---------------|---------------|
| **equality** | X = Y | Find input where X ≠ Y |
| **invariant** | P always holds | Find state where ¬P |
| **membership** | X ∈ S | Find X ∉ S |
| **ordering** | X ≤ Y | Find order violation |
| **grounding** | X supported by Y | Find ungrounded X |
| **feasibility** | Can X work? | Show blocker |

## Agents

| Agent | Model | Role | Skills |
|-------|-------|------|--------|
| **popper** | opus | Triage: classify claims, determine strategy | capabilities, test-claim |
| **technician** | sonnet | Validate: check testability with existing tools | capabilities |
| **claimer** | sonnet | Build: create POC/tests (main workhorse) | build-poc, refine-claim, extract-claims, software-philosophy, python-standards |
| **falsifier** | opus | Attack: execute tests, render verdicts | ALL project skills |
| **jester** | opus | Reflect: zen insight (read-only) | ALL project skills |

**Important:** Agents are invoked by the orchestrating command (`/test-claim`), not by each other.

## Verdicts

- **KILLED** — Falsification criteria met
- **SURVIVED** — Criteria not met, test valid
- **UNCERTAIN** — Inconclusive

## Testability Levels

| Level | Meaning | Action |
|-------|---------|--------|
| `full` | Type known, tools available | Proceed normally |
| `partial` | Some tools missing | Proceed with reduced verification |
| `manual` | No automated tools | Guidance only |
| `unknown` | Type not in registry | Run extension protocol |
| `blocked` | Required tool unavailable | Report and ask user |

## Key Principles

1. **Claims must be falsifiable** — Specific enough to be wrong
2. **State kill criteria before testing** — No moving goalposts
3. **Seek the strongest attack** — Try to kill the claim
4. **Context isolation** — Agents only see what they need
5. **Capture everything** — Raw observations matter
6. **Propose multiple strategies** — Claimer MUST offer different testing approaches
7. **Visible handoffs** — User sees each agent transition
8. **Registry-based capabilities** — Check testability before execution
