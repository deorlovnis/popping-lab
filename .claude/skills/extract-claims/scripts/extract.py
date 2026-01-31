#!/usr/bin/env python3
"""
Extract claims from a codebase.

Usage:
    python extract.py <project_path> [--output <file>]

Outputs YAML to stdout or file.
"""

import argparse
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def extract_claims(project_path: str) -> dict[str, Any]:
    """Extract claims from a project directory."""
    path = Path(project_path).resolve()

    if not path.exists():
        raise ValueError(f"Path does not exist: {path}")

    claims = []
    claim_id = 0

    # Patterns for different claim types
    contract_patterns = [
        # HTTP status codes
        (r'return.*(?:status|status_code)\s*=\s*(\d{3})', 'Returns HTTP {0}'),
        (r'Response\(.*status=(\d{3})', 'Returns HTTP {0}'),
        (r'raise.*(?:Http)?(\d{3})', 'Can raise HTTP {0}'),
        # Auth patterns
        (r'@(?:require_)?auth|@login_required', 'Requires authentication'),
        (r'if not.*(?:authenticated|logged_in|is_admin)', 'Has authorization check'),
        # Validation
        (r'raise (?:ValidationError|ValueError)', 'Validates input'),
    ]

    belief_patterns = [
        # Performance comments
        (r'#.*(?:fast|slow|performance|optimize|cache)', None),
        (r'#.*(?:O\([^)]+\))', None),  # Big O notation
        # Assumptions
        (r'#.*(?:assume|assuming|should be|must be)', None),
        (r'#.*(?:typically|usually|most|often)', None),
    ]

    spark_patterns = [
        # TODOs and FIXMEs
        (r'#\s*TODO:?\s*(.+)', 'TODO: {0}'),
        (r'#\s*FIXME:?\s*(.+)', 'FIXME: {0}'),
        (r'#\s*FUTURE:?\s*(.+)', 'Future: {0}'),
    ]

    # File extensions to scan
    code_extensions = {'.py', '.js', '.ts', '.go', '.rs', '.java', '.rb'}

    for root, dirs, files in os.walk(path):
        # Skip common non-code directories
        dirs[:] = [d for d in dirs if d not in {
            '.git', 'node_modules', '__pycache__', '.venv', 'venv',
            'dist', 'build', '.next', 'target'
        }]

        for file in files:
            file_path = Path(root) / file

            if file_path.suffix not in code_extensions:
                continue

            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            rel_path = file_path.relative_to(path)

            for line_num, line in enumerate(content.splitlines(), 1):
                # Check contract patterns
                for pattern, template in contract_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        claim_id += 1
                        statement = template.format(*match.groups()) if template else match.group(0)
                        claims.append({
                            'id': f'{claim_id:03d}',
                            'type': 'contract',
                            'statement': statement,
                            'source_file': f'{rel_path}:{line_num}',
                            'source_text': line.strip(),
                            'confidence': 'high',
                        })

                # Check belief patterns
                for pattern, template in belief_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        claim_id += 1
                        claims.append({
                            'id': f'{claim_id:03d}',
                            'type': 'belief',
                            'statement': line.strip().lstrip('#').strip(),
                            'source_file': f'{rel_path}:{line_num}',
                            'source_text': line.strip(),
                            'confidence': 'medium',
                        })

                # Check spark patterns
                for pattern, template in spark_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        claim_id += 1
                        statement = template.format(*match.groups()) if template else match.group(0)
                        claims.append({
                            'id': f'{claim_id:03d}',
                            'type': 'spark',
                            'statement': statement,
                            'source_file': f'{rel_path}:{line_num}',
                            'source_text': line.strip(),
                            'confidence': 'low',
                        })

    return {
        'source': {
            'path': str(path),
            'analyzed': datetime.now().isoformat(),
        },
        'claims': claims,
    }


def main():
    parser = argparse.ArgumentParser(description='Extract claims from codebase')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    args = parser.parse_args()

    try:
        result = extract_claims(args.project_path)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    yaml_output = yaml.dump(result, default_flow_style=False, sort_keys=False)

    if args.output:
        Path(args.output).write_text(yaml_output)
        print(f"Claims written to {args.output}")
    else:
        print(yaml_output)

    print(f"\nFound {len(result['claims'])} claims", file=__import__('sys').stderr)
    return 0


if __name__ == '__main__':
    exit(main())
