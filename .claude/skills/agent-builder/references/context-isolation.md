# Context Isolation

Critical principle: Agents receive only what they need.

## Why Isolation Matters

### Prevents Bias

If the falsifier knows the claimer was excited about an idea, they might go easy on it.

### Enables Fresh Eyes

Each agent should approach their task without preconceptions from prior steps.

### Reduces Noise

More context = more distraction. Keep it focused.

## What to Pass

### To Claimer

**Pass:**
- Raw user input (idea or project reference)
- Skill: refine-claim

**Don't pass:**
- Prior conversation
- User's emotional state
- Time pressure

### To Falsifier

**Pass:**
- claims.yaml from claimer
- Skill: test-claim
- For spark: build-poc skill

**Don't pass:**
- Original user input
- Why claimer chose this framing
- Claimer's confidence level

### To Jester

**Pass:**
- 3-sentence brief: what was claimed, verdict, why
- Skill: wild-take

**Don't pass:**
- Full claims.yaml
- Test code or output
- Any details beyond brief

## Brief Format for Jester

Maximum 3 sentences:

```
We tested whether [claim in plain language].
The verdict was [KILLED/SURVIVED/UNCERTAIN].
[One sentence on why.]
```

**Example:**

```
We tested whether typing speed could predict stress levels.
The verdict was UNCERTAIN.
The POC showed weak correlation but sample size was too small.
```

## Handoff Protocol

### popper → claimer

```yaml
handoff:
  to: claimer
  input: "<raw user input>"
  skills: [refine-claim]
  return: claims.yaml
```

### popper → falsifier

```yaml
handoff:
  to: falsifier
  input: claims.yaml
  skills: [test-claim, build-poc]  # if spark
  return: updated claims.yaml
```

### popper → jester

```yaml
handoff:
  to: jester
  input: "<3-sentence brief>"
  skills: [wild-take]
  return: reflection text
```

## Red Flags

Signs you're passing too much context:

- Agent output references things it shouldn't know
- Agent seems biased by prior steps
- Agent is overwhelmed with information
- Agent is summarizing rather than doing its job

## Testing Isolation

To verify isolation is working:

1. Give the same claim to falsifier with different (fake) claimer confidence levels
2. Verdicts should be identical
3. If verdict changes based on confidence, isolation failed
