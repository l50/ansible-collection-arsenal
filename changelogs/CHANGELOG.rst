==============================================
Arsenal Ansible Collection 1.0.1 Release Notes
==============================================

.. contents:: Topics

v1.0.1
======

Release Summary
---------------

New and updated roles for penetration testing, red teaming, and cybersecurity drills.

Added
-----

- Added new Molecule tests for the `attack_box` role, ensuring proper setup and configuration.
- Added role `vulnerable_windows_scenarios` to create vulnerable Windows environments for cybersecurity training and testing.
- Added tasks and configurations for SSH key management, wordlist setup, and package management within the `attack_box` role.
- Included playbook `vulnerable_windows_scenarios.yml` for deploying vulnerable Windows scenarios using AWS EC2 instances.
- Integrated new collections `amazon.aws` and `community.windows` in `requirements.yml` to enhance AWS and Windows functionalities.
- Introduced callback plugin `profile_tasks.py` for task profiling in the `attack_box` role.
- Introduced new role `attack_box` for setting up a Kali Linux-based attack box for penetration testing and red teaming.
- Updated `ttpforge` role to support dynamic user and shell configurations across different OS platforms, including Windows.

Changed
-------

- Enhanced GitHub Actions workflows (`molecule.yaml`) to include new roles (`attack_box`, `vulnerable_windows_scenarios`) and updated dependencies.
- Enhanced the `ttpforge` role by updating user management and shell assignment logic, improving cross-platform compatibility.
- Updated Go toolchain to `go1.23.0` and upgraded multiple Go dependencies for improved performance and security.
- Updated `README.md` to reflect the addition of the `attack_box` and `vulnerable_windows_scenarios` roles.

Removed
-------

- Removed the deprecated playbook `attack-box.yml` and replaced it with the updated `attack_box.yml`.

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
