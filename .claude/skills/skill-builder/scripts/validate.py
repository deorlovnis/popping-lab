#!/usr/bin/env python3
"""
Validate skill directory structure.

Usage:
    python validate.py <skill-path>

Checks:
    - SKILL.md exists with valid frontmatter
    - Description is not TODO
    - Scripts are executable
    - References exist if mentioned
"""

import argparse
import re
import sys
from pathlib import Path

import yaml


def validate_skill(skill_path: str) -> list[str]:
    """Validate a skill directory, return list of errors."""
    path = Path(skill_path)
    errors = []

    # Check directory exists
    if not path.exists():
        return [f"Path does not exist: {path}"]

    if not path.is_dir():
        return [f"Not a directory: {path}"]

    # Check SKILL.md exists
    skill_md = path / 'SKILL.md'
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
        return errors

    # Parse SKILL.md
    content = skill_md.read_text()

    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("SKILL.md missing YAML frontmatter")
        return errors

    try:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML frontmatter: {e}")
        return errors

    # Check required fields
    if 'name' not in frontmatter:
        errors.append("Frontmatter missing 'name' field")

    if 'description' not in frontmatter:
        errors.append("Frontmatter missing 'description' field")
    elif 'TODO' in frontmatter.get('description', ''):
        errors.append("Description contains TODO - needs to be filled in")

    # Check scripts are executable
    scripts_dir = path / 'scripts'
    if scripts_dir.exists():
        for script in scripts_dir.glob('*.py'):
            if not script.stat().st_mode & 0o111:
                errors.append(f"Script not executable: {script.name}")

    # Check mentioned references exist
    body = content[frontmatter_match.end():]
    ref_mentions = re.findall(r'`references/([^`]+)`', body)
    refs_dir = path / 'references'

    for ref in ref_mentions:
        ref_path = refs_dir / ref
        if not ref_path.exists():
            errors.append(f"Referenced file missing: references/{ref}")

    # Check mentioned scripts exist
    script_mentions = re.findall(r'`scripts/([^`]+)`', body)

    for script in script_mentions:
        script_path = scripts_dir / script
        if not script_path.exists():
            errors.append(f"Referenced script missing: scripts/{script}")

    return errors


def main():
    parser = argparse.ArgumentParser(description='Validate skill structure')
    parser.add_argument('path', help='Path to skill directory')
    args = parser.parse_args()

    errors = validate_skill(args.path)

    if errors:
        print(f"Validation failed for {args.path}:")
        for error in errors:
            print(f"  - {error}")
        return 1
    else:
        print(f"Skill valid: {args.path}")
        return 0


if __name__ == '__main__':
    sys.exit(main())
