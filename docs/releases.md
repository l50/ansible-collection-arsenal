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
NEXT_VERSION=x.y.z
export TASK_X_REMOTE_TASKFILES=1
NEXT_VERSION=$NEXT_VERSION task -y ansible:gen-changelog
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

## Automated Release Process (Recommended)

The collection includes automated release tasks that streamline the entire release process.

### Quick Release

For a complete automated release:

```bash
export TASK_X_REMOTE_TASKFILES=1
NEXT_VERSION=x.y.z task -y release
```

This command will:

1. Create a release branch
2. Auto-generate changelog from git commits using fabric
3. Update galaxy.yml version
4. Commit and push changes
5. Create a pull request

After the PR is created:

1. Wait for CI tests to pass in the PR
2. Review and merge the PR
3. Finalize the release:

```bash
export TASK_X_REMOTE_TASKFILES=1
NEXT_VERSION=x.y.z task -y release-finalize
```

This will:

- Create the GitHub release and tag
- Trigger automatic publishing to Ansible Galaxy

### How It Works

**Changelog Generation**: The `gen-changelog-fragment` task uses a fabric pattern to analyze git commits since the last release and automatically generates a properly formatted changelog fragment with the correct sections (`added`, `changed`, `fixed`, `removed`).

**No Manual Fragments Needed**: You don't need to manually create changelog fragments - the automation extracts this from your commit messages.

**Tests Run in CI**: Tests are not run locally during the release task - they run in the PR's CI workflow, keeping the release process fast.

**Tag Creation**: The release tag is only created when you run `release-finalize` after the PR is merged, ensuring the tag points to the merged commit.

## Manual Release Process (Alternative)

If you prefer manual control or need to customize the process, follow these steps:

1. **Update Documentation**

   Ensure all documentation is up-to-date, including README files and role documentation.

1. **Create a Version Branch**

   ```bash
   git checkout -b $NEXT_VERSION  # e.g., git checkout -b 2.0.4
   ```

1. **Generate Changelog Fragment (Optional)**

   If you want to manually create a fragment instead of using automation:

   ```yaml
   # changelogs/fragments/x.y.z.yaml
   ---
   release_summary: "Brief summary"
   added:
     - "New feature description"
   changed:
     - "Change description"
   fixed:
     - "Bug fix description"
   ```

1. **Generate Changelog**

   ```bash
   export TASK_X_REMOTE_TASKFILES=1
   NEXT_VERSION=$NEXT_VERSION task -y ansible:gen-changelog
   ```

1. **Create Release Commit and Push**

   ```bash
   git add .
   git commit -m "chore: Release version $NEXT_VERSION"
   git push origin $NEXT_VERSION
   ```

1. **Create and Merge Pull Request**
   - Create a PR from your branch
   - Wait for CI tests to pass
   - Review and merge

1. **Finalize Release**

   ```bash
   git checkout main
   git pull
   export TASK_X_REMOTE_TASKFILES=1
   NEXT_VERSION=$NEXT_VERSION task -y release-finalize
   ```

1. **Automatic Collection Publishing**

   The GitHub Action defined in `.github/workflows/release.yaml` will automatically:
   - Be triggered by the new tag
   - Build the Ansible collection
   - Publish it to Ansible Galaxy

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
