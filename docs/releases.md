# Ansible Collection Release Process

This document outlines the process for creating new releases of this Ansible collection.

## Prerequisites

- [Taskfile](https://taskfile.dev/) installed on your system (`brew install go-task/tap/go-task`)
- [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog)
  installed (`pip install antsibull-changelog`)
- Git repository with proper credentials configured
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
  installed
- [Molecule](https://molecule.readthedocs.io/en/latest/installation.html)
  installed (for testing)
- [act](https://github.com/nektos/act) installed (for GitHub Actions local testing)
- [jq](https://stedolan.github.io/jq/download/) installed (for JSON processing)
- Docker installed (required for Molecule and act)

## Pre-Release Tasks

Before creating a release, perform these preparation steps:

1. **Run Molecule Tests**

   Run tests to ensure all roles work as expected:

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   task -y ansible:run-molecule-tests
   ```

   This command will:

   - Create a logs directory if it doesn't exist
   - Set the ANSIBLE_CONFIG environment variable
   - Run molecule tests for each role directory
   - Log all test output to logs/molecule_tests.log

   Or test a specific role/playbook using GitHub Actions locally:

   ```bash
   # Test a specific role
   export TASK_X_REMOTE_TASKFILES=1
   task -y ansible:run-molecule-action ROLE=sliver

   # Test a specific playbook
   export TASK_X_REMOTE_TASKFILES=1
   task -y ansible:run-molecule-action PLAYBOOK=ttpforge
   ```

   The run-molecule-action task will:

   - Clean up any existing act containers
   - Automatically handle ARM64 architecture on macOS
   - Run the GitHub Actions workflow with the specified role or playbook

1. **Lint Your Ansible Code**

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   task -y ansible:lint-ansible
   ```

   This runs ansible-lint with the configuration file at `.hooks/linters/ansible-lint.yaml`.

1. **Update Collection Dependencies and Versions**

   Update all collection dependencies and version numbers in `requirements.yml`
   and role defaults as needed.

## Changelog Management

The collection uses [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog)
to manage the changelog.

### Creating Changelog Fragments

Add details of changes to the changelog in `changelogs/fragments/` directory.
Create YAML files with appropriate categories:

```yaml
# changelogs/fragments/x.y.z.yaml
---
added:
  - "Description of new feature"
changed:
  - "Description of changes to existing functionality"
removed:
  - "Description of features that were removed"
bugfixes:
  - "Description of bug fixes"
release_summary: "Brief summary of the release"
```

**Important formatting rules:**

- Fragment files should only contain the specific changes for the new version
- Do NOT include the `ancestor` or `releases` sections in fragment files
- Do NOT include a `release_date` field - this is added automatically
- Use YAML list format with hyphens (`-`) for each list item, not indented lists
- Fragment files are automatically deleted after being processed - this is by design

### Managing the Changelog

You can work with the changelog in two ways:

#### Option 1: Run the complete changelog process in one command

```bash
export TASK_X_REMOTE_TASKFILES=1
NEXT_VERSION=x.y.z task -y ansible:gen-changelog
```

This command will run all the necessary steps (linting and release generation).

#### Option 2: Run individual changelog tasks separately

Lint the changelog first:

```bash
export TASK_X_REMOTE_TASKFILES=1
task -y ansible:changelog-lint
```

Then generate the release:

```bash
export TASK_X_REMOTE_TASKFILES=1
NEXT_VERSION=$NEXT_VERSION task -y ansible:changelog-release
```

**Required Variables:**

- `NEXT_VERSION`: Version number for the release (e.g., 1.0.0)

Example output:

```bash
task: [ansible:gen-changelog] Generating changelog for release 1.0.0
task: [ansible:changelog-lint] antsibull-changelog lint
task: [ansible:changelog-release] antsibull-changelog release --version $NEXT_VERSION
```

## Complete Release Process

Follow these steps to create a new release:

1. Run Tests and Linting

   Ensure all tests pass and code is linted:

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   task -y ansible:run-molecule-tests
   export TASK_X_REMOTE_TASKFILES=1
   task -y ansible:lint-ansible
   ```

1. Update Documentation

   Ensure all documentation is up-to-date, including README files and role documentation.

1. Create a Version Branch

   Create a new branch for the release version:

   ```bash
   git checkout -b $NEXT_VERSION  # e.g., git checkout -b 2.0.4
   ```

1. Generate Changelog

   **Option 1: Complete changelog process in one command**

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   NEXT_VERSION=$NEXT_VERSION task -y ansible:gen-changelog
   ```

   **Option 2: Run individual changelog tasks**

   ```bash
   # First lint the changelog
   export TASK_X_REMOTE_TASKFILES=1
   task -y ansible:changelog-lint

   # Then generate the release (this will also update galaxy.yml)
   export TASK_X_REMOTE_TASKFILES=1
   NEXT_VERSION=$NEXT_VERSION task -y ansible:changelog-release
   ```

   **Note:** When these commands run, antsibull-changelog will process your
   fragment files, incorporate their content into the main changelog, and then
   automatically remove the fragment files from the filesystem. This is normal
   behavior.

1. Create a Release Commit

   ```bash
   git add .
   git commit
   ```

   Use this format for your commit message:

   ```bash
   feat: Improve VNC setup and add awscli as asdf plugin

   **Key Changes:**

   - Enhanced VNC setup with better systemd integration and verification.
   - Added awscli (v2.24.0) as default asdf plugin.
   - Refactored user and VNC roles for better maintainability.
   - Updated Ansible collections and asdf plugin versions.

   **Added:**

   - `awscli` plugin (v2.24.0) to asdf defaults.
   - Verification tests for VNC: config, services, and port checks.
   - Cleanup tasks for VNC sessions to support clean restarts.
   - `vnc_setup_depth` param to control color depth in VNC.
   - UID-aware handling for better VNC session management.

   **Changed:**

   - Improved VNC systemd template: error handling, env vars, restarts.
   - Refactored VNC setup into modular task files.
   - Improved shell detection in user_setup via basename + patterns.
   - Refactored user_setup role for robust shell installation.
   - Bumped Ansible collections:
     - amazon.aws: 9.1.1 → 9.3.0
     - ansible.windows: 2.7.0 → 2.8.0
     - community.docker: 4.3.1 → 4.5.2
     - community.general: 10.3.0 → 10.5.0
   - Bumped asdf plugins:
     - golang: 1.23.5 → 1.24.0
     - python: 3.13.1 → 3.13.2
     - ruby: 3.3.5 → 3.4.2
     - helm: 3.17.0 → 3.17.2
     - kubectl: 1.32.1 → 1.32.3

   **Removed:**

   - RedHat platform from VNC Molecule tests.
   ```

1. Push the Branch

   ```bash
   git push origin $NEXT_VERSION  # e.g., git push origin 2.0.4
   ```

   This will output a URL you can use to create a Pull Request:

   ```bash
   remote: Create a pull request for '$NEXT_VERSION' on GitHub by visiting:
   remote:      https://github.com/CowDogMoo/ansible-collection-workstation/pull/new/$NEXT_VERSION
   ```

1. Create and Merge the Pull Request

   - Click the URL from the previous step to create a PR
   - Wait for all CI tests to pass
   - Review the changes
   - Merge the PR into the main branch

1. Checkout the Main Branch

   ```bash
   git checkout main
   git pull
   ```

1. Create GitHub Release and Tag

   ```bash
   # This creates both a GitHub release and a git tag
   gh release create $NEXT_VERSION --generate-notes
   ```

   This command uses the GitHub CLI to:

   - Create a new release with the specified version
   - Generate release notes automatically based on commits since the last release
   - Create a corresponding git tag

1. Automatic Collection Publishing

   The GitHub Action defined in `.github/workflows/release.yaml` will automatically:

   - Be triggered by the new tag you created
   - Build the Ansible collection
   - Publish it to Ansible Galaxy using the GALAXY_API_KEY secret
     stored in the repository settings

## Release Versioning

We follow semantic versioning (SemVer) for this collection:

- **Major version** (x.0.0): Incompatible API changes
- **Minor version** (0.x.0): Add functionality in a backward-compatible manner
- **Patch version** (0.0.x): Backward-compatible bug fixes

## Troubleshooting

If you encounter issues with the changelog generation:

1. **Validation Errors**: Check the format of your changelog fragment files
1. **Missing antsibull-changelog**: Install with `pip install antsibull-changelog`
1. **Git Issues**: Ensure your git configuration is correct and you have the
   necessary permissions
1. **Log Files**: Check logs in `logs/molecule_tests.log` for testing issues
