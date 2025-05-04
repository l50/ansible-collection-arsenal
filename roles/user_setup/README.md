# Ansible Role: User Setup

This role sets up user accounts with optional sudo privileges for Unix-like
systems.

---

## Requirements

- Ansible 2.14 or higher.
- Python packages. Install with:

  ```bash
  python3 -m pip install --upgrade \
    ansible-core \
    molecule \
    molecule-docker \
    "molecule-plugins[docker]"
  ```

---

## Role Variables

| Variable                    | Default Value                | Description                  |
| --------------------------- | ---------------------------- | ---------------------------- |
| user_setup_install_packages | bash, sudo                   | Base packages for users.     |
| user_setup_default_users    | Defined in defaults/main.yml | Default user configurations. |

### Default Configuration for `user_setup_default_users`

- `username`: Default username based on OS distribution.
- `usergroup`: Default group based on OS distribution.
- `sudo`: Whether the user has sudo privileges.
- `shell`: Default shell for the user.

Example `user_setup_default_users` configuration:

```yaml
- username: "{{ ansible_env.USER if ansible_distribution == 'MacOSX' else
  user_setup_default_username }}"
  usergroup: "{{ 'staff' if ansible_distribution == 'MacOSX' else
  user_setup_default_group }}"
  sudo: true
  shell: /bin/zsh
```

---

## Testing

To test the role, use Molecule:

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```

## Role Tasks

Key tasks in this role:

- Gather list of unique shells to install.
- Install base packages for all users.
- Install user-specific shells.
- Ensure groups exist for users.
- Create users with specific attributes.
- Provide sudoers access for relevant users.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali

## Dependencies

No dependencies.

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
