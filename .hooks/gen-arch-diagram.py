#!/usr/bin/env python3
"""
Ansible Collection Mermaid Diagram Generator Pre-commit Hook

Generates a Mermaid diagram from an Ansible collection structure
and updates repo README.
"""

from pathlib import Path
import sys
import re

class AnsibleCollectionAnalyzer:
    def __init__(self, collection_path: str):
        self.collection_path = Path(collection_path)
        self.structure = {
            'roles': [],
            'plugins': [],
            'playbooks': []
        }

    def analyze(self):
        """Analyze the Ansible collection structure"""
        # Analyze roles
        roles_path = self.collection_path / 'roles'
        if roles_path.exists():
            for role_dir in sorted(roles_path.iterdir(), key=lambda p: p.name):
                if role_dir.is_dir() and not role_dir.name.startswith('.'):
                    self.structure['roles'].append({
                        'name': role_dir.name,
                        'has_molecule': (role_dir / 'molecule').exists(),
                        'description': self._read_role_description(role_dir),
                    })

        # Analyze plugins
        plugins_path = self.collection_path / 'plugins' / 'modules'
        if plugins_path.exists():
            for plugin_file in sorted(plugins_path.glob('*.py'), key=lambda p: p.name):
                if not plugin_file.name.startswith('__'):
                    self.structure['plugins'].append(plugin_file.stem)

        # Analyze playbooks
        playbooks_path = self.collection_path / 'playbooks'
        if playbooks_path.exists():
            for item in sorted(playbooks_path.iterdir(), key=lambda p: p.name):
                if item.is_dir() and not item.name.startswith('.'):
                    self.structure['playbooks'].append({
                        'name': item.name,
                        'has_molecule': (item / 'molecule').exists()
                    })

        return self.structure

    @staticmethod
    def _read_role_description(role_dir: Path) -> str:
        """Extract ``galaxy_info.description`` from a role's ``meta/main.yml``.

        Hand-rolled so we don't pull in PyYAML as a hook dep. Anchors on the
        ``galaxy_info:`` block specifically so an unrelated ``description:``
        key elsewhere in the file (e.g. ``argument_specs``) can't shadow it.
        Handles plain values, quoted values, and YAML block scalars (``|`` /
        ``>`` with optional ``-`` / ``+`` chomping). Inline ``# …`` comments
        are stripped from every value form — strictly YAML keeps ``#``
        literal inside block scalars, but the output here is a README table
        cell, not program input, so user-friendlier wins.
        """
        meta_path = role_dir / 'meta' / 'main.yml'
        if not meta_path.exists():
            return ''
        try:
            text = meta_path.read_text()
        except OSError:
            return ''

        lines = text.splitlines()
        galaxy_info_re = re.compile(r'^galaxy_info:\s*$')
        # Match real top-level keys (an identifier at col 0 followed by ``:``)
        # so comments and ``---``/``...`` document markers don't end the block.
        top_key_re = re.compile(r'^[A-Za-z_][\w-]*\s*:')
        desc_re = re.compile(r'^(\s+)description:\s*(.*)$')
        block_indicator_re = re.compile(r'^[|>][-+]?\s*$')
        comment_re = re.compile(r'\s+#.*$')

        start_idx = next(
            (i + 1 for i, line in enumerate(lines) if galaxy_info_re.match(line)),
            None,
        )
        if start_idx is None:
            return ''
        end_idx = next(
            (j for j in range(start_idx, len(lines)) if top_key_re.match(lines[j])),
            len(lines),
        )

        for i in range(start_idx, end_idx):
            m = desc_re.match(lines[i])
            if not m:
                continue
            key_indent = len(m.group(1))
            value = m.group(2).strip()

            if value and not block_indicator_re.match(value):
                value = comment_re.sub('', value).strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                return value

            # Block scalar — collect more-indented continuation lines and
            # fold into a single line; table cells can't render newlines.
            parts = []
            for cont in lines[i + 1:end_idx]:
                if not cont.strip():
                    continue
                stripped = cont.lstrip()
                cont_indent = len(cont) - len(stripped)
                if cont_indent <= key_indent:
                    break
                parts.append(comment_re.sub('', stripped.rstrip()))
            return ' '.join(p for p in parts if p)

        return ''

def generate_mermaid(structure):
    """Generate Mermaid diagram"""
    lines = ["```mermaid", "graph TD"]
    lines.append("    Collection[Ansible Collection]")

    # Add plugins
    if structure['plugins']:
        lines.append("    Collection --> Plugins[🔌 Plugins]")
        for i, plugin in enumerate(structure['plugins']):
            lines.append(f"    Plugins --> P{i}[{plugin}]")

    # Add roles
    if structure['roles']:
        lines.append("    Collection --> Roles[⚙️ Roles]")
        for i, role in enumerate(structure['roles']):
            role_label = role['name']
            if role['has_molecule']:
                role_label += " 🧪"
            lines.append(f"    Roles --> R{i}[{role_label}]")

    # Add playbooks
    if structure['playbooks']:
        lines.append("    Collection --> Playbooks[📚 Playbooks]")
        for i, playbook in enumerate(structure['playbooks']):
            pb_label = playbook['name']
            if playbook['has_molecule']:
                pb_label += " 🧪"
            lines.append(f"    Playbooks --> PB{i}[{pb_label}]")

    lines.append("```")
    return '\n'.join(lines)

def generate_roles_table(structure):
    """Generate a markdown table linking to each role's README."""
    lines = [
        "| Role | Description |",
        "| ---- | ----------- |",
    ]
    for role in structure['roles']:
        name = role['name']
        desc = role.get('description') or '_No description_'
        # Escape pipes in descriptions so they don't break the table
        desc = desc.replace('|', '\\|')
        lines.append(f"| [`{name}`](roles/{name}/README.md) | {desc} |")
    return '\n'.join(lines)

def update_readme_section(content, start_marker, end_marker, replacement):
    """Replace text between two marker lines in README content.

    Returns the new content, or None if either marker is missing.
    """
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)
    if start_pos == -1 or end_pos == -1 or end_pos < start_pos:
        return None
    return (
        content[:start_pos + len(start_marker)]
        + '\n\n' + replacement + '\n\n'
        + content[end_pos:]
    )

def update_readme(mermaid_content):
    """Update README.md with the generated Mermaid diagram"""
    readme_path = Path('README.md')

    if not readme_path.exists():
        print("❌ README.md not found")
        return False

    readme_content = readme_path.read_text()

    # Define markers for the architecture section
    start_marker = "## Architecture Diagram"
    end_marker = "## Requirements"  # The next section after Architecture Diagram

    # Find the start and end positions
    start_pos = readme_content.find(start_marker)
    if start_pos == -1:
        print("❌ Could not find '## Architecture Diagram' section in README.md")
        return False

    end_pos = readme_content.find(end_marker, start_pos)
    if end_pos == -1:
        # If we can't find the next section, look for the next ## heading
        next_section_pattern = re.compile(r'\n## (?!Architecture Diagram)')
        match = next_section_pattern.search(readme_content, start_pos + len(start_marker))
        if match:
            end_pos = match.start() + 1  # +1 to keep the newline before the next section
        else:
            print("❌ Could not find the end of the Architecture Diagram section")
            return False

    # Build the new architecture section
    new_section = f"{start_marker}\n\n{mermaid_content}\n\n"

    # Replace the section
    new_readme = readme_content[:start_pos] + new_section + readme_content[end_pos:]

    # Write back to README
    readme_path.write_text(new_readme)

    return True

def update_readme_roles_table(roles_table):
    """Replace the auto-generated roles table block in README.md."""
    readme_path = Path('README.md')
    if not readme_path.exists():
        print("❌ README.md not found")
        return False

    content = readme_path.read_text()
    new_content = update_readme_section(
        content,
        '<!-- ROLES TABLE START -->',
        '<!-- ROLES TABLE END -->',
        roles_table,
    )
    if new_content is None:
        print("❌ Could not find roles table markers in README.md")
        return False

    readme_path.write_text(new_content)
    return True

def main():
    """Main function for pre-commit hook"""
    # Analyze collection from current directory
    analyzer = AnsibleCollectionAnalyzer('.')
    structure = analyzer.analyze()

    # Generate Mermaid diagram and roles table
    mermaid_content = generate_mermaid(structure)
    roles_table = generate_roles_table(structure)

    # Update README.md
    diagram_ok = update_readme(mermaid_content)
    table_ok = update_readme_roles_table(roles_table)
    if diagram_ok and table_ok:
        print("✅ Architecture diagram and roles table updated in README.md")
        print(f"\nCollection summary:")
        print(f"  • Roles: {len(structure['roles'])}")
        print(f"  • Plugins: {len(structure['plugins'])}")
        print(f"  • Playbooks: {len(structure['playbooks'])}")

        # Check if the README was actually modified (unstaged changes)
        import subprocess
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'README.md'],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            print("⚠️ README.md was updated. Please stage and re-commit.")
            return 1

        return 0
    else:
        print("❌ Failed to update README.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
