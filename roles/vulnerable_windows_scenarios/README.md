# Ansible Role: Vulnerable Windows Scenarios

This role provides scenarios for testing and training cybersecurity tools and
techniques on Windows EC2 instances.

## Requirements

- Ansible 2.14 or higher.
- Access to package repositories for required software packages.
- AWS credentials configured to access EC2 instances.

## Role Variables

| Variable            | Default Value   | Description                             |
| ------------------- | --------------- | --------------------------------------- |
| `users`             | Defined in vars | List of users to be created             |
| `shares`            | Defined in vars | List of shares to be created            |
| `documents`         | Defined in vars | List of documents to be created         |
| `welcome_documents` | Defined in vars | List of welcome documents to be created |

## Example Playbook

Be sure to replace `your-s3-bucket-name` with the name of an actual S3 bucket
in the playbook.

```yaml
---
- name: Apply attack box configurations
  hosts: "{{ target }}"
  vars_files:
    - ../../vars/main.yml
  vars:
    ansible_connection: aws_ssm
    ansible_aws_ssm_bucket_name: your-s3-bucket-name
    ansible_shell_type: powershell
  roles:
    - role: vulnerable-windows-scenarios
  tasks:
    - name: Fail if no target is provided
      fail:
        msg: "You must provide a target host using --extra-vars"
      when: target is undefined or target == "none"
```

### Running Provided Playbook

1. **Identify the First Instance**:

   ```bash
   first_instance=$(ansible-inventory -i ansible-collection-arsenal/playbooks/vulnerable-windows-scenarios/windows_inventory_aws_ec2.yaml \
     --list | jq -r '._meta.hostvars | keys | sort | .[0]')
   ```

1. **Run the Playbook with the First Instance**:

   ```bash
   INVENTORY_PATH=ansible-collection-arsenal/playbooks/vulnerable_windows_scenarios/windows_inventory_aws_ec2.yaml
   PLAYBOOK_PATH=ansible-collection-arsenal/playbooks/vulnerable_windows_scenarios/windows_scenarios.yml

   ansible-playbook \
     -i $INVENTORY_PATH \
     $PLAYBOOK_PATH \
     --extra-vars "target=${first_instance}"
   ```

## License

MIT

## Author Information

This role was created by [Jayson Grace](https://github.com/l50).
