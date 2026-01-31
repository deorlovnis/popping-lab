---
name: test-claim
description: Test a claim against a project or explore a wild idea. Creates experiments in lab/<name>/.
---

# /test-claim

Test claims against existing projects or explore wild ideas.

## Usage

```
/test-claim <idea-or-project-path>
/test-claim --type <contract|belief|spark> <claim>
/test-claim --project <path> "<claim>"
```

## Arguments

- `<idea-or-project-path>` — Either a path to existing codebase or a claim string
- `--type` — Force claim type: contract, belief, or spark
- `--project` — Test specific claim against this project

## Behavior

| Input | Detection | Result |
|-------|-----------|--------|
| Path to directory | Existing project | Extract claims, test against project |
| Idea string | Auto-classify type | Create experiment, build POC if spark |
| `--type spark "..."` | Explicit spark | Always create new experiment with POC |

## Examples

```bash
# Test existing project
/test-claim ~/my-app

# Test specific claim against project
/test-claim --project ~/my-app "POST /login returns 401"

# Test wild idea (spark)
/test-claim "predict mood from typing patterns"

# Explicit type
/test-claim --type belief "caching improves latency by 40%"
```

## Process

This command invokes the **popper** agent to orchestrate the experiment:

1. Parse input to determine mode (project vs spark)
2. Create experiment directory: `lab/<slugified-name>/`
3. Route to **claimer** agent to refine claims
4. Route to **falsifier** agent to test claims
5. Route to **jester** agent for zen reflection
6. Generate `experiment.ipynb` and `claims.yaml`

## Output

Creates `lab/<experiment-name>/` containing:
- `experiment.ipynb` — The experiment record
- `claims.yaml` — Claims and verdicts
- `poc/` — POC code (for spark claims)
