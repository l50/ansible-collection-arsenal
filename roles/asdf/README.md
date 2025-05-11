# Ansible Role: asdf

This role installs and configures the `asdf` version manager for multiple
programming languages on Unix-like systems.

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

## Role Variables

| Variable              | Default Value                                                                                | Description                                         |
| --------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| asdf_git_repo         | "https://github.com/asdf-vm/asdf.git"                                                        | Git repository of ASDF.                             |
| asdf_os_family        | "{{ ansible_os_family \| lower }}"                                                           | Operating system family.                            |
| asdf_default_username | "{{ ansible_env.USER if ansible_os_family == 'Darwin' else ansible_distribution \| lower }}" | Default username based on OS.                       |
| asdf_default_group    | "{{ 'staff' if ansible_os_family == 'Darwin' else ansible_distribution \| lower }}"          | Default group based on OS.                          |
| asdf_users            | See below                                                                                    | List of users to set up with ASDF and their plugins |

### Default Configuration for `asdf_users`

- `username`: The username for ASDF setup.
- `usergroup`: The group of the user.
- `shell`: The shell used by the user.
- `plugins`: List of ASDF plugins to install.

Example `asdf_users` configuration:

```yaml
- username: "{{ asdf_default_username }}"
  usergroup: "{{ asdf_default_group }}"
  shell: "/usr/bin/zsh"
  plugins:
    - name: golang
      version: "1.22"
      scope: "global"
    # ... other plugins ...
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

- Check and install libyaml.
- Update shell profiles for users.
- Deploy `.tool-versions` file.
- Set permissions for ASDF directories.
- Gather installed ASDF plugins and versions.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- macOS
- Kali

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
