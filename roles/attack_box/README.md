<!-- DOCSIBLE START -->
# attack_box

## Description

Creates an attack box for penetration testing and red teaming

## Requirements

- Ansible >= 2.14

## Dependencies


- cowdogmoo.workstation.package_management

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
| `attack_box_user` | str | <code>{{ ansible_facts&#91;'user_id'&#93; }}</code> | No description |

## Tasks

### main.yml


- **Include tasks for package installation** (ansible.builtin.include_tasks) - Conditional
- **Include tasks for wordlists setup** (ansible.builtin.include_tasks) - Conditional
- **Include tasks for SSH key setup** (ansible.builtin.include_tasks)

### packages.yml


- **Ensure no other package management processes are running** (ansible.builtin.shell)
- **Install required packages for attack box** (ansible.builtin.include_role)

### ssh.yml


- **Compute target user and .ssh directory** (ansible.builtin.set_fact)
- **Get primary group name of the current user "{{ attack_box_target_user }}"** (ansible.builtin.command)
- **Ensure .ssh directory exists for "{{ attack_box_target_user }}"** (ansible.builtin.file)
- **Get list of public SSH key files** (ansible.builtin.find)
- **Add optionally provided public SSH key files to authorized_keys "{{ attack_box_target_user }}"** (ansible.builtin.copy) - Conditional

### wordlists.yml


- **Ensure wordlists directory exists** (ansible.builtin.file)
- **Download rockyou wordlist if not present** (ansible.builtin.get_url)

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
