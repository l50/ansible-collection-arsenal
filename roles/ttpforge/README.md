<!-- DOCSIBLE START -->
# ttpforge

## Description

TTPForge is a Cybersecurity Framework for developing, automating, and executing
attacker Tactics, Techniques, and Procedures (TTPs)


## Requirements

- Ansible >= 2.14

## Dependencies

- cowdogmoo.workstation.package_management
- cowdogmoo.workstation.asdf

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ttpforge_install_path` | str | `/opt/ttpforge` | No description |
| `ttpforge_username` | str | `{% if ansible_os_family == 'Darwin' %}{{ ansible_user_id }}{% else %}{{ ansible_distribution | lower }}{% endif %}` | No description |
| `ttpforge_usergroup` | str | `{% if ansible_os_family == 'Darwin' %}staff{% elif ansible_os_family == 'Debian' %}{{ ansible_user_id }}{% elif ansible_os_family == 'RedHat' %}{{ ansible_user_id }}{% else %}{{ ansible_distribution | lower }}{% endif %}` | No description |
| `ttpforge_shell` | str | `{% if ansible_os_family == 'Darwin' %}/bin/zsh{% else %}/bin/bash{% endif %}` | No description |
| `ttpforge_asdf_plugins` | list | `[]` | No description |
| `ttpforge_asdf_plugins.0` | dict | `{}` | No description |
| `ttpforge_asdf_plugins.1` | dict | `{}` | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `ttpforge_common_install_packages` | list | `[]` | No description |
| `ttpforge_common_install_packages.0` | str | `build-essential` | No description |
| `ttpforge_common_install_packages.1` | str | `g++` | No description |
| `ttpforge_common_install_packages.2` | str | `gcc` | No description |
| `ttpforge_common_install_packages.3` | str | `git` | No description |
| `ttpforge_common_install_packages.4` | str | `make` | No description |
| `ttpforge_common_install_packages.5` | str | `unzip` | No description |
| `ttpforge_common_install_packages.6` | str | `wget` | No description |
| `ttpforge_common_install_packages.7` | str | `zip` | No description |

## Tasks

### main.yml

- **Set ttpforge user home directory** (ansible.builtin.include_tasks)
- **Install required packages for ttpforge** (ansible.builtin.include_role)
- **Ensure home directory exists for ttpforge user** (ansible.builtin.file)
- **Check if .bashrc exists for ttpforge user** (ansible.builtin.stat)
- **Ensure .bashrc exists for ttpforge user** (ansible.builtin.file) - Conditional
- **Check if asdf is installed for ttpforge user** (ansible.builtin.stat)
- **Check if asdf binary is installed** (ansible.builtin.stat)
- **Install asdf and associated plugins for ttpforge user** (ansible.builtin.include_role) - Conditional
- **Include TTPForge setup tasks** (ansible.builtin.include_tasks)

### setup.yml

- **Configure Git to allow ttpforge repository as a safe directory** (community.general.git_config)
- **Clone ttpforge repo** (ansible.builtin.git)
- **Check current ownership of {{ ttpforge_install_path }}** (ansible.builtin.stat)
- **Ensure correct ownership of the ttpforge repository** (ansible.builtin.file) - Conditional
- **Set up Go version in ttpforge directory** (ansible.builtin.copy) - Conditional
- **Add ttpforge_install_path to $PATH** (ansible.builtin.lineinfile)
- **Check if ttpforge binary exists** (ansible.builtin.stat)
- **Ensure golang is installed for user** (ansible.builtin.shell) - Conditional
- **Compile ttpforge** (ansible.builtin.shell) - Conditional
- **Check if ttpforge has been initialized** (ansible.builtin.stat)
- **Initialize ttpforge** (ansible.builtin.command) - Conditional

### ttpforge_get_user_home.yml

- **Gather available local users** (ansible.builtin.getent) - Conditional
- **Set user home directory** (ansible.builtin.set_fact) - Conditional
- **Set user home directory for macOS** (ansible.builtin.set_fact) - Conditional

## Example Playbook

```yaml
- hosts: servers
  roles:
    - ttpforge
```

## Author Information

- **Author**: Jayson Grace
- **Company**: techvomit
- **License**: MIT

## Platforms

- Ubuntu: all
- macOS: all
- EL: all
<!-- DOCSIBLE END -->
