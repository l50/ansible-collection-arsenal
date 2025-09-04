==============================================
Arsenal Ansible Collection 1.0.5 Release Notes
==============================================

.. contents:: Topics

v1.0.5
======

Added
-----

- Added SSL certificate environment variables for Go module downloads.
- Added `.templatesyncignore` file to control template synchronization.
- Added `area/plugins` label for plugin directory changes.
- Added `create.yml` and `destroy.yml` to all Molecule test scenarios.
- Added `go mod tidy` step before compilation in sliver and ttpforge roles.
- Added alternative local build and install method for the collection in README
- Added architecture diagram generation with Mermaid for collection visualization.
- Added comprehensive README documentation for all playbooks.
- Added custom Docsible template for automated Ansible role documentation.
- Added development environment setup and documentation generation instructions to README
- Added markdownlint configuration replacing mdstyle.rb.
- Added renovate dashboard label configuration.
- Added template sync workflow for infrastructure file synchronization.
- Added use of Docsible for automated role documentation to README

Changed
-------

- Enhanced error handling and fallback mechanisms in Go binary detection.
- Fixed ASDF installation checks to verify both data directory and binary.
- Fixed sliver role operator config generation with proper permissions.
- Fixed ttpforge compilation issues with proper environment variable setup.
- Fixed user home directory detection for different OS families.
- Improved ASDF plugin version management with renovate datasource annotations.
- Improved Molecule test configurations with consistent provisioner settings.
- Refactored sliver role to use single user configuration instead of user list.
- Refactored ttpforge role with improved user home directory detection.
- Simplified playbook configurations removing redundant variable definitions.
- Standardized shell configuration to use .bashrc instead of .bash_profile.
- Updated Ansible collection dependencies (amazon.aws to 10.1.1, ansible.windows to 3.2.0, community.docker to 4.7.0, community.general to 11.2.1).
- Updated GitHub Actions to latest versions (create-github-app-token, checkout, setup-python, cache).
- Updated Go version to 1.24.4 and Python to 3.13.3 in CI workflows.
- Updated renovate configuration with improved automerge rules and custom regex managers.

Removed
-------

- Removed `generate_docs.py` in favor of Docsible documentation generation.
- Removed `mdstyle.rb` linter configuration file.
- Removed redundant user creation tasks from playbook converge files.
- Removed unused `install-sliver.sh.j2` template.

v1.0.4
======

Release Summary
---------------

Improved TTPForge role with robust ASDF and Go setup, modernized playbooks, fixed shell errors, and updated multiple dependencies across the collection.

Added
-----

- Added dynamic `go` binary detection via multiple fallback mechanisms.
- Added missing items to gitignore.
- Bumped max-parallel to 4 for playbook tests.
- Ensured environment variables like `GOPATH` and `GO111MODULE` are set.
- Implemented robust Go install logic with direct asdf shell commands.
- Improved compilation step to use explicitly detected `go` binary.
- Modernized ttpforge playbook.
- Switched `cowdogmoo.workstation` to Git-based source in `requirements.yml`.
- Validated directory structure and executable presence post-install.
- Verified both ASDF binary and data directory presence before installing.

Changed
-------

- Differentiated group keys in workflow based on event type for better control of workflow execution.
- Refactored `ttpforge` compilation to avoid reliance on shell rc files.
- Replaced old manual directory permission check with automated rebuild logic.
- Updated `molecule.yaml` concurrency logic to only cancel in-progress jobs for non-Renovate PRs.
- Updated all ASDF references to use `asdf_data_dir` and `asdf_bin_dir`.

Removed
-------

- Removed inline comment about `bash_profile` creation being conditional.
- Removed old system package.

v1.0.3
======

Release Summary
---------------

Major refactors to Molecule testing, improved automation workflows, better role and playbook organization, and removal of deprecated Windows scenarios.

Added
-----

- Added `area/molecule` label to track molecule-related changes.
- Added `ttpforge_get_user_home.yml` task file to dynamically determine home directories.
- Added logging and error collection for failed Molecule tests to improve debugging.
- Implemented input validation for role and playbook names in the Molecule workflow to prevent incorrect invocations.
- Introduced role and playbook-specific labels in `.github/labeler.yaml` and `.github/labels.yaml` for better issue categorization.
- Introduced targeted Molecule testing for individual roles and playbooks via workflow dispatch inputs.
- Refactored and modularized `ttpforge` role by introducing a dedicated `setup.yml` task file.

Changed
-------

- Changed `sliver_users` in `sliver/defaults/main.yml` to dynamically set usernames based on environment variables.
- Improved concurrency settings in GitHub Actions workflows to ensure efficient job execution.
- Refactored `.github/labeler.yaml` and `.github/labels.yaml` to use consistent color codes and descriptions.
- Removed Red Hat Rocky Linux 9 test images from `molecule.yml` in `atomic-red-team`, `sliver`, and `ttpforge` playbooks.
- Standardized error handling in Molecule test jobs.
- Updated Ansible Galaxy version to `1.0.3` in `galaxy.yml`.
- Updated Renovate configuration to track molecule playbook dependencies (`playbooks/.+/molecule/.+/molecule.yml`).
- Updated `actions/cache` to v4.2.0 for optimized caching in Molecule workflows.
- Updated `actions/setup-go` to v5 in pre-commit workflows.
- Updated `actions/setup-python` to v5.4.0 in all workflows to maintain compatibility with the latest Python releases.
- Updated `ttpforge/defaults/main.yml` to use cleaner per-user configuration instead of global installs.
- Upgraded `actions/create-github-app-token` across workflows to v1.11.2 for security and compatibility improvements.

Removed
-------

- Cleaned up unused permissions in `meta-sync-labels.yaml`, `meta-labeler.yaml`, and `molecule.yaml` workflows.
- Removed `area/ansible-role` and `area/ansible-playbook` labels, replacing them with more specific role/playbook labels.
- Removed hardcoded `build_user` assignment in `sliver/tasks/main.yml`, making the process more dynamic.
- Removed redundant Rocky Linux 9 test images from `molecule.yml` in `atomic-red-team`, `sliver`, and `ttpforge` playbooks.
- Removed redundant task definitions in `ttpforge` and modularized into `setup.yml` and `ttpforge_get_user_home.yml`.
- Removed unnecessary `Vulnerable Windows Scenarios` section from `README.md`.

v1.0.2
======

Release Summary
---------------

Enhanced security compliance, task management, and automation workflows.

Changed
-------

- Added `permissions` blocks for GitHub Actions workflows to enhance security compliance.
- Deleted redundant `magefiles` directory, replacing it with `Taskfile.yaml` for task management.
- Introduced `.hooks/requirements.txt` to centralize Python dependencies for pre-commit and Molecule testing.
- Renamed `area/magefiles` to `area/taskfiles` in `.github/labeler.yaml` and `.github/labels.yaml`.
- Updated Ansible Galaxy version to `1.0.1` in `galaxy.yml`.
- Updated GitHub Actions workflows (`meta-labeler.yaml`, `meta-sync-labels.yaml`, `molecule.yaml`) for improved label syncing and Molecule testing on schedule.
- Updated Renovate configuration to align with new `Taskfile.yaml` structure and added Ansible collection grouping rules.

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

Release Summary
---------------

Initial release with roles for Atomic Red Team, TTPForge, and Sliver.

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
