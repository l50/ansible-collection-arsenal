# Ansible Role: VNC Setup

This role configures VNC services with systemd integration, ensuring isolated
and secure remote desktop access for each user on Unix-like systems.

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

| Variable                    | Default Value                                                                            | Description                       |
| --------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------- |
| vnc_setup_vncpwd_repo_url   | [https://github.com/jeroennijhof/vncpwd.git](https://github.com/jeroennijhof/vncpwd.git) | URL for cloning vncpwd repo.      |
| vnc_setup_client_options    | "-geometry 1920x1080"                                                                    | VNC client configuration options. |
| vnc_setup_systemd           | true                                                                                     | Enable/disable systemd setup.     |
| vnc_setup_users             | Configurable                                                                             | List of users for VNC setup.      |
| vnc_setup_default_username  | "{{ ansible_distribution \| lower }}"                                                    | Default username.                 |
| vnc_setup_vncpwd_clone_path | "/tmp/vncpwd"                                                                            | Clone path for vncpwd repo.       |
| vnc_setup_vncpwd_path       | "/usr/local/bin/vncpwd"                                                                  | Path for vncpwd executable.       |

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

- Install and configure vncpwd.
- Set up .vnc directories for users.
- Generate random VNC passwords.
- Create user runtime directories.
- Enable lingering and systemd directories.
- Configure VNC service files and permissions.
- Add scripts for starting VNC.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali

## Dependencies

- `cowdogmoo.workstation.user_setup`
- `cowdogmoo.workstation.package_management`
- `cowdogmoo.workstation.zsh_setup`

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
