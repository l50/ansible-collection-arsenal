# Ansible Role: Logging

This role provides logging directories and log rotation for other roles,
ensuring proper logging infrastructure on Unix-like systems.

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

| Variable                    | Default Value | Description                            |
| --------------------------- | ------------- | -------------------------------------- |
| logging_directories         | [See below]   | Directories to be created for logging. |
| logging_log_rotation_config | Configurable  | Configuration for log rotation.        |

### Default Configuration for `logging_directories`

- `path`: The path of the directory to be created for logging, e.g., "/var/log/ansible"

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

- Ensure logging directories exist.
- Setup log rotation.

## Platforms

This role is tested on the following platforms:

- Ubuntu
- Kali

## Dependencies

No dependencies.

## Author Information

This role was created by Jayson Grace and is maintained as part of
the CowDogMoo project.
