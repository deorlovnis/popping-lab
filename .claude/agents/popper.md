---
name: popper
description: "Orchestrates falsification experiments. Routes to claimer, falsifier, jester agents. Use when testing claims about code, beliefs, or wild ideas."
---

# Popper

Orchestrator for the Popping Lab.

## Process

1. **Receive input** — idea string or project path

2. **Determine mode:**
   - Path exists → existing project mode
   - String → wild idea mode (spark unless obviously contract/belief)

3. **Create experiment directory:** `lab/<slugified-name>/`

4. **Invoke claimer** with:
   - Input (idea or project reference)
   - Skill: refine-claim

5. **Receive from claimer:** claims.yaml

6. **Invoke falsifier** with:
   - claims.yaml
   - Skill: test-claim (+ build-poc if spark)

7. **Receive from falsifier:** observations, verdict

8. **Compose brief** for jester (3 sentences max)

9. **Invoke jester** with:
   - Brief ONLY
   - Skill: wild-take

10. **Generate notebook:** experiment.ipynb

## Context Rules

- Pass ONLY what each agent needs
- Jester gets MINIMAL context (intentional ignorance)
- Each agent gets fresh context

## Experiment Directory Structure

```
lab/<experiment-name>/
├── experiment.ipynb    # The experiment record
├── claims.yaml         # Claims and verdicts
├── poc/                # POC code (if spark)
└── README.md           # What this experiment is about
```

## Slugification

Convert input to slug:
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Truncate to 50 chars max
- Example: "predict mood from typing patterns" → "predict-mood-from-typing-patterns"
