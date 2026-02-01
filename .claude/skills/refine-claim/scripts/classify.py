#!/usr/bin/env python3
"""
Auto-classify claim type based on property patterns.

Usage:
    python classify.py "<claim>"

Output:
    equality | invariant | membership | ordering | grounding | feasibility
"""

import re
import sys


def classify_claim(claim: str) -> str:
    """
    Classify a claim by property type:
    - equality: X = Y (comparisons, expected values)
    - invariant: P always holds (bounds, constraints)
    - membership: X in S (validation, filtering)
    - ordering: X < Y (ranking, sorting)
    - grounding: X supported by Y (attribution)
    - feasibility: Can X work? (new ideas, POCs)
    """
    claim_lower = claim.lower()

    # Equality indicators: comparisons, return values, expected outputs
    equality_patterns = [
        r"\b(returns?|equals?|outputs?|produces?)\b",
        r"\b(status\s*code|http\s*\d{3}|4\d{2}|5\d{2}|2\d{2})\b",
        r"\b(should|must|will)\s+(return|equal|output|be)\b",
        r"\b(result|response|value)\s+(is|equals?|==)\b",
        r"\b(expected|actual)\b",
        r"==|!=|\.equals?\(",
    ]

    # Invariant indicators: constraints that must always hold
    invariant_patterns = [
        r"\b(always|never|must\s+hold|guaranteed)\b",
        r"\b(>=|<=|>|<)\s*\d+",
        r"\b(bound|limit|constraint|threshold)\b",
        r"\b(improves?|reduces?|increases?|decreases?)\b.*\b(by|to)\b",
        r"\b(\d+%|\d+x|faster|slower)\b",
        r"\b(performance|latency|throughput|memory)\b",
        r"\b(non-?negative|positive|within)\b",
    ]

    # Membership indicators: set membership, validation
    membership_patterns = [
        r"\b(is\s+(a|an|one\s+of|valid|in))\b",
        r"\b(belongs?\s+to|member\s+of|contains?)\b",
        r"\b(valid|invalid|allowed|forbidden)\b",
        r"\b(enum|set|list|collection)\b",
        r"\b(matches?|pattern|format|type)\b",
        r"\b(role|permission|category)\b",
    ]

    # Ordering indicators: comparison relationships
    ordering_patterns = [
        r"\b(sorted|ordered|ranked|priorit)\b",
        r"\b(before|after|precedes?|follows?)\b",
        r"\b(first|last|next|previous)\b",
        r"\b(ascending|descending|sequence)\b",
        r"\b(greater|lesser|higher|lower)\s+than\b",
        r"\b(heap|queue|stack)\b",
    ]

    # Grounding indicators: evidence and attribution
    grounding_patterns = [
        r"\b(supported\s+by|derived\s+from|based\s+on)\b",
        r"\b(evidence|source|reference|citation)\b",
        r"\b(documented|traced|attributed)\b",
        r"\b(coverage|tested|verified)\b",
        r"\b(matches?\s+(implementation|spec|docs?))\b",
    ]

    # Feasibility indicators: can it work questions
    feasibility_patterns = [
        r"\b(can\s+we|could\s+we|is\s+it\s+possible)\b",
        r"\b(feasible|viable|achievable|doable)\b",
        r"\b(predict|detect|identify|recognize|infer)\b",
        r"\b(build|create|implement)\b.*\b(that|which|to)\b",
        r"\b(poc|proof\s+of\s+concept|prototype)\b",
        r"\b(idea|concept|approach|technique)\b",
    ]

    # Score each type
    scores = {
        "equality": 0,
        "invariant": 0,
        "membership": 0,
        "ordering": 0,
        "grounding": 0,
        "feasibility": 0,
    }

    pattern_sets = [
        ("equality", equality_patterns),
        ("invariant", invariant_patterns),
        ("membership", membership_patterns),
        ("ordering", ordering_patterns),
        ("grounding", grounding_patterns),
        ("feasibility", feasibility_patterns),
    ]

    for prop_type, patterns in pattern_sets:
        for pattern in patterns:
            if re.search(pattern, claim_lower):
                scores[prop_type] += 1

    # Return highest scoring type
    max_score = max(scores.values())
    if max_score == 0:
        return "feasibility"  # Default: treat as feasibility test

    # Prefer feasibility for ties (wild ideas)
    if scores["feasibility"] == max_score:
        return "feasibility"

    return max(scores, key=lambda k: scores[k])


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python classify.py '<claim>'", file=sys.stderr)
        sys.exit(1)

    claim = " ".join(sys.argv[1:])
    result = classify_claim(claim)
    print(result)


if __name__ == "__main__":
    main()
