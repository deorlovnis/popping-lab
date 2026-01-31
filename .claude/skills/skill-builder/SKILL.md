---
name: skill-builder
description: "Create new skills for Popping Lab. Use when adding new claim types, POC templates, or testing methodologies. Self-bootstrapping."
---

# Skill Builder

Create new skills following Anthropic's structure.

## Skill Anatomy

```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + instructions
├── scripts/              # Optional: Executable code
├── references/           # Optional: Documentation for context
└── assets/               # Optional: Templates for output
```

## Process

1. Run `scripts/init_skill.py <name>` to scaffold
2. Edit SKILL.md with clear description (triggers in frontmatter!)
3. Add scripts for deterministic operations
4. Add references for domain knowledge
5. Add assets for templates/boilerplate
6. Validate with `scripts/validate.py <path>`

## SKILL.md Structure

```markdown
---
name: skill-name
description: "When to use this skill. Be specific about triggers."
---

# Skill Name

Brief description of what this skill does.

## Process

Step-by-step instructions.

## Scripts

- `scripts/foo.py` — What it does

## References

- `references/bar.md` — What knowledge it provides

## Assets

- `assets/template.xyz` — What it templates
```

## Key Principles

### Triggers in Description

The description field determines when the skill is invoked. Be specific:

**Good:** "Use when building API POCs for spark claims that involve HTTP endpoints"
**Bad:** "Build things"

### Scripts for Determinism

Put repeatable operations in scripts:
- File generation
- Validation
- Classification
- Template rendering

### References for Knowledge

Put domain expertise in references:
- Patterns and anti-patterns
- Best practices
- Examples

### Assets for Output

Put templates and boilerplate in assets:
- Code templates
- File structures
- Starter files

## Scripts

- `scripts/init_skill.py` — Initialize new skill directory
- `scripts/validate.py` — Validate skill structure

## References

- `references/patterns.md` — Popping Lab skill patterns
