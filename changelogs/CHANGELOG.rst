==============================================
Arsenal Ansible Collection 1.0.0 Release Notes
==============================================

.. contents:: Topics

v1.0.0
======

Added
-----

- Added `molecule-plugins[docker]` dependency in GitHub Actions.
- Added a new GitHub Actions workflow `molecule.yaml` for running Molecule tests on pull requests and pushes.
- Added automated documentation generation for magefile utilities
- Added depth and force options to git clone tasks in roles.
- Added playbooks and Molecule tests for Atomic Red Team and TTPForge.
- Added sliver role and playbook
- Added task to delete unnecessary tools folder in Molecule workflows.
- Automated Release Playbook - Introduced `galaxy-deploy.yml`, an automated release playbook for publishing the collection to Ansible Galaxy.
- Included callback plugin `profile_tasks.py` for task profiling.
- Included user and shell variable updates in roles for consistency.
- Introduced new role `ttpforge` for TTPForge framework.
- Renovate Bot Configuration - Updated Renovate Bot configurations to reflect the new repository structure and naming.

Changed
-------

- Enhanced shell profile updates for users.
- Improved package installation tasks in roles.
- Modified gmake command to utilize all available CPU cores.
- Refactored roles to use blocks for better readability.
- Updated `README.md` to reflect new repository URL and added TTPForge role.
- Updated default versions for Go and plugins in roles.
- Updated dependencies in `.pre-commit-config.yaml` for various tools.

Removed
-------

- Deleted unnecessary `.gitignore` and `LICENSE` files from sliver role.
- Removed redundant files and old configurations from sliver role.
