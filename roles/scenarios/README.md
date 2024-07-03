# Ansible Role: Scenarios

This role provides scenarios for testing and training cybersecurity tools and techniques.

## Requirements

- Ansible 2.14 or higher.
- Access to package repositories for required software packages.

## Role Variables

| Variable                | Default Value      | Description                        |
| ----------------------- | ------------------ | ---------------------------------- |
| `paige_turner_password` | Randomly generated | Password for the PaigeTurner user. |
| `frank_furter_password` | "Password123!"     | Password for the FrankFurter user. |

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Apply attack box configurations
  hosts: windows
  roles:
    - role: scenarios
      tasks_from: windows/vuln-cifs/vuln-cifs-user.yaml
    - role: scenarios
      tasks_from: windows/vuln-cifs/secure-cifs-user.yaml
```

## License

MIT

## Author Information

This role was created by [Jayson Grace](https://github.com/l50).
