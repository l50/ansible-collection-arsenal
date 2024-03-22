# Ansible Role: Sliver

[![Pre-Commit](https://github.com/l50/ansible-sliver/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/l50/ansible-sliver/actions/workflows/pre-commit.yaml)
[![Molecule Test](https://github.com/l50/ansible-sliver/actions/workflows/molecule.yaml/badge.svg)](https://github.com/l50/ansible-sliver/actions/workflows/molecule.yaml)
[![Ansible Galaxy](https://img.shields.io/badge/Galaxy-sliver-660198.svg?style=flat)](https://galaxy.ansible.com/l50/sliver)
[![License](https://img.shields.io/github/license/l50/ansible-sliver?label=License&style=flat&color=blue&logo=github)](https://github.com/l50/ansible-sliver/blob/master/LICENSE)

This role installs [Sliver](https://github.com/BishopFox/sliver.git)
on Linux hosts.

---

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

Path to the Sliver install script.

```yaml
sliver_install_path: /tmp/install-sliver.sh
```

Setup Sliver systemd service (default: false).

```yaml
sliver_setup_systemd: true
```

---

## Example Playbooks

Install Sliver and setup systemd service.

```yaml
- hosts: all
  become: true
  vars:
    sliver_setup_systemd: true
  roles:
    - role: l50.sliver
```

Install and configure Sliver with custom file paths.

```yaml
- hosts: all
  become: true
  vars:
    server_path: /root/sliver-server
    client_path: /usr/local/bin/sliver
    sliver_service_path: /etc/systemd/system/sliver.service
    sliver_client_config_path: /root/.sliver-client/configs
  roles:
    - role: l50.sliver
```

---

## Local Development

Make sure to run the following to develop locally:

```bash
PATH_TO_ROLE="${PWD}"
ln -s "${PATH_TO_ROLE}" "${HOME}/.ansible/roles/l50.sliver"
```

---

## Testing

To test changes made to this role, run the following commands:

```bash
# If on an Apple Silicon machine:
if [[ "$(uname -a | awk '{ print $NF }')" == "arm64" ]]; then
  export DOCKER_DEFAULT_PLATFORM=linux/arm64
fi
molecule create
molecule converge
molecule idempotence
# If everything passed, tear down the docker container spawned by molecule:
molecule destroy
```
