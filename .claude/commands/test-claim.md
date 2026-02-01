---
name: test-claim
description: Test a claim against a project or explore a wild idea. Creates experiments in lab/<name>/.
---

# /test-claim

Test claims against existing projects or explore wild ideas.

## Usage

```
/test-claim <idea-or-project-path>
/test-claim --type <property-type> <claim>
/test-claim --project <path> "<claim>"
```

## Arguments

- `<idea-or-project-path>` — Either a path to existing codebase or a claim string
- `--type` — Force property type: equality, invariant, membership, ordering, grounding, feasibility
- `--project` — Test specific claim against this project

## Behavior

| Input | Detection | Result |
|-------|-----------|--------|
| Path to directory | Existing project | Extract claims, test against project |
| Idea string | Auto-classify type | Create experiment, build POC if feasibility |
| `--type feasibility "..."` | Explicit | Always create new experiment with POC |

## Examples

```bash
# Test existing project
/test-claim ~/my-app

# Test specific claim against project
/test-claim --project ~/my-app "POST /login returns 401"

# Test wild idea (feasibility)
/test-claim "predict mood from typing patterns"

# Explicit type
/test-claim --type invariant "caching improves latency by 40%"
```

## Orchestration Flow

This command orchestrates the experiment by invoking agents sequentially:

```
/test-claim
    │
    ├─→ Step 1: Task(popper, opus) ─→ triage result
    │
    ├─→ Step 2: Task(technician, sonnet) ─→ testability report
    │
    ├─→ Step 3: Task(claimer, sonnet) ─→ claims.yaml + POC/tests
    │
    ├─→ Step 4: Task(falsifier, opus) ─→ verdicts
    │
    ├─→ Step 5: Task(jester, opus) ─→ reflection
    │
    └─→ Step 6: Generate experiment.ipynb
```

### Step 1: POPPER (Triage)

```
Task(subagent_type="popper", model="opus", prompt="
  Triage this claim: $ARGS

  Return:
  - mode (project | wild_idea)
  - experiment_dir path
  - claim_type
  - skill_gap (true/false)
  - input_summary
  - strategy_hints
")
```

**Show:** `POPPER: Received "<claim>", classifying as <type>...`

### Step 2: TECHNICIAN (Validation)

```
Task(subagent_type="technician", model="sonnet", prompt="
  Validate testability for:
  - Claim: <claim>
  - Type: <claim_type from popper>
  - Triage: <triage result>

  Return testability report with:
  - level (full | partial | manual | unknown | blocked)
  - kill_template
  - available tools
  - gaps
")
```

**Show:** `TECHNICIAN: Checking capabilities... [testability: <level>]`

### Step 3: CLAIMER (Build)

```
Task(subagent_type="claimer", model="sonnet", prompt="
  Build tests for:
  - Input: <original claim>
  - Experiment dir: <experiment_dir>
  - Testability: <testability report>

  Create:
  - claims.yaml with refined claims and strategies
  - Test code or POC in experiment directory

  Return path to claims.yaml
")
```

**Show:** `CLAIMER: Building claims and tests...`

### Step 4: FALSIFIER (Attack)

```
Task(subagent_type="falsifier", model="opus", prompt="
  Attack claims in: <claims.yaml path>
  Experiment dir: <experiment_dir>

  For each claim:
  - Run the tests
  - Capture observations
  - Render verdict (KILLED | SURVIVED | UNCERTAIN)

  Update claims.yaml with verdicts
  Return updated claims.yaml path
")
```

**Show:** `FALSIFIER: Attacking claims...`

### Step 5: JESTER (Reflect)

Compose a 3-sentence brief:
1. What was claimed
2. The verdict
3. Why

```
Task(subagent_type="jester", model="opus", prompt="
  Brief: <3-sentence summary>

  Reflect on the act of experimentation.
")
```

**Show:** `JESTER: <reflection>`

### Step 6: Generate experiment.ipynb

Create notebook documenting the full experiment with all agent outputs.

## Output

Creates `lab/<experiment-name>/` containing:
- `experiment.ipynb` — The experiment record
- `claims.yaml` — Claims and verdicts
- `poc/` — POC code (for feasibility claims)

## Visible Handoffs

Show agent transitions clearly:

```
POPPER: Received "<claim>", classifying as <type>...
→ Triage complete

TECHNICIAN: Checking capabilities...
[testability: full, tools: pytest available]
→ Validation complete

CLAIMER: Building claims and tests...
[claims.yaml created with 2 claims]
→ Build complete

FALSIFIER: Attacking claims...
[C001: SURVIVED, C002: KILLED]
→ Verdicts rendered

JESTER: [reflection]
```
