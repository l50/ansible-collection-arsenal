# Ansible Collection: l50 arsenal

[![License](https://img.shields.io/github/license/l50/ansible-collection-arsenal?label=License&style=flat&color=blue&logo=github)](https://github.com/l50/ansible-collection-arsenal/blob/main/LICENSE)
[![Pre-Commit](https://github.com/l50/ansible-collection-arsenal/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/l50/ansible-collection-arsenal/actions/workflows/pre-commit.yaml)
[![Molecule Test](https://github.com/l50/ansible-collection-arsenal/actions/workflows/molecule.yaml/badge.svg)](https://github.com/l50/ansible-collection-arsenal/actions/workflows/molecule.yaml)
[![Renovate](https://github.com/l50/ansible-collection-arsenal/actions/workflows/renovate.yaml/badge.svg)](https://github.com/l50/ansible-collection-arsenal/actions/workflows/renovate.yaml)

This Ansible collection provides offsec tools, configurations, and utilities
that I employ regularly.

## Requirements

- Ansible 2.15 or higher

## Installation

Install the Workstation collection from Ansible Galaxy:

```bash
ansible-galaxy collection install git+https://github.com/l50/ansible-collection-arsenal.git,main
```

## Roles

### Sliver

Installs and configures [Sliver](https://github.com/BishopFox/sliver), a
cross-platform implant framework.

### TTPForge

Installs and configures [TTPForge](https://github.com/facebookincubator/TTPForge),
a Cybersecurity Framework for developing, automating, and executing attacker
Tactics, Techniques, and Procedures (TTPs).

### Attack Box

Creates an attack box for penetration testing and red teaming.

### Vulnerable Windows Scenarios

Sets up vulnerable Windows scenarios for use in training and testing of
cybersecurity tools and techniques.

## Usage

Include the roles from this collection in your playbook. Here's an example:

```yaml
---
- name: Provision container
  hosts: localhost
  roles:
    - l50.arsenal.sliver
    - l50.arsenal.ttpforge
    - l50.arsenal.attack_box
```

## License

This collection is licensed under the MIT License - see the [LICENSE](LICENSE)
file for details.

## Support

- Repository: [l50/ansible-collection-arsenal](http://github.com/l50/ansible-collection-arsenal)
- Issue Tracker: [GitHub Issues](https://github.com/l50/ansible-collection-arsenal/issues)

## Authors

- Jayson Grace ([techvomit.net](https://techvomit.net))
