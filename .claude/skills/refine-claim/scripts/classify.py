#!/usr/bin/env python3
"""
Auto-classify claim type based on keywords and patterns.

Usage:
    python classify.py "<claim>"

Output:
    contract | belief | spark
"""

import re
import sys


def classify_claim(claim: str) -> str:
    """
    Classify a claim into one of three types:
    - contract: Code behavior claims (API, function behavior, errors)
    - belief: Assumption claims (performance, metrics, comparisons)
    - spark: Feasibility claims (can we, is it possible, new ideas)
    """
    claim_lower = claim.lower()

    # Contract indicators: specific code behavior
    contract_patterns = [
        r'\b(returns?|throws?|raises?)\b',
        r'\b(status\s*code|http\s*\d{3}|4\d{2}|5\d{2}|2\d{2})\b',
        r'\b(api|endpoint|route|post|get|put|delete|patch)\b',
        r'\b(function|method|class)\s+\w+',
        r'\b(should|must|will)\s+(return|throw|raise|output)',
        r'\b(when|if)\s+.*\s+(then|returns?)',
    ]

    # Belief indicators: assumptions about behavior/metrics
    belief_patterns = [
        r'\b(improves?|reduces?|increases?|decreases?)\b.*\b(by|to)\b',
        r'\b(\d+%|\d+x|faster|slower|better|worse)\b',
        r'\b(performance|latency|throughput|memory|cpu)\b',
        r'\b(most|majority|typically|usually|often)\b',
        r'\b(because|due to|causes?|affects?)\b',
        r'\b(assume|assumption|believe|think)\b',
    ]

    # Spark indicators: feasibility questions
    spark_patterns = [
        r'\b(can\s+we|could\s+we|is\s+it\s+possible)\b',
        r'\b(predict|detect|identify|recognize|infer)\b',
        r'\b(from|using|based\s+on|via)\b.*\b(patterns?|signals?|data)\b',
        r'\b(build|create|make|implement)\b.*\b(that|which|to)\b',
        r'\b(feasible|viable|possible|achievable)\b',
        r'\b(idea|concept|approach|technique)\b',
    ]

    # Score each type
    scores = {'contract': 0, 'belief': 0, 'spark': 0}

    for pattern in contract_patterns:
        if re.search(pattern, claim_lower):
            scores['contract'] += 1

    for pattern in belief_patterns:
        if re.search(pattern, claim_lower):
            scores['belief'] += 1

    for pattern in spark_patterns:
        if re.search(pattern, claim_lower):
            scores['spark'] += 1

    # Return highest scoring type, default to spark for wild ideas
    max_score = max(scores.values())
    if max_score == 0:
        return 'spark'  # Default: treat as feasibility test

    # Prefer spark for ties with spark, otherwise first match
    if scores['spark'] == max_score:
        return 'spark'

    return max(scores, key=scores.get)


def main():
    if len(sys.argv) < 2:
        print("Usage: python classify.py '<claim>'", file=sys.stderr)
        sys.exit(1)

    claim = ' '.join(sys.argv[1:])
    result = classify_claim(claim)
    print(result)


if __name__ == '__main__':
    main()
