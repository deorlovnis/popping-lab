# Popping Lab Skill Patterns

Best practices for creating skills in Popping Lab.

## Skill Categories

### Refinement Skills

Transform input into structured output.

**Pattern:**
```
Input → Classification → Refinement → Structured Output
```

**Example:** `refine-claim` takes fuzzy ideas, classifies type, outputs claims.yaml

**Key elements:**
- Classification logic (script or heuristics)
- Type-specific refinement (references per type)
- Consistent output format

### Testing Skills

Execute tests and capture observations.

**Pattern:**
```
Claims → Test Design → Execution → Observations → Verdict
```

**Example:** `test-claim` takes claims, runs tests, outputs verdicts

**Key elements:**
- Test execution (actual code runs)
- Observation capture (raw output)
- Verdict logic (criteria comparison)

### Building Skills

Create artifacts from specifications.

**Pattern:**
```
Specification → Template Selection → Generation → Artifact
```

**Example:** `build-poc` takes claim, selects template, generates POC code

**Key elements:**
- Template library (assets)
- Generation logic (scripts or instructions)
- Output location conventions

### Extraction Skills

Find patterns in existing content.

**Pattern:**
```
Source → Scanning → Pattern Matching → Structured Output
```

**Example:** `extract-claims` scans code, finds patterns, outputs claims

**Key elements:**
- Pattern definitions (references)
- Scanning logic (scripts)
- Confidence rating

### Reflection Skills

Generate unstructured insight.

**Pattern:**
```
Minimal Input → Unconstrained Reflection → Output
```

**Example:** `wild-take` receives brief, outputs zen reflection

**Key elements:**
- Minimal structure
- No templates
- Freedom to diverge

## Common Patterns

### Script + Reference Combo

Use scripts for deterministic operations, references for guidance.

```
SKILL.md:
  1. Run scripts/classify.py to determine type
  2. Load references/{type}.md for guidance
  3. Follow the process in that reference
```

### Type-Specific References

When behavior varies by type, use separate reference files.

```
references/
├── contract.md    # Type A guidance
├── belief.md      # Type B guidance
└── spark.md       # Type C guidance
```

### Asset Templates

When generating files, use templates in assets.

```
assets/
├── web/
│   └── template.html
└── api/
    └── template.py
```

## Anti-Patterns

### Monolithic SKILL.md

**Bad:** Everything in one file
**Good:** SKILL.md as orchestrator, references for details

### No Classification

**Bad:** Same process for all inputs
**Good:** Classify first, then branch

### Missing Scripts

**Bad:** Describe what to do in prose
**Good:** Executable scripts for repeatable operations

### Vague Triggers

**Bad:** description: "Help with things"
**Good:** description: "Use when building API POCs for spark claims"

## Naming Conventions

- Skill names: `kebab-case`
- Script names: `snake_case.py`
- Reference names: `kebab-case.md`
- Asset names: `purpose.ext`
