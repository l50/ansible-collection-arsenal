============================================================
CowDogMoo Workstation Ansible Collection 2.0.6 Release Notes
============================================================

.. contents:: Topics

v2.0.6
======

Release Summary
---------------

This release focuses on improving package management reliability, especially for Debian-based systems with better apt lock handling. Added support for Kali Linux package verification and simplified VNC service management. Several dependencies were also updated to their latest versions.

Added
-----

- Added Kali archive keyring installation task for Kali-based systems
- Added Molecule verification to ensure no apt/dpkg locks remain after package_management role runs
- Added `area/molecule` and `playbook/vnc_box` labels for improved PR categorization
- Added retry loop in package_management role to wait until apt locks are released

Changed
-------

- Fixed label formatting and added missing area label for playbooks
- Improved reliability of package installation on Debian-based systems
- Simplified VNC service setup by removing redundant XDG_RUNTIME_DIR handling
- Updated Debian package tasks to proactively prevent apt lock contention
- Updated actions/create-github-app-token from v2.0.2 to v2.0.6
- Updated adrienverge/yamllint from v1.37.0 to v1.37.1
- Updated community.docker from 4.5.2 to 4.6.0
- Updated renovatebot/github-action from v41.0.22 to v42.0.1

v2.0.5
======

Release Summary
---------------

Added VNC box playbook, thoroughly refactored ASDF role to support binary-based installs, improved service reliability, and updated numerous dependencies. Fixed issues with user home detection, shell integrations, and Molecule testing.

Added
-----

- Added Molecule scenario for VNC box playbook and registered it in the GitHub Actions workflow
- Added VNC box playbook (`playbooks/vnc_box/vnc_box.yml`) to configure a VNC workstation
- Added conditional check for ASDF completions directory in shell profile setup
- Added environment detection for GitHub Actions CI environments in ASDF role
- Added shell completions for ASDF in Bash and Zsh via `update_shell_profile.yml`
- Added verification for Golang functionality in ASDF Molecule tests

Changed
-------

- Addressed minor inaccuracy in releases.md
- Fixed ASDF path in dotfile configuration
- Fixed bug determining asdf_user_home for the root user
- Fixed bug in workstation playbook molecule tests
- Fixed idempotency issues in various roles
- Fixed issue with zsh_setup_get_user_home.yml to handle root user home on Linux and macOS
- Fixed naming issue causing molecule test failure for vnc_box playbook
- Improved ASDF shell profile setup for v0.16+ compatibility and CI environments
- Improved VNC service startup and cleanup reliability with better process handling
- Optimized task running documentation
- Refactored ASDF role to support binary-based installs with improved shell integration
- Switched VNC playbook and role tests to use Ubuntu 24.04 for testing
- Updated actions/setup-python from v5.5.0 to v5.6.0
- Updated ansible.windows from 2.8.0 to 3.0.0
- Updated ansible/ansible-lint from v25.1.3 to v25.4.0
- Updated community.general from 10.5.0 to 10.6.0
- Updated helm/helm from v3.17.2 to v1.17.3
- Updated kubernetes/kubernetes from v1.32.3 to v1.33.0
- Updated python/cpython from v3.13.2 to v3.13.3

v2.0.4
======

Release Summary
---------------

Improved VNC setup with enhanced systemd integration, more robust session management, and comprehensive verification. Added awscli to default asdf plugins and updated all plugin and Ansible collection versions.

Added
-----

- Added awscli as a new asdf plugin (version 2.24.0)
- Added comprehensive verification tests for VNC setup to validate configuration, services, and ports
- Added explicit cleanup tasks for VNC sessions to ensure clean restarts
- Added new `vnc_setup_depth` parameter to control color depth in VNC connections
- Added proper handling of user UIDs for improved VNC session management

Changed
-------

- Enhanced VNC systemd service template with improved error handling, environment variables, and restart policies
- Improved user shell detection in user_setup role using basename and pattern matching
- Refactored VNC setup role with modular task files for better organization and maintenance
- Refactored user_setup role to handle shell installation more robustly
- Updated Ansible collection versions: amazon.aws (9.1.1 to 9.3.0), ansible.windows (2.7.0 to 2.8.0), community.docker (4.3.1 to 4.5.2), community.general (10.3.0 to 10.5.0)
- Updated asdf plugin versions: golang (1.23.5 to 1.24.0), python (3.13.1 to 3.13.2), ruby (3.3.5 to 3.4.2), helm (3.17.0 to 3.17.2), kubectl (1.32.1 to 1.32.3)

Removed
-------

- Removed RedHat-specific testing platform from VNC setup molecule configuration

v2.0.3
======

Release Summary
---------------

Improved ASDF default shell handling and refactored ZSH setup verification for simplified user checks and dependency removal

Changed
-------

- Improved ZSH verification logic to assert correct `.oh-my-zsh` and `.zshrc` file existence with streamlined assertions
- Refactored ZSH setup verification to use `container_user` and `container_home` instead of `zsh_setup_users`
- Removed dependency on `cowdogmoo.workstation.zsh_setup` from the ASDF role
- Simplified verification tasks in ZSH setup by removing redundant user iteration
- Updated ASDF default shell setting to use `/bin/bash` instead of `/usr/bin/zsh` for non-MacOS systems

v2.0.2
======

Release Summary
---------------

Streamlined ZSH setup role with improved user management and added template synchronization capabilities for better repository maintenance

Added
-----

- Added `.templatesyncignore` file to control which files are synchronized
- Added template synchronization workflow for maintaining consistency across repositories

Changed
-------

- Enhanced user and group management in ZSH setup role
- Improved user home directory detection logic in ZSH setup
- Refactored ZSH setup role to use simplified user management
- Streamlined ZSH installation process with better environment handling
- Updated ZSH configuration to use predefined plugins list

Removed
-------

- Eliminated redundant user iteration in ZSH setup tasks
- Removed complex user enrichment tasks in favor of simpler direct user management

v2.0.1
======

Release Summary
---------------

Improved ASDF plugin installation process with better version handling and error management

Added
-----

- Added new template-based approach for ASDF plugin installation
- Improved handling of 'latest' version specifications in ASDF plugin installation

Changed
-------

- Enhanced ASDF plugin installation process with better version checking
- Improved plugin installation script with more robust error handling
- Refactored plugin installation to use templated shell script instead of direct shell commands

v2.0.0
======

Release Summary
---------------

Major refactor of Molecule tests, improved Renovate and GitHub Actions workflows, streamlined ASDF role, and removed deprecated tasks for a more maintainable codebase.

Added
-----

- Added dependency enforcement in the `asdf` role for `package_management` and `zsh_setup`
- Added input validation for Molecule workflows to ensure either a role or playbook is specified, not both
- Enhanced `asdf` role with dynamic variable assignments and improved user profile configurations
- Implemented local collection build and installation in GitHub Actions workflows for Molecule testing
- Introduced a `full_test` job in the Molecule workflow that runs all role and playbook tests when no specific input is given
- Introduced improved error handling and debugging for Ansible Molecule tests
- Introduced regex-based Renovate configuration for managing Helm and Ruby versions in `roles/asdf/defaults/main.yml`

Changed
-------

- Improved Ansible collection paths in Molecule configurations for consistency
- Improved Renovate configuration by extending from `config:recommended` instead of `config:base`
- Refactored Ansible pre-task execution in `playbooks/workstation` to dynamically determine user settings
- Refactored `molecule.yaml` files across roles to remove hardcoded platform specifications and improve test flexibility
- Removed Enterprise Linux (EL) testing references from multiple roles
- Replaced `roles/asdf/defaults/main.yml` structure with a more modular approach, removing nested user definitions
- Standardized `converge.yml` in Molecule tests to explicitly include roles instead of relying on implicit paths
- Updated package versions in `requirements.yml`, including Amazon AWS, Ansible Windows, community.docker, and community.general collections
- Updated various GitHub Actions workflows (`meta-labeler`, `meta-sync-labels`, `pre-commit`, `release`, and `renovate`) to use newer action versions for security and efficiency

Removed
-------

- Deleted deprecated `asdf_get_enriched_users.yml` and `install_asdf_plugins.yml` tasks, integrating functionality directly into the main playbook
- Eliminated redundant shell profile update tasks, consolidating them into `update_shell_profile.yml`
- Removed outdated Molecule role tests for Red Hat-based distributions
- Removed unnecessary `Taskfile.yaml` tasks for changelog generation and running GitHub Actions with Act

v1.9.4
======

Release Summary
---------------

Streamlined workflows, removed deprecated runzero_explorer role, and enhanced Renovate configurations for more efficient dependency management.

Added
-----

- Added Renovate configuration improvements, including auto-merging of Galaxy dependencies and enhanced grouping for Ansible Galaxy dependencies.
- Added `permissions` block to GitHub Actions workflows for enhanced security and proper access control.
- Introduced a new version of the GitHub Actions Molecule workflow for role testing, which now leverages environment variables to streamline dependency management and improve collection consistency.

Changed
-------

- Enhanced the Molecule workflow by using more dynamic environment variables and removing references to deprecated playbooks such as `runzero-explorer`.
- Improved GitHub Actions workflows (`pre-commit`, `release`, `renovate`) by updating action versions to the latest releases and adjusting dependency cache paths for more efficient workflow runs.
- Updated Renovate's base configuration to extend from `config:recommended` instead of `config:base` to adhere to best practices.
- Updated `Taskfile.yaml` to include Renovate tasks and improved the modular inclusion of other Taskfiles for consistency across different environments.
- Updated the `.github/labeler.yaml` and `.github/labels.yaml` files by removing the deprecated `runzero_explorer` role and playbook configurations.

Removed
-------

- Deleted the `autoMerge.json5` file under `.github/renovate/` as its contents were merged into a unified Renovate configuration file for better maintainability.
- Removed the deprecated `runzero_explorer` role, all associated tasks, variables, playbooks, and Molecule configurations, simplifying the repository and reducing maintenance overhead.

v1.9.3
======

Release Summary
---------------

Enhanced task management with Taskfile, improved role organization, and streamlined testing workflows

Added
-----

- Added `Taskfile.yaml` integration to replace Mage with centralized task management and modularized includes.
- Added distinct area and role labeling in `.github/labeler.yaml` for improved categorization of changes.
- Implemented new Python callback plugin `profile_tasks.py` in the `vnc_setup` role for task profiling during testing.
- Introduced the `.hooks/requirements.txt` file to centralize and streamline dependencies for pre-commit hooks and Molecule tests.
- Set concurrency in GitHub Actions workflows to prevent overlapping jobs and improve resource management.
- Updated label colors in `.github/labels.yaml` for clearer visual distinctions and modified descriptions for clarity.

Changed
-------

- Adjusted Renovate, GitHub Actions, and Molecule configurations for enhanced compatibility and version updates.
- Merged redundant tasks and removed deprecated task files to reduce workflow complexity.
- Refined Molecule workflow to improve testing and debug output management for failed Molecule runs.
- Updated README and `roles/asdf` with additional details and consistency in ASDF plugin management tasks.

Removed
-------

- Deprecated `setup_asdf_env.sh` script and transitioned to `setup_asdf_env.sh.j2` for templated environment setup.
- Removed outdated `.taskfiles` for Ansible linting and Molecule testing in favor of new Taskfile modularization.

v1.9.2
======

Release Summary
---------------

Migrated from Mage to Taskfile, updated roles for cross-platform support, and improved Renovate config and GitHub Actions workflows.

Added
-----

- Added PAT token generation to `meta-sync-labels.yaml` workflow in GitHub Actions.
- Added new tasks in the `zsh_setup` role to ensure that necessary packages, directories, and configurations are in place for both Unix-like and Windows systems.
- Added regex-based custom managers for golang, python, kubectl, and packer versions in `asdf` role defaults.
- Included author metadata in `getent_passwd.py` and `vnc_pw.py` for clarity and attribution.
- Introduced `.taskfiles` directory with tasks for changelog generation, linting, and running Molecule tests, providing Taskfile support.
- Introduced new Python callback plugin `profile_tasks.py` in the `vnc_setup` role for task profiling, helping to monitor task execution time during Molecule testing.
- Updated `molecule.yaml` and `pre-commit.yaml` workflows to use `task` instead of `mage`.

Changed
-------

- Migrated functionality from `magefiles` to `Taskfile`, centralizing task management in a single configuration.
- Modified Python module files to include author information.
- Modified the `user_setup` and `zsh_setup` roles to support both Unix-like and Windows systems, including adjustments to user creation and group management tasks.
- Refactored labels, replacing `area/magefiles` with `area/taskfiles` in labeler and labels configurations.
- Renamed and relocated `package_management` variables from `vars/main.yml` to `defaults/main.yml` for better variable management.
- Updated README to reflect the removal of Mage-related documentation and examples.
- Updated Renovate configuration to use proper JSON5 format with quotes around keys.
- Updated `actions/setup-go`, `actions/setup-python`, and `renovatebot/github-action` versions in GitHub Actions workflows.
- Updated `roles/asdf/defaults/main.yml` with version bumps for Ruby (3.3.4), Helm (3.15.4), Kubectl (1.30.3), and Packer (1.11.1).
- Updated installation instructions for Ansible Galaxy collection.
- Updated tasks in `asdf`, `vnc_setup`, and `zsh_setup` roles to conditionally apply `become` logic based on the operating system family (`Darwin`, `Windows`, etc.).
- Updated the `vnc_setup` role to check for systemd presence before configuring VNC services, improving compatibility across different Linux distributions.

Removed
-------

- Deleted `attack-box` playbook and associated Molecule test files, deprecating the `attack-box` configuration.
- Deprecated `magefiles` references and removed associated README.
- Removed `CreateRelease`, `GenerateMagePackageDocs`, and `RunMoleculeTests` functions from `magefiles`, transitioning task execution to the new `Taskfile` setup.
- Removed `magefiles` directory, `go.mod`, `go.sum`, and `magefile.go` in favor of `Taskfile` implementation.
- Removed all references to Mage functions such as `InstallDeps`, `RunPreCommit`, `GenChangeLog`, and their associated documentation in README.
- Removed dependencies on the `cowdogmoo.workstation.package_management` role from `asdf`, `vnc_setup`, and `zsh_setup` roles.
- Removed redundant tasks and variables associated with XFCE and VNC setup from the `package_management` role, simplifying the package installation process.

v1.9.1
======

Release Summary
---------------

Fixed breaking change for non-root users

Changed
-------

- Fixed breaking change for non-root users

v1.9.0
======

Release Summary
---------------

Enhanced roles with new profiling plugins, improved task handling, updated dependencies, and better consistency across multiple roles.

Added
-----

- Added Ansible environment variables in Molecule configurations.
- Added `molecule-plugins[docker]` to install dependencies in GitHub Actions.
- Added block tasks for downloading, extracting, and installing libyaml.
- Added depth and force options to git clone tasks in asdf and Sliver roles.
- Added tasks to delete unnecessary tools folder in Molecule workflows.
- Included `ensure_directory_exists.yml` for directory creation tasks.
- Introduced Ansible callback plugin `profile_tasks.py` for task profiling.
- Introduced user and shell variable updates in multiple roles for consistency.

Changed
-------

- Adjusted user setup tasks to improve clarity and consistency.
- Improved shell profile updates for users in multiple roles.
- Modified gmake command to utilize all available CPU cores in Sliver role.
- Refactored asdf role tasks to use blocks for better readability.
- Refactored package installation tasks in package_management role.
- Updated Magefile dependencies in `go.mod` and `go.sum`.
- Updated default versions for golang, python, ruby, helm, and kubectl plugins.
- Updated dependencies in `.pre-commit-config.yaml` for various tools.

Removed
-------

- Removed redundant debug task `getent_user_shell` from asdf role.

v1.8.0
======

Release Summary
---------------

Enhanced ASDF role configurability and maintenance, updated dependencies, and streamlined role tasks for better performance and reliability.

Added
-----

- Added shell environment setup tasks and improved user-specific ASDF configuration.
- Enhanced ASDF role with adjustments to shell configuration and global installation paths.
- Introduced handling for different user shell paths based on operating system.
- Updated GitHub Actions Renovate and pre-commit hooks to new versions.

Changed
-------

- Modified main.yml to streamline ASDF role processes, ensuring cleaner management of user and global installations.
- Refactored tasks to improve idempotency and user-specific configurations.
- Standardized handling of user directories and permissions across all tasks.
- Updated dependencies in go.mod and go.sum to newer versions.

v1.7.0
======

Added
-----

- Global ASDF installation directory creation
- Global installation of asdf
- Global installation support in Molecule tests for asdf role
- Install asdf globally or per user
- Path to the asdf install script
- asdf.sh script for global ASDF installation

Changed
-------

- Modified asdf vars to include default username and group
- Refactored asdf role to support global installation
- Updated default username and group based on the operating system in asdf role
- Updated gojq dependency in magefiles
- Updated main tasks in asdf role for global installation
- Updated package_individual_setup.yml in asdf role for global installation

v1.6.0
======

Release Summary
---------------

Enhancements in GitHub Actions workflows, updates to the `asdf` role, and general improvements.

Added
-----

- Added `molecule-plugins[docker]` to the dependencies in the Molecule GitHub Actions workflow.
- Added condition to exclude `root` user in `asdf_get_enriched_users.yml`.
- Added content-based `.tool-versions` file deployment in `main.yml`.
- Added initialization of `asdf_enriched_users` in `asdf_get_enriched_users.yml`.
- Added update functionality to the ASDF clone task in `main.yml`.

Changed
-------

- Changed the symlink creation path in the Molecule GitHub Actions workflow to use `$HOME`.
- Modified the `asdf_get_enriched_users.yml` task to ensure user home directory exists.
- Refactored the installation of dependencies in the Molecule GitHub Actions workflow.
- Removed the template for `.tool-versions` file.
- Simplified the deployment of `.tool-versions` file in `main.yml`.
- Updated GitHub Actions setup-python step to a new version.
- Updated Renovate Bot GitHub Action to a new version.
- Updated plugin versions in `asdf` role defaults.
- Updated the ASDF clone task to fetch updates if the repository already exists.

v1.5.0
======

Added
-----

- Added `getent` task to `asdf` and `zsh_setup` roles for fetching local user info
- Added docstring for new plugin; minor QOL updates
- Added macOS compatibility with custom `getent_passwd` plugin
- Debugging for enriched_asdf_enriched_users in asdf main task
- Shell specification for MacOSX in workstation playbook
- Task to ensure asdf directory is cloned for each user in asdf role
- Task to ensure user home directory exists before cloning asdf
- Updated `asdf` and `zsh_setup` roles to dynamically resolve user home directories

Changed
-------

- Adjusted `zsh_setup_get_enriched_users.yml` to align with changes in user creation and home directory setup
- Adjusted file and directory paths in asdf tasks to use `item.home`
- Adjusted loops in `asdf` role's `package_individual_setup.yml` for consistency
- Cleaned up unused variables in `zsh_setup` defaults and molecule verification
- Defined `zsh_setup_users` in zsh_setup main task for clarity
- Fixed issues with handling undefined `plugins` attribute in the `asdf` role
- Fixed naming scheme of enriched asdf users
- Included default variables in zsh_setup molecule verification
- Modified `asdf_get_enriched_users.yml`, `main.yml` in `user_setup`, and `zsh_setup_get_enriched_users.yml` to conditionally use `getent_passwd` module on macOS systems
- Modified `zsh_setup` role to ensure `shell` attribute is defined for users and to use Ansible's user module for creating users and home directories
- Modified main tasks in `asdf` and `zsh_setup` roles to use updated user variables
- Refactored `asdf_get_enriched_users.yml` and `zsh_setup_get_enriched_users.yml`
- Refactored `asdf_get_enriched_users.yml` to use Ansible's user module for creating users and home directories, eliminating the need for `getent`
- Refactored workstation playbook and roles for idempotency and user existence checks
- Removed redundant `set_fact` task in `zsh_setup` main.yml
- Renamed platform names in zsh_setup molecule configuration
- Resolved undefined variable errors related to the `shell` attribute in the `zsh_setup` role
- Simplified variable names and usage in asdf role
- Updated `getent` tasks to exclude macOS systems, ensuring compatibility
- Updated `main.yml` and `package_individual_setup.yml` in the asdf role to handle undefined `plugins` attribute more gracefully
- Updated asdf clone task to use `item.home` and added `become` statements
- Updated file and directory paths in zsh_setup verification tasks
- Updated paths and variable usage in zsh_setup tasks
- Updated shell profile update task in asdf role
- Updated user_setup to use ansible_facts for getent_passwd

Removed
-------

- Removed redundant user creation tasks in `asdf` and `zsh_setup` roles that were causing idempotency issues in playbooks

v1.4.0
======

Release Summary
---------------

Significant enhancements to asdf role, introduction of Molecule tests, and configuration improvements in this release.

Added
-----

- Enhanced asdf role with user-specific setup scripts.
- Logging configuration enhancements in the logging role.
- Molecule testing configurations for `attack-box` playbook.
- Package management improvements for different distributions.
- User setup and zsh setup roles in `attack-box.yml`.

Changed
-------

- Changed hosts from localhost to all in `attack-box.yml`.
- Simplified package management role with unified tasks for Debian and RedHat.
- Updated asdf role to remove OS-specific tasks and focus on user-based configuration.

Removed
-------

- Deprecated vnc_zsh role and associated files in favor of streamlined setup.
- Removed Windows support in asdf role's documentation.

v1.3.0
======

Release Summary
---------------

Extended `asdf` role functionality and improved project configurations.

Added
-----

- Enhanced asdf role with user-specific setup scripts.
- Logging configuration enhancements in the logging role.
- Molecule testing configurations for `attack-box` playbook.
- Package management improvements for different distributions.
- User setup and zsh setup roles in `attack-box.yml`.

Changed
-------

- Changed hosts from localhost to all in `attack-box.yml`.
- Simplified package management role with unified tasks for Debian and RedHat.
- Updated asdf role to remove OS-specific tasks and focus on user-based configuration.

Removed
-------

- Deprecated vnc_zsh role and associated files in favor of streamlined setup.
- Removed Windows support in asdf role's documentation.

v1.2.0
======

Release Summary
---------------

Refactored `asdf` and created new `vnc_zsh` role enhancing functionality.

Added
-----

- Failure conditions in `asdf` role's `check-and-download.yml`.
- Molecule setup for testing `vnc_zsh` role with various scenarios.
- OS-specific setup tasks and variables for Debian in `vnc_zsh` role.
- Unified `asdf_install_packages` variable for package installation.
- Variables, tasks, templates for configuring VNC and ZSH in `vnc_zsh` role.

Changed
-------

- Restructured table, moved variables, modified tasks in `asdf` role.
- Updated package installation tasks in `asdf` role's `setup-debian.yml`, `setup-redhat.yml`.

Removed
-------

- Windows support, redundant block in `asdf` role's `README.md` and `tasks/main.yml`.

v1.1.0
======

Release Summary
---------------

Extended `asdf` role functionality and improved project configurations.

Added
-----

- Added `ansible-galaxy` collection installation from GitHub repository in GitHub Actions workflow.
- Documentation Generation Hook: Implemented a pre-commit hook for automated documentation generation of Go packages.
- New Example Provision Playbook: Added `provision.yml` in the examples directory illustrating the usage of the `asdf` role.
- RedHat Specific Tasks: Created `setup-redhat.yml` for RedHat specific setup tasks within the `asdf` role.
- RedHat Support: Added support for RedHat-based systems in the `asdf` role.
- Shell Profile Update: Automated the update of shell profiles with ASDF settings ensuring idempotency.
- Test Enhancements: Expanded Molecule tests to verify the `asdf` role on RedHat and Debian-based systems.

Changed
-------

- ASDF Setup Logic: Modified the ASDF setup logic in `asdf` role for better clarity and maintainability.
- Error Handling Improvement: Corrected the error handling in `magefile.go` to reflect the correct variable.
- File Renames: Renamed linting configuration files to remove leading dots and comply with standard naming conventions.
- Refactored `pre-commit.yaml` to add new hooks for checking symlinks, private keys, and ensuring shebang scripts are executable.
- Refactored file addition in `pre-commit.yaml` to use a single `git add` command.
- Shell Profile Update: Enhanced the shell profile update tasks in `asdf` role to ensure idempotency and clarity.
- Updated `README.md` in both the repository root and `roles/asdf` directory to reflect new changes and provide clearer instructions.
- Updated `README.md` to reflect the new installation command using `git+https` URL.
- Updated `ansible-lint` and `yamllint` paths in `.pre-commit-config.yaml` to reflect the new file names.
- Updated `molecule.yaml` in GitHub Actions workflow to include `ansible-galaxy` collection installation step.
- Updated minimum Ansible version in `roles/asdf/meta/main.yml` to 2.14

Removed
-------

- Removed the separate ShellCheck repository in `.pre-commit-config.yaml` and consolidated ShellCheck hook under `jumanjihouse/pre-commit-hooks`.

v1.0.0
======

Release Summary
---------------

Added a new `asdf` role

Added
-----

- Added automated documentation generation for magefile utilities
- Automated Release Playbook - Introduced `galaxy-deploy.yml`, an automated release playbook for publishing the collection to Ansible Galaxy.
- Molecule Workflow - Added a new GitHub Actions workflow `molecule.yaml` for running Molecule tests on pull requests and pushes.
- Renovate Bot Configuration - Updated Renovate Bot configurations to reflect the new repository structure and naming.
- `molecule` configuration - Added new `molecule` configuration for the `asdf` role to support local testing and verification.
- asdf role - Added a new `asdf` role with enhanced functionality including OS-specific setup. Updated metadata and created new documentation under `roles/asdf/README.md` detailing role usage and variables.

Changed
-------

- GitHub Actions Workflows - Refactored the `release.yaml` workflow to align with Ansible collection standards, including updating working directory paths, setting up Python, installing dependencies, and automating the release to Ansible Galaxy.
- Pre-commit hooks - Added new pre-commit hooks for shell script validation and formatting.
- Refactored Ansible linting configuration - Moved the `.ansible-lint` configuration to `.ansible-lint.yaml` and adjusted linting rules. Also, added `mdstyle.rb` and `.mdlrc` for markdown linting configurations.
- Repository Metadata - Updated repository links in `README.md` and `galaxy.yml` to reflect the new repository naming and structure.
- Upgrade dependencies - Upgraded versions of pre-commit hooks and dependencies in `.pre-commit-config.yaml`, updated mage's `go.sum` to reflect the new dependency tree, and removed unused dependencies from mage's `go.sum`.

Removed
-------

- Removed old files in preparation for later refactoring.
- Windows Support for asdf role - Removed Windows support from `roles/asdf/README.md` as it is not supported in the tasks.
