# Ansible Role: TTPForge

This role installs and configures [TTPForge](https://github.com/facebookincubator/TTPForge),
a Cybersecurity Framework for developing, automating, and executing attacker
Tactics, Techniques, and Procedures (TTPs).

## Requirements

- Ansible 2.14 or higher.
- Access to package repositories for required software packages.

## Role Variables

| Variable                           | Default Value                       | Description                                           |
| ---------------------------------- | ----------------------------------- | ----------------------------------------------------- |
| `ttpforge_repo_path`               | `"{{ ansible_env.HOME }}/ttpforge"` | Path to clone the TTPForge repository.                |
| `ttpforge_install_path`            | `"/usr/local/bin/ttpforge"`         | Path to install the TTPForge executable.              |
| `ttpforge_go_path`                 | `"/usr/bin/go"`                     | Path to the Go executable for building TTPForge.      |
| `ttpforge_common_install_packages` | See `vars/main.yml`                 | Common packages required for TTPForge.                |
| `ttpforge_debian_packages`         | See `vars/main.yml`                 | Debian-specific packages required for TTPForge.       |
| `ttpforge_el_packages`             | See `vars/main.yml`                 | EL (Enterprise Linux) specific packages for TTPForge. |

## Dependencies

- `cowdogmoo.workstation.package_management`
- `cowdogmoo.workstation.asdf`

## Example Playbook

```yaml
- hosts: servers
  roles:
    - {
        role: cowdogmoo.workstation.ttpforge,
        ttpforge_users:
          [
            {
              username: "ttpforge",
              usergroup: "ttpforge",
              shell: "/bin/bash",
              sudo: true,
              plugins: [{ name: "golang", version: "1.22.0", scope: "global" }],
            },
          ],
      }
```

## Testing

This role uses Molecule for testing. To run the tests:

```bash
molecule converge
molecule verify
molecule destroy
```

## License

MIT

## Author Information

This role was created by [Jayson Grace](https://github.com/l50).
