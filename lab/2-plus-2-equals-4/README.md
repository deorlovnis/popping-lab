# Experiment: 2+2=4

A falsification experiment testing the claim "2+2=4".

## Result

| Claim | Verdict |
|-------|---------|
| C1: Standard arithmetic | **SURVIVED** |
| C2: Modular arithmetic (Z/3Z) | **KILLED** |
| C3: All number systems | **KILLED** |
| C4: All computational systems | **KILLED** |

**Final Verdict:** UNCERTAIN (true in standard arithmetic, false in many valid interpretations)

## Key Insight

"2+2=4" is a local truth, not a universal one. Precision matters.

## Files

- `experiment.ipynb` - Full experiment notebook
- `claims.yaml` - Refined claims and verdicts
- `poc/test_claims.py` - Falsification test code
- `jester_reflection.md` - Zen reflection
