# Popping Lab

A standalone falsification laboratory for ideas.

## What This Is

Popping Lab tests claims against reality. Ideas enter as hypotheses. They leave as **KILLED**, **SURVIVED**, or **UNCERTAIN**.

## CRITICAL: Workflow Execution

**NEVER execute experiments directly.** Always invoke the **popper** agent via Task tool:

```
Task(subagent_type="popper", prompt="<claim or path>")
```

### Required Agent Orchestration

When `/test-claim` is invoked, the following MUST happen:

1. **POPPER** (orchestrator) receives input
   - Classifies claim type (contract/belief/spark)
   - Creates experiment directory
   - Routes to other agents IN SEQUENCE

2. **CLAIMER** refines the claim
   - Proposes multiple testing strategies (not just one!)
   - For math: axiomatic proof, counterexamples, edge cases
   - For code: unit tests, integration, fuzzing
   - Outputs: refined claims with kill criteria

3. **FALSIFIER** attacks claims
   - Uses STRONGEST attack (try to kill, not confirm)
   - Executes actual tests
   - Captures raw observations
   - Renders verdict per claim

4. **JESTER** reflects (NEVER SKIP)
   - Receives 3-sentence brief ONLY
   - Provides zen insight
   - Always runs last

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
POPPER: Received "2+2=4", classifying as belief...
→ Routing to CLAIMER

CLAIMER: Proposing 4 testing strategies...
[shows strategies]
→ Routing to FALSIFIER

FALSIFIER: Attacking C1 with axiomatic proof...
[shows tests and results]

JESTER: [reflection]
```

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

| Agent | Role | Invocation |
|-------|------|------------|
| **popper** | Orchestrates the experiment | `Task(subagent_type="popper")` — ALWAYS start here |
| **claimer** | Refines claims, proposes strategies | Invoked BY popper only |
| **falsifier** | Attacks claims, renders verdict | Invoked BY popper only |
| **jester** | Zen reflection | Invoked BY popper only, NEVER skip |

**Important:** Only popper is invoked directly. Other agents are invoked by popper during orchestration.

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
6. **Propose multiple strategies** — Claimer MUST offer different testing approaches before falsifier runs
7. **Never shortcut orchestration** — All 4 agents must run, visible handoffs required
