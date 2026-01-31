# Popping Lab

Popping Lab is a falsification engine for the age of AI. Born from the need to verify the complex web of assumptions baked into modern software, it serves as a unified interface for ideation and verification. The framework employs agents to extract specific claims from your ideas and codebases, actively attempting to disprove them to distinguish actual feasibility from mere hallucination.

Whether you are prototyping a wild idea or auditing an existing project, Popping Lab helps you see the reality of the code. It attempts to break confirmation bias and spark self-reflection, empowering you to confidently build what really matters.

## Philosophy

Ideas enter as hypotheses. They leave as:
- **KILLED** — Proven false
- **SURVIVED** — Held up to testing
- **UNCERTAIN** — Needs more investigation

Inspired by Karl Popper's falsificationism: we can never prove ideas true, but we can prove them false.

## Usage

### Test a Wild Idea (Spark)

```bash
/test-claim "predict mood from typing patterns"
```

Creates `lab/predict-mood-from-typing-patterns/` with:
- `claims.yaml` — Refined, testable claims
- `experiment.ipynb` — Full experiment record
- `poc/` — Proof of concept code

### Test an Existing Project

```bash
/test-claim ~/my-project
```

Extracts claims from code and tests them.

### Extract Claims Without Testing

```bash
/extract-claims ~/my-project
```

### Get Zen Reflection

```bash
/jester
/jester "what do we learn from failure"
```

## Claim Types

| Type | Description | Example |
|------|-------------|---------|
| **contract** | Code behavior | "POST /login returns 401 for bad password" |
| **belief** | Assumption | "Caching improves latency by 40%" |
| **spark** | Feasibility | "Can predict mood from typing" |

## How It Works

```
┌──────────┐     ┌──────────┐     ┌────────────┐     ┌────────┐
│  popper  │ ──> │ claimer  │ ──> │ falsifier  │ ──> │ jester │
│(orchestr)│     │(refine)  │     │(test)      │     │(reflect)│
└──────────┘     └──────────┘     └────────────┘     └────────┘
      │                │                  │               │
      │           claims.yaml        verdict          wisdom
      │                                   │
      └───────────────────────────────────┴──> experiment.ipynb
```

1. **Popper** receives your input and orchestrates the flow
2. **Claimer** refines fuzzy ideas into sharp, testable claims
3. **Falsifier** attacks claims with strongest possible tests
4. **Jester** provides zen reflection on the process

## Output Structure

```
lab/
└── <experiment-name>/
    ├── experiment.ipynb    # Full record
    ├── claims.yaml         # Claims and verdicts
    ├── poc/                # POC code (for sparks)
    └── README.md           # Experiment summary
```

## Verdicts

| Verdict | Meaning |
|---------|---------|
| **KILLED** | At least one kill criterion was met |
| **SURVIVED** | No criteria met, test was valid |
| **UNCERTAIN** | Test was flawed, blocked, or inconclusive |

## Key Principles

1. **Falsifiability** — Claims must be specific enough to be wrong
2. **Pre-stated criteria** — Define what kills a claim before testing
3. **Strongest attack** — Try to disprove, not confirm
4. **Context isolation** — Each agent sees only what it needs
5. **Raw observations** — Capture everything, interpret later

## Extending

### Add a Skill

```bash
python .claude/skills/skill-builder/scripts/init_skill.py my-skill --path .claude/skills
```

### Validate a Skill

```bash
python .claude/skills/skill-builder/scripts/validate.py .claude/skills/my-skill
```

## License

MIT
