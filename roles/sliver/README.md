<!-- DOCSIBLE START -->
# sliver

## Description

Install sliver c2

## Requirements

- Ansible >= 2.14

## Dependencies

- cowdogmoo.workstation.package_management
- cowdogmoo.workstation.asdf

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `sliver_install_path` | str | `/opt/sliver` | No description |
| `sliver_setup_systemd` | bool | `False` | No description |
| `sliver_username` | str | `sliver` | No description |
| `sliver_usergroup` | str | `sliver` | No description |
| `sliver_shell` | str | `{% if ansible_os_family == 'Darwin' %}/bin/zsh{% else %}/bin/bash{% endif %}` | No description |
| `sliver_asdf_plugins` | list | `[]` | No description |
| `sliver_asdf_plugins.0` | dict | `{}` | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `sliver_common_install_packages` | list | `[]` | No description |
| `sliver_common_install_packages.0` | str | `acl` | No description |
| `sliver_common_install_packages.1` | str | `git` | No description |
| `sliver_common_install_packages.2` | str | `gnupg` | No description |
| `sliver_common_install_packages.3` | str | `make` | No description |
| `sliver_common_install_packages.4` | str | `wget` | No description |
| `sliver_common_install_packages.5` | str | `unzip` | No description |
| `sliver_common_install_packages.6` | str | `zip` | No description |
| `sliver_debian_packages` | list | `[]` | No description |
| `sliver_debian_packages.0` | str | `apt-utils` | No description |
| `sliver_debian_packages.1` | str | `autoconf` | No description |
| `sliver_debian_packages.2` | str | `build-essential` | No description |
| `sliver_debian_packages.3` | str | `binutils-mingw-w64` | No description |
| `sliver_debian_packages.4` | str | `bison` | No description |
| `sliver_debian_packages.5` | str | `curl` | No description |
| `sliver_debian_packages.6` | str | `g++-mingw-w64` | No description |
| `sliver_debian_packages.7` | str | `gpg` | No description |
| `sliver_debian_packages.8` | str | `libapr1` | No description |
| `sliver_debian_packages.9` | str | `libcurl4-openssl-dev` | No description |
| `sliver_debian_packages.10` | str | `libgmp3-dev` | No description |
| `sliver_debian_packages.11` | str | `libpcap-dev` | No description |
| `sliver_debian_packages.12` | str | `libpq-dev` | No description |
| `sliver_debian_packages.13` | str | `libsqlite3-dev` | No description |
| `sliver_debian_packages.14` | str | `libsvn1` | No description |
| `sliver_debian_packages.15` | str | `libssl-dev` | No description |
| `sliver_debian_packages.16` | str | `libtool` | No description |
| `sliver_debian_packages.17` | str | `libxml2` | No description |
| `sliver_debian_packages.18` | str | `libxml2-dev` | No description |
| `sliver_debian_packages.19` | str | `libxslt-dev` | No description |
| `sliver_debian_packages.20` | str | `libyaml-dev` | No description |
| `sliver_debian_packages.21` | str | `locate` | No description |
| `sliver_debian_packages.22` | str | `make` | No description |
| `sliver_debian_packages.23` | str | `mingw-w64` | No description |
| `sliver_debian_packages.24` | str | `nasm` | No description |
| `sliver_debian_packages.25` | str | `ncurses-dev` | No description |
| `sliver_debian_packages.26` | str | `openssl` | No description |
| `sliver_debian_packages.27` | str | `postgresql` | No description |
| `sliver_debian_packages.28` | str | `postgresql-contrib` | No description |
| `sliver_debian_packages.29` | str | `postgresql-client` | No description |
| `sliver_debian_packages.30` | str | `xsel` | No description |
| `sliver_debian_packages.31` | str | `zlib1g` | No description |
| `sliver_debian_packages.32` | str | `zlib1g-dev` | No description |
| `sliver_el_packages` | list | `[]` | No description |
| `sliver_el_packages.0` | str | `epel-release` | No description |
| `sliver_el_packages.1` | str | `gcc` | No description |
| `sliver_el_packages.2` | str | `gcc-c++` | No description |
| `sliver_el_packages.3` | str | `protobuf` | No description |
| `sliver_el_packages.4` | str | `zlib` | No description |
| `sliver_el_packages.5` | str | `zlib-devel` | No description |

## Tasks

### main.yml

- **Install required packages for Sliver** (ansible.builtin.include_role)
- **Create user** (ansible.builtin.include_role)
- **Set sliver user home directory** (ansible.builtin.include_tasks)
- **Ensure home directory exists for sliver user** (ansible.builtin.file)
- **Check if .bashrc exists for sliver user** (ansible.builtin.stat)
- **Ensure .bashrc exists for sliver user** (ansible.builtin.file) - Conditional
- **Check if ASDF is installed for sliver user** (ansible.builtin.stat)
- **Check if asdf binary is installed** (ansible.builtin.stat)
- **Print sliver user info** (ansible.builtin.debug)
- **Install asdf and golang for sliver user** (ansible.builtin.include_role) - Conditional
- **Include Sliver setup tasks** (ansible.builtin.include_tasks)
- **Include systemd tasks** (ansible.builtin.include_tasks) - Conditional

### setup.yml

- **Configure Git to allow sliver_install_path as a safe directory** (community.general.git_config)
- **Clone Sliver repo** (ansible.builtin.git)
- **Check current ownership of {{ sliver_install_path }}** (ansible.builtin.stat)
- **Ensure correct ownership of the Sliver repository** (ansible.builtin.file) - Conditional
- **Set up Go version in Sliver directory** (ansible.builtin.copy) - Conditional
- **Add sliver_install_path to $PATH** (ansible.builtin.lineinfile)
- **Check if Sliver server exists** (ansible.builtin.stat)
- **Ensure golang is installed for user** (ansible.builtin.shell) - Conditional
- **Compile sliver** (ansible.builtin.shell) - Conditional
- **Check if Sliver server unpacked** (ansible.builtin.stat)
- **Unpack Sliver server** (ansible.builtin.command) - Conditional
- **Ensure .sliver-client/configs directory exists** (ansible.builtin.file)
- **Generate operator config** (ansible.builtin.shell)
- **Set ownership of sliver-client binary** (ansible.builtin.file)

### sliver_get_user_home.yml

- **Gather available local users** (ansible.builtin.getent) - Conditional
- **Set user home directory** (ansible.builtin.set_fact) - Conditional
- **Set user home directory for macOS** (ansible.builtin.set_fact) - Conditional

### systemd.yml

- **Configure systemd service for Sliver** (ansible.builtin.copy)
- **Start Sliver service** (ansible.builtin.systemd)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - sliver
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
