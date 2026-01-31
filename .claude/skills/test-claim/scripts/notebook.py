#!/usr/bin/env python3
"""
Generate experiment notebook from claims.yaml.

Usage:
    python notebook.py <experiment_dir>

Creates experiment.ipynb in the specified directory.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import yaml


def create_notebook(experiment_dir: str) -> None:
    """Generate experiment.ipynb from claims.yaml."""
    exp_path = Path(experiment_dir)
    claims_file = exp_path / 'claims.yaml'
    notebook_file = exp_path / 'experiment.ipynb'

    if not claims_file.exists():
        print(f"Error: {claims_file} not found", file=sys.stderr)
        sys.exit(1)

    with open(claims_file) as f:
        data = yaml.safe_load(f)

    cells = []

    # Title cell
    exp_name = data.get('experiment', {}).get('name', 'Experiment')
    cells.append(markdown_cell(f"# {exp_name}\n\n**Created:** {datetime.now().isoformat()}"))

    # Overview cell
    source = data.get('experiment', {}).get('source', 'Unknown')
    cells.append(markdown_cell(f"## Overview\n\n**Source:** {source}"))

    # Claims section
    for claim in data.get('claims', []):
        claim_id = claim.get('id', '???')
        claim_type = claim.get('type', 'unknown')
        statement = claim.get('statement', 'No statement')

        # Claim header
        cells.append(markdown_cell(f"## Claim {claim_id}: {claim_type.upper()}\n\n> {statement}"))

        # Criteria
        criteria = claim.get('criteria', [])
        if criteria:
            criteria_md = "### Kill Criteria\n\n" + "\n".join(f"- {c}" for c in criteria)
            cells.append(markdown_cell(criteria_md))

        # Test (if present)
        test = claim.get('test', {})
        if test:
            method = test.get('method', '')
            code = test.get('code', '')

            cells.append(markdown_cell(f"### Test\n\n**Method:** {method}"))

            if code:
                cells.append(code_cell(code))

        # Observations (if present)
        obs = claim.get('observations', {})
        if obs:
            raw = obs.get('raw', '')
            unexpected = obs.get('unexpected', '')

            obs_md = "### Observations\n\n```\n" + raw + "\n```"
            if unexpected:
                obs_md += f"\n\n**Unexpected:** {unexpected}"
            cells.append(markdown_cell(obs_md))

        # Verdict (if present)
        verdict = claim.get('verdict')
        if verdict:
            reasoning = claim.get('reasoning', '')
            verdict_md = f"### Verdict: **{verdict}**\n\n{reasoning}"
            cells.append(markdown_cell(verdict_md))

        # Mutations (if present)
        mutations = claim.get('mutations', [])
        if mutations:
            mut_md = "### Mutations\n\nNew claims from this test:\n\n" + "\n".join(f"- {m}" for m in mutations)
            cells.append(markdown_cell(mut_md))

    # Jester reflection (if present)
    jester = data.get('jester', {})
    if jester:
        reflection = jester.get('reflection', '')
        if reflection:
            cells.append(markdown_cell(f"## Jester's Reflection\n\n*{reflection}*"))

    # Create notebook
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "cells": cells
    }

    with open(notebook_file, 'w') as f:
        json.dump(notebook, f, indent=2)

    print(f"Created {notebook_file}")


def markdown_cell(content: str) -> dict:
    """Create a markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": content.split('\n')
    }


def code_cell(content: str) -> dict:
    """Create a code cell."""
    return {
        "cell_type": "code",
        "metadata": {},
        "source": content.split('\n'),
        "outputs": [],
        "execution_count": None
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python notebook.py <experiment_dir>", file=sys.stderr)
        sys.exit(1)

    create_notebook(sys.argv[1])


if __name__ == '__main__':
    main()
