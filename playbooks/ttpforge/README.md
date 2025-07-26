# Ansible Playbook: TTPForge

This playbook sets up TTPForge, a Tactics, Techniques, and Procedures (TTP)
execution framework, on Ubuntu and Kali Linux hosts. TTPForge is designed for
security testing, adversary emulation, and purple team exercises.

---

## Base Requirements

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

## Usage

### Basic Playbook Execution

```bash
ansible-playbook ttpforge.yml -i inventory
```

### Local Machine Setup

For setting up your local machine:

```bash
ansible-playbook ttpforge.yml -i inventory --connection=local
```

### With specific hosts

```bash
ansible-playbook ttpforge.yml -i inventory --limit "ttpforge-servers"
```

### Connect with Ansible using the playbook through SSM and the provided S3 bucket

```bash
ansible-playbook -i inventory \
  -e ansible_aws_ssm_bucket_name=$AWS_S3_BUCKET_NAME \
  -e ansible_connection=aws_ssm \
  -e ansible_aws_ssm_region=$AWS_DEFAULT_REGION \
  -e ansible_shell_executable=/bin/bash \
  -e ansible_aws_ssm_s3_addressing_style=virtual \
  -vvvv \
~/security/ansible-collection-arsenal/playbooks/ttpforge/ttpforge.yml
```

---

## Testing

This playbook includes Molecule tests for both Ubuntu and Kali Linux. To test
the playbook:

```bash
# Run the full test sequence
molecule test

# Or run individual steps
molecule converge    # Deploy the playbook
molecule idempotence # Test idempotency
molecule verify      # Run verification tests
molecule destroy     # Clean up test instances
```

---

## Configuration

The playbook performs the following tasks:

1. **User Setup**: Configures users on the workstation using the
   `cowdogmoo.workstation.user_setup` role
1. **TTPForge Installation**: Installs and configures TTPForge using the
   `l50.arsenal.ttpforge` role

### Roles Used

- `cowdogmoo.workstation.user_setup` - Sets up user accounts and configurations
- `l50.arsenal.ttpforge` - Installs and configures the TTPForge framework

---

## Example Inventory

### Local Setup

```ini
[all]
localhost ansible_connection=local
```

### Remote TTPForge Servers

```ini
[ttpforge_servers]
ttpforge1 ansible_host=192.168.1.200
ttpforge2 ansible_host=192.168.1.201

[ttpforge_servers:vars]
ansible_user=ubuntu
ansible_become=true
```

### Multiple Environment Setup

```ini
[dev_ttpforge]
dev-ttpforge ansible_host=10.0.1.50

[prod_ttpforge]
prod-ttpforge ansible_host=10.0.2.50

[all:children]
dev_ttpforge
prod_ttpforge

[all:vars]
ansible_user=admin
ansible_become=true
```

---

## Requirements

This playbook depends on external roles. Ensure you have the required
collections and roles installed:

```bash
ansible-galaxy install -r requirements.yml
```

The playbook requires:

- `cowdogmoo.workstation` collection
- `l50.arsenal` collection

---

## Security Considerations

- TTPForge is a powerful framework for executing adversary techniques and
  should only be deployed in authorized environments
- Ensure proper network segmentation between TTPForge instances and production systems
- Implement strict access controls and authentication mechanisms
- Log and monitor all TTP executions for compliance and security purposes
- Regular security updates should be applied to the TTPForge framework and its dependencies

---

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure the ansible user has sudo privileges
1. **Role Not Found**: Run `ansible-galaxy install -r requirements.yml` to
   install dependencies
1. **Connection Issues**: Verify network connectivity and SSH/SSM configurations

### Debug Mode

Run with increased verbosity for troubleshooting:

```bash
ansible-playbook ttpforge.yml -i inventory -vvv
```
