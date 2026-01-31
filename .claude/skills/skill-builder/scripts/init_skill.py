#!/usr/bin/env python3
"""
Initialize a new skill directory structure.

Usage:
    python init_skill.py <skill-name> [--path <base-path>]

Creates:
    <base-path>/<skill-name>/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
"""

import argparse
from pathlib import Path

SKILL_TEMPLATE = '''---
name: {name}
description: "TODO: Describe when to use this skill. Be specific about triggers."
---

# {title}

TODO: Brief description of what this skill does.

## Process

1. TODO: First step
2. TODO: Second step
3. TODO: Third step

## Scripts

- `scripts/example.py` — TODO: What it does

## References

- `references/patterns.md` — TODO: What knowledge it provides
'''

SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""
TODO: Script description.

Usage:
    python {name}.py <args>
"""

import sys


def main():
    print("TODO: Implement {name}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
'''

REFERENCE_TEMPLATE = '''# {title}

TODO: Add domain knowledge here.

## Patterns

TODO: Common patterns.

## Examples

TODO: Examples.
'''


def init_skill(name: str, base_path: str = '.') -> None:
    """Initialize a new skill directory."""
    base = Path(base_path)
    skill_dir = base / name

    if skill_dir.exists():
        print(f"Error: {skill_dir} already exists")
        return

    # Create directories
    (skill_dir / 'scripts').mkdir(parents=True)
    (skill_dir / 'references').mkdir()
    (skill_dir / 'assets').mkdir()

    # Create SKILL.md
    title = name.replace('-', ' ').title()
    skill_content = SKILL_TEMPLATE.format(name=name, title=title)
    (skill_dir / 'SKILL.md').write_text(skill_content)

    # Create example script
    script_content = SCRIPT_TEMPLATE.format(name='example')
    script_path = skill_dir / 'scripts' / 'example.py'
    script_path.write_text(script_content)
    script_path.chmod(0o755)

    # Create example reference
    ref_content = REFERENCE_TEMPLATE.format(title='Patterns')
    (skill_dir / 'references' / 'patterns.md').write_text(ref_content)

    # Create .gitkeep in assets
    (skill_dir / 'assets' / '.gitkeep').touch()

    print(f"Created skill: {skill_dir}")
    print(f"  - SKILL.md (edit this!)")
    print(f"  - scripts/example.py")
    print(f"  - references/patterns.md")
    print(f"  - assets/")


def main():
    parser = argparse.ArgumentParser(description='Initialize a new skill')
    parser.add_argument('name', help='Skill name (use-kebab-case)')
    parser.add_argument('--path', default='.', help='Base path for skill directory')
    args = parser.parse_args()

    # Validate name
    if not args.name.replace('-', '').isalnum():
        print("Error: Skill name should be kebab-case alphanumeric")
        return 1

    init_skill(args.name, args.path)
    return 0


if __name__ == '__main__':
    exit(main())
