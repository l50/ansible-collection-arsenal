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
| -------- | ---- | ------- | ----------- |
| `ttpforge_cleanup` | bool | <code>False</code> | No description |
| `ttpforge_install_path` | str | <code>/opt/ttpforge</code> | No description |
| `ttpforge_username` | str | <code>{% if ansible_os_family == 'Darwin' %}{{ ansible_user_id }}{% else %}{{ ansible_distribution &#124; lower }}{% endif %}</code> | No description |
| `ttpforge_usergroup` | str | <code>{% if ansible_os_family == 'Darwin' %}staff{% elif ansible_os_family == 'Debian' %}{{ ansible_user_id }}{% elif ansible_os_family == 'RedHat' %}{{ ansible_user_id }}{% else %}{{ ansible_distribution &#124; lower }}{% endif %}</code> | No description |
| `ttpforge_shell` | str | <code>{% if ansible_os_family == 'Darwin' %}/bin/zsh{% else %}/bin/bash{% endif %}</code> | No description |
| `ttpforge_asdf_plugins` | list | <code>&#91;&#93;</code> | No description |
| `ttpforge_asdf_plugins.0` | dict | <code>{}</code> | No description |
| `ttpforge_asdf_plugins.1` | dict | <code>{}</code> | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
| -------- | ---- | ----- | ----------- |
| `ttpforge_packages` | dict | `{}` | No description |
| `ttpforge_packages.essential` | list | `[]` | No description |
| `ttpforge_packages.essential.0` | str | `git` | No description |
| `ttpforge_packages.essential.1` | str | `unzip` | No description |
| `ttpforge_packages.essential.2` | str | `wget` | No description |
| `ttpforge_packages.essential.3` | str | `zip` | No description |
| `ttpforge_packages.build_only` | list | `[]` | No description |
| `ttpforge_packages.build_only.0` | str | `build-essential` | No description |
| `ttpforge_packages.build_only.1` | str | `g++` | No description |
| `ttpforge_packages.build_only.2` | str | `gcc` | No description |
| `ttpforge_packages.build_only.3` | str | `make` | No description |
| `ttpforge_packages.runtime_debian` | list | `[]` | No description |
| `ttpforge_common_install_packages` | str | `{{ ttpforge_packages.essential + ttpforge_packages.build_only }}` | No description |
| `ttpforge_cleanup_packages_debian` | str | `{{ ttpforge_packages.build_only }}` | No description |
| `ttpforge_cleanup_paths` | list | `[]` | No description |
| `ttpforge_cleanup_paths.0` | str | `{{ ttpforge_user_home }}/go` | No description |
| `ttpforge_cleanup_paths.1` | str | `{{ ttpforge_user_home }}/.cache` | No description |
| `ttpforge_cleanup_paths.2` | str | `{{ ttpforge_user_home }}/.asdf` | No description |
| `ttpforge_cleanup_paths.3` | str | `{{ ttpforge_user_home }}/.local` | No description |
| `ttpforge_cleanup_paths.4` | str | `{{ ttpforge_user_home }}/.config` | No description |
| `ttpforge_cleanup_paths.5` | str | `{{ ttpforge_user_home }}/.tool-versions` | No description |
| `ttpforge_cleanup_paths.6` | str | `/root/go` | No description |
| `ttpforge_cleanup_paths.7` | str | `/root/.cache` | No description |
| `ttpforge_cleanup_paths.8` | str | `/root/.asdf` | No description |
| `ttpforge_cleanup_paths.9` | str | `/root/.local` | No description |
| `ttpforge_cleanup_paths.10` | str | `/root/.tool-versions` | No description |
| `ttpforge_cleanup_paths.11` | str | `/root/.ssh` | No description |
| `ttpforge_cleanup_paths.12` | str | `/tmp/*` | No description |
| `ttpforge_cleanup_paths.13` | str | `/var/tmp/*` | No description |
| `ttpforge_source_directories` | list | `[]` | No description |
| `ttpforge_source_directories.0` | str | `.git` | No description |
| `ttpforge_source_directories.1` | str | `.github` | No description |
| `ttpforge_source_directories.2` | str | `cmd` | No description |
| `ttpforge_source_directories.3` | str | `pkg` | No description |
| `ttpforge_source_directories.4` | str | `examples` | No description |
| `ttpforge_source_directories.5` | str | `docs` | No description |
| `ttpforge_source_directories.6` | str | `test` | No description |
| `ttpforge_source_directories.7` | str | `tests` | No description |
| `ttpforge_keep_binaries` | list | `[]` | No description |
| `ttpforge_keep_binaries.0` | str | `ttpforge` | No description |
| `ttpforge_container_remove_packages` | list | `[]` | No description |
| `ttpforge_container_remove_packages.0` | str | `*vulkan*` | No description |
| `ttpforge_container_remove_packages.1` | str | `*llvm*` | No description |
| `ttpforge_container_remove_packages.2` | str | `libicu*` | No description |
| `ttpforge_container_remove_packages.3` | str | `snapd` | No description |
| `ttpforge_container_remove_packages.4` | str | `libgallium*` | No description |

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
- **Add TTPForge paths to user's bashrc** (ansible.builtin.blockinfile) - Conditional
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
