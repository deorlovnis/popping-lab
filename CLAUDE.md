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
POPPER: Received "2+2=4", classifying as Analytic...
→ Triage complete

TECHNICIAN: Checking Veritas testability...
[testability: full, sympy available]
→ Validation complete

CLAIMER: Building claims and tests...
[claims.yaml created with Veritas truth types]
→ Build complete

FALSIFIER: Attacking claims with Veritas...
[VerdictResult: SURVIVED]

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

src/veritas/      # SymPy-verified falsification library
├── symbolic.py   # Formula building blocks
├── truth.py      # Truth types (Analytic, Modal, Empirical, Probabilistic)
├── evidence.py   # Evidence and Verdict structures
├── engine.py     # Verification logic
├── testing.py    # User-facing API (@verified, claim())
└── extensions.py # Domain-specific extensions

lab/              # Experiment output (per experiment)
└── <name>/
    ├── experiment.ipynb
    ├── claims.yaml
    └── poc/
```

## Veritas Truth Types

| Truth Type | What It Tests | Falsification Form |
|------------|---------------|-------------------|
| **Analytic** | X = Y, X ∈ S, X ≤ Y | ∃x: f(x) ≠ expected |
| **Modal** | P always holds | ◇¬P (find state where ¬P) |
| **Empirical** | Observation supports claim | Find contradicting observation |
| **Probabilistic** | P(X) op threshold | Find metric violating threshold |

### Mapping from Legacy Types

| Old Type | Veritas Truth | Rationale |
|----------|---------------|-----------|
| equality | `Analytic` | ∃x: f(x) ≠ expected |
| membership | `Analytic` | ∃x: x ∉ S |
| ordering | `Analytic` | ∃x,y: order violated |
| invariant | `Modal` | ◇¬P |
| grounding | `Empirical` | observation contradicts |
| feasibility | `Empirical`/`Probabilistic` | blocker or threshold |

## Agents

| Agent | Model | Role | Skills |
|-------|-------|------|--------|
| **popper** | opus | Triage: classify into Veritas truth types | refine-claim, test-claim |
| **technician** | sonnet | Validate: check Veritas testability | (veritas checks) |
| **claimer** | sonnet | Build: create POC/tests using Veritas | build-poc, refine-claim, extract-claims |
| **falsifier** | opus | Attack: execute Veritas verification | ALL project skills |
| **jester** | opus | Reflect: zen insight (read-only) | ALL project skills |

**Important:** Agents are invoked by the orchestrating command (`/test-claim`), not by each other.

## Verdicts

- **KILLED** — Falsification criteria met (counterexample found)
- **SURVIVED** — Criteria not met, test valid
- **UNCERTAIN** — Inconclusive (missing evidence, symbolic unresolvable)

## Veritas API

```python
from veritas import Analytic, claim, Verdict

# Define a truth
truth = Analytic(
    statement="add(2, 2) equals 4",
    lhs="result",
    rhs=4,
)

# Test with claim() context manager
with claim(truth) as c:
    actual = 2 + 2
    c.bind(result=actual, x=actual)

# Veritas verifies automatically
assert c.result.verdict == Verdict.SURVIVED
```

## Key Principles

1. **Claims must be falsifiable** — Specific enough to be wrong
2. **State falsification form before testing** — No moving goalposts
3. **Seek the strongest attack** — Try to kill the claim
4. **Context isolation** — Agents only see what they need
5. **Capture everything** — Evidence bindings matter
6. **Propose multiple strategies** — Claimer MUST offer different testing approaches
7. **Visible handoffs** — User sees each agent transition
8. **Veritas verification** — Let SymPy evaluate, don't manually determine verdicts
