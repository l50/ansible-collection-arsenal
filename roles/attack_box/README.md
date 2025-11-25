<!-- DOCSIBLE START -->
# attack_box

## Description

Creates an attack box for penetration testing and red teaming

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `attack_box_common_install_packages` | list | <code>&#91;&#93;</code> | No description |
| `attack_box_common_install_packages.0` | str | <code>gzip</code> | No description |
| `attack_box_common_install_packages.1` | str | <code>kali-linux-core</code> | No description |
| `attack_box_common_install_packages.2` | str | <code>vim</code> | No description |
| `attack_box_common_install_packages.3` | str | <code>wordlists</code> | No description |
| `attack_box_common_install_packages.4` | str | <code>zsh</code> | No description |
| `attack_box_user` | str | <code>{{ ansible_user_id }}</code> | No description |

## Tasks

### main.yml


- **Include tasks for package installation** (ansible.builtin.include_tasks) - Conditional
- **Include tasks for wordlists setup** (ansible.builtin.include_tasks) - Conditional
- **Include tasks for SSH key setup** (ansible.builtin.include_tasks)

### packages.yml


- **Ensure no other package management processes are running** (ansible.builtin.shell)
- **Install required packages for attack box** (ansible.builtin.include_role)

### ssh.yml


- **Get primary group name of the current user "{{ attack_box_user ¦ default(ansible_user_id) }}"** (ansible.builtin.command)
- **Ensure .ssh directory exists for "{{ attack_box_user ¦ default(ansible_user_id) }}"** (ansible.builtin.file)
- **Get list of public SSH key files** (ansible.builtin.find)
- **Add optionally provided public SSH key files to authorized_keys "{{ attack_box_user ¦ default(ansible_user_id) }}"** (ansible.builtin.copy) - Conditional

### wordlists.yml


- **Ensure wordlists directory exists** (ansible.builtin.file)
- **Download rockyou wordlist if not present** (ansible.builtin.get_url)
- **Extract wordlists** (ansible.builtin.command)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - attack_box
```

## Author Information

- **Author**: Jayson Grace
- **Company**: techvomit
- **License**: MIT

## Platforms


- Kali: all
<!-- DOCSIBLE END -->
