# Ansible Role: ZSH Setup

This role installs and configures `zsh` with `oh-my-zsh` for user accounts on
Unix-like systems.

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

| Variable                         | Default Value                                                           | Description              |
| -------------------------------- | ----------------------------------------------------------------------- | ------------------------ |
| zsh_setup_omz_install_script_url | "https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh" | oh-my-zsh install script |
| zsh_setup_theme                  | "af-magic"                                                              | Default theme for zsh    |
| zsh_setup_default_username       | {{ ansible_distribution \| lower }}                                     | Default username         |
| zsh_setup_enriched_users         | Configurable                                                            | Users for zsh setup      |

### Default Configuration for `zsh_setup_enriched_users`

- `username`: Specified user or default `{{ zsh_setup_default_username }}`
- `usergroup`: User's group, default is `{{ zsh_setup_default_username }}`

## Role Tasks

- Gather and enrich user data.
- Ensure necessary packages for `zsh` are installed.
- Ensure user groups and users exist.
- Ensure user home directories exist.
- Check if `.oh-my-zsh` exists for users.
- Download and install oh-my-zsh for users.
- Ensure `.zshrc` exists for each user.

## Testing

To test the role, use Molecule:

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```

## Platforms

This role is tested on the following platforms:

- Ubuntu
- macOS
- Kali Linux

## Dependencies

- `cowdogmoo.workstation.package_management`

## Author Information

This role was created by Jayson Grace and is maintained as part of the
CowDogMoo project.
