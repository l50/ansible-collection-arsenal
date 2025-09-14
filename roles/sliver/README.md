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
| `sliver_cleanup` | bool | `False` | No description |
| `sliver_install_path` | str | `/opt/sliver` | No description |
| `sliver_setup_systemd` | bool | `False` | No description |
| `sliver_unpack_at_build` | bool | `True` | No description |
| `sliver_username` | str | `sliver` | No description |
| `sliver_usergroup` | str | `sliver` | No description |
| `sliver_shell` | str | `{% if ansible_os_family == 'Darwin' %}/bin/zsh{% else %}/bin/bash{% endif %}` | No description |
| `sliver_asdf_plugins` | list | `[]` | No description |
| `sliver_asdf_plugins.0` | dict | `{}` | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `sliver_packages` | dict | `{}` | No description |
| `sliver_packages.essential` | list | `[]` | No description |
| `sliver_packages.essential.0` | str | `acl` | No description |
| `sliver_packages.essential.1` | str | `git` | No description |
| `sliver_packages.essential.2` | str | `gnupg` | No description |
| `sliver_packages.essential.3` | str | `unzip` | No description |
| `sliver_packages.essential.4` | str | `zip` | No description |
| `sliver_packages.build_only` | list | `[]` | No description |
| `sliver_packages.build_only.0` | str | `make` | No description |
| `sliver_packages.build_only.1` | str | `wget` | No description |
| `sliver_packages.build_only.2` | str | `curl` | No description |
| `sliver_packages.build_only.3` | str | `autoconf` | No description |
| `sliver_packages.build_only.4` | str | `automake` | No description |
| `sliver_packages.build_only.5` | str | `build-essential` | No description |
| `sliver_packages.build_only.6` | str | `gcc` | No description |
| `sliver_packages.build_only.7` | str | `g++` | No description |
| `sliver_packages.build_only.8` | str | `libtool` | No description |
| `sliver_packages.build_only.9` | str | `python3-pip` | No description |
| `sliver_packages.build_only.10` | str | `ansible` | No description |
| `sliver_packages.build_only.11` | str | `libssl-dev` | No description |
| `sliver_packages.build_only.12` | str | `zlib1g-dev` | No description |
| `sliver_packages.build_only.13` | str | `libncurses5-dev` | No description |
| `sliver_packages.build_only.14` | str | `libncursesw5-dev` | No description |
| `sliver_packages.build_only.15` | str | `libreadline-dev` | No description |
| `sliver_packages.build_only.16` | str | `libsqlite3-dev` | No description |
| `sliver_packages.build_only.17` | str | `libgdbm-dev` | No description |
| `sliver_packages.build_only.18` | str | `libdb5.3-dev` | No description |
| `sliver_packages.build_only.19` | str | `libbz2-dev` | No description |
| `sliver_packages.build_only.20` | str | `libexpat1-dev` | No description |
| `sliver_packages.build_only.21` | str | `liblzma-dev` | No description |
| `sliver_packages.build_only.22` | str | `libffi-dev` | No description |
| `sliver_packages.runtime_debian` | list | `[]` | No description |
| `sliver_packages.runtime_debian.0` | str | `apt-utils` | No description |
| `sliver_packages.runtime_debian.1` | str | `gpg` | No description |
| `sliver_packages.runtime_debian.2` | str | `openssl` | No description |
| `sliver_packages.runtime_debian.3` | str | `libapr1` | No description |
| `sliver_packages.runtime_debian.4` | str | `libsvn1` | No description |
| `sliver_packages.runtime_debian.5` | str | `libxml2` | No description |
| `sliver_packages.runtime_debian.6` | str | `zlib1g` | No description |
| `sliver_packages.runtime_debian.7` | str | `xsel` | No description |
| `sliver_packages.runtime_debian.8` | str | `libcurl4-openssl-dev` | No description |
| `sliver_packages.runtime_debian.9` | str | `libgmp3-dev` | No description |
| `sliver_packages.runtime_debian.10` | str | `libpcap-dev` | No description |
| `sliver_packages.runtime_debian.11` | str | `libpq-dev` | No description |
| `sliver_packages.runtime_debian.12` | str | `libxml2-dev` | No description |
| `sliver_packages.runtime_debian.13` | str | `libxslt-dev` | No description |
| `sliver_packages.runtime_debian.14` | str | `libyaml-dev` | No description |
| `sliver_packages.runtime_debian.15` | str | `ncurses-dev` | No description |
| `sliver_packages.runtime_debian.16` | str | `postgresql` | No description |
| `sliver_packages.runtime_debian.17` | str | `postgresql-contrib` | No description |
| `sliver_packages.runtime_debian.18` | str | `postgresql-client` | No description |
| `sliver_packages.cross_compile` | list | `[]` | No description |
| `sliver_packages.cross_compile.0` | str | `binutils-mingw-w64` | No description |
| `sliver_packages.cross_compile.1` | str | `g++-mingw-w64` | No description |
| `sliver_packages.cross_compile.2` | str | `mingw-w64` | No description |
| `sliver_packages.cross_compile.3` | str | `bison` | No description |
| `sliver_packages.cross_compile.4` | str | `nasm` | No description |
| `sliver_packages.cross_compile.5` | str | `locate` | No description |
| `sliver_packages.cross_compile.6` | str | `patch` | No description |
| `sliver_common_install_packages` | str | `{{ sliver_packages.essential + ['make', 'wget', 'curl'] }}` | No description |
| `sliver_debian_packages` | str | `{{ sliver_packages.build_only + sliver_packages.runtime_debian + sliver_packages.cross_compile }}` | No description |
| `sliver_el_packages` | list | `[]` | No description |
| `sliver_el_packages.0` | str | `epel-release` | No description |
| `sliver_el_packages.1` | str | `gcc` | No description |
| `sliver_el_packages.2` | str | `gcc-c++` | No description |
| `sliver_el_packages.3` | str | `protobuf` | No description |
| `sliver_el_packages.4` | str | `zlib` | No description |
| `sliver_el_packages.5` | str | `zlib-devel` | No description |
| `sliver_cleanup_packages_debian` | str | `{{ sliver_packages.build_only + sliver_packages.cross_compile }}` | No description |
| `sliver_cleanup_paths` | list | `[]` | No description |
| `sliver_cleanup_paths.0` | str | `{{ sliver_user_home }}/go` | No description |
| `sliver_cleanup_paths.1` | str | `{{ sliver_user_home }}/.cache` | No description |
| `sliver_cleanup_paths.2` | str | `{{ sliver_user_home }}/.asdf` | No description |
| `sliver_cleanup_paths.3` | str | `{{ sliver_user_home }}/.local` | No description |
| `sliver_cleanup_paths.4` | str | `{{ sliver_user_home }}/.config` | No description |
| `sliver_cleanup_paths.5` | str | `{{ sliver_user_home }}/.tool-versions` | No description |
| `sliver_cleanup_paths.6` | str | `/root/go` | No description |
| `sliver_cleanup_paths.7` | str | `/root/.cache` | No description |
| `sliver_cleanup_paths.8` | str | `/root/.asdf` | No description |
| `sliver_cleanup_paths.9` | str | `/root/.local` | No description |
| `sliver_cleanup_paths.10` | str | `/root/.tool-versions` | No description |
| `sliver_cleanup_paths.11` | str | `/root/.ssh` | No description |
| `sliver_mingw_directories` | list | `[]` | No description |
| `sliver_mingw_directories.0` | str | `/usr/x86_64-w64-mingw32` | No description |
| `sliver_mingw_directories.1` | str | `/usr/i686-w64-mingw32` | No description |
| `sliver_mingw_directories.2` | str | `/usr/x86_64-w64-mingw32ucrt` | No description |
| `sliver_source_directories` | list | `[]` | No description |
| `sliver_source_directories.0` | str | `client` | No description |
| `sliver_source_directories.1` | str | `server` | No description |
| `sliver_source_directories.2` | str | `implant` | No description |
| `sliver_source_directories.3` | str | `protobuf` | No description |
| `sliver_source_directories.4` | str | `util` | No description |
| `sliver_source_directories.5` | str | `vendor` | No description |
| `sliver_source_directories.6` | str | `test` | No description |
| `sliver_source_directories.7` | str | `docs` | No description |
| `sliver_source_directories.8` | str | `.github` | No description |
| `sliver_source_directories.9` | str | `.git` | No description |
| `sliver_keep_binaries` | list | `[]` | No description |
| `sliver_keep_binaries.0` | str | `sliver-server` | No description |
| `sliver_keep_binaries.1` | str | `sliver-client` | No description |
| `sliver_container_remove_packages` | list | `[]` | No description |
| `sliver_container_remove_packages.0` | str | `*vulkan*` | No description |
| `sliver_container_remove_packages.1` | str | `*llvm*` | No description |
| `sliver_container_remove_packages.2` | str | `libicu*` | No description |
| `sliver_container_remove_packages.3` | str | `snapd` | No description |
| `sliver_container_remove_packages.4` | str | `libgallium*` | No description |
| `sliver_container_remove_packages.5` | str | `libasan*` | No description |

## Tasks

### cleanup.yml

- **Clean up build environment** (block) - Conditional
- **Hold git package to prevent removal during cleanup** (ansible.builtin.dpkg_selections) - Conditional
- **Remove build-time Go installation and caches** (ansible.builtin.file)
- **Find non-binary files in sliver directory** (ansible.builtin.find)
- **Remove non-binary files from sliver directory** (ansible.builtin.file)
- **Remove source directories from sliver installation** (ansible.builtin.file)
- **Find empty directories in sliver path** (ansible.builtin.find)
- **Remove empty directories** (ansible.builtin.file) - Conditional
- **Strip debug symbols from binaries** (ansible.builtin.command)
- **Check for unpacked Go compiler** (ansible.builtin.stat)
- **Remove unpacked Go compiler if found** (ansible.builtin.file) - Conditional
- **Check for unpacked Zig compiler** (ansible.builtin.stat)
- **Remove unpacked Zig compiler if found** (ansible.builtin.file) - Conditional
- **Gather package facts** (ansible.builtin.package_facts) - Conditional
- **Identify MinGW packages to remove** (ansible.builtin.set_fact) - Conditional
- **Remove MinGW packages** (ansible.builtin.apt) - Conditional
- **Remove MinGW directories** (ansible.builtin.file)
- **Remove unnecessary system libraries for containers** (ansible.builtin.apt) - Conditional
- **Remove development packages** (ansible.builtin.apt) - Conditional
- **Find Python cache directories** (ansible.builtin.find)
- **Remove Python cache directories** (ansible.builtin.file)
- **Find Python compiled files** (ansible.builtin.find)
- **Remove Python compiled files** (ansible.builtin.file)
- **Remove pip cache** (ansible.builtin.file)
- **Find log files** (ansible.builtin.find)
- **Truncate sliver log files** (ansible.builtin.copy)
- **Clean sliver user cache directories** (ansible.builtin.file)
- **Clean root home directories** (ansible.builtin.file)
- **Final cleanup - remove unnecessary items for container image builds** (ansible.builtin.shell) - Conditional
- **Unhold git package after cleanup is complete** (ansible.builtin.dpkg_selections) - Conditional

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
- **Include cleanup tasks** (ansible.builtin.include_tasks) - Conditional

### setup.yml

- **Configure Git to allow sliver_install_path as a safe directory** (community.general.git_config)
- **Clone Sliver repo** (ansible.builtin.git)
- **Check current ownership of {{ sliver_install_path }}** (ansible.builtin.stat)
- **Ensure correct ownership of the Sliver repository** (ansible.builtin.file) - Conditional
- **Set up Go version in Sliver directory** (ansible.builtin.copy) - Conditional
- **Add Sliver paths to user's bashrc** (ansible.builtin.blockinfile)
- **Check if Sliver server exists** (ansible.builtin.stat)
- **Ensure golang is installed for user** (ansible.builtin.shell) - Conditional
- **Compile sliver** (ansible.builtin.shell) - Conditional
- **Check if Sliver server unpacked** (ansible.builtin.stat)
- **Check if Sliver server binary exists before unpacking** (ansible.builtin.stat)
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
