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

### Test a Wild Idea

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

## Methodology: How Verification Works

Popping Lab uses **registry-based capability detection** to reliably verify claims.

### Claim Classification

Claims are classified by the **property being tested**:

| Property | Tests | Kill Criteria |
|----------|-------|---------------|
| equality | X = Y | Find X ≠ Y |
| invariant | P holds | Find ¬P |
| membership | X ∈ S | Find X ∉ S |
| ordering | X ≤ Y | Find violation |
| grounding | X ↔ Y | Find ungrounded |
| feasibility | Can X? | Show blocker |

### Verification Flow

```
┌──────────┐     ┌────────────┐     ┌──────────┐     ┌────────────┐     ┌────────┐
│  popper  │ ──> │ technician │ ──> │ claimer  │ ──> │ falsifier  │ ──> │ jester │
│(orchestr)│     │(validate)  │     │(refine)  │     │(test)      │     │(reflect)│
└──────────┘     └────────────┘     └──────────┘     └────────────┘     └────────┘
      │                │                  │                  │               │
      │          testability         claims.yaml        verdict          wisdom
      │            report                                    │
      └──────────────────────────────────────────────────────┴──> experiment.ipynb
```

1. **POPPER** classifies claim → looks up in registry
2. **TECHNICIAN** validates tools available, checks testability
3. **CLAIMER** refines with kill criteria from registry
4. **FALSIFIER** attacks using registered verification method
5. **JESTER** reflects

### Testability Levels

| Level | Meaning |
|-------|---------|
| full | Type known, tools available |
| partial | Type known, some tools missing |
| manual | Guidance only, no automation |
| unknown | Need extension protocol |
| blocked | Required tool unavailable |

### Extension Protocol

Unknown claim types trigger 3 questions:
1. What makes this TRUE?
2. What makes this FALSE?
3. How do we measure it?

Answers create a new registry entry, extending the system's capabilities.

## Claim Types (Property-Based)

| Type | Description | Example |
|------|-------------|---------|
| **equality** | X equals Y | "POST /login returns 401 for bad password" |
| **invariant** | P always holds | "Caching improves latency by >40%" |
| **membership** | X belongs to S | "Email matches valid format" |
| **ordering** | X ≤ Y relationship | "Results sorted by relevance" |
| **grounding** | X supported by Y | "All assertions have test coverage" |
| **feasibility** | Can X work? | "Can predict mood from typing" |

## Output Structure

```
lab/
└── <experiment-name>/
    ├── experiment.ipynb    # Full record
    ├── claims.yaml         # Claims and verdicts
    ├── poc/                # POC code (for feasibility)
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
6. **Registry-based** — Capabilities are explicit and extensible

## Extending

### Add a Skill

```bash
python .claude/skills/skill-builder/scripts/init_skill.py my-skill --path .claude/skills
```

### Validate a Skill

```bash
python .claude/skills/skill-builder/scripts/validate.py .claude/skills/my-skill
```

### Add a Claim Type

Extend the registry at `.claude/skills/capabilities/registry/claim_types.yaml`:

```yaml
types:
  my_new_type:
    name: my_new_type
    description: "What this type tests"
    tests: "How verification works"
    kills: "Kill criteria template"
    required_tools: [pytest]
```

## License

MIT
