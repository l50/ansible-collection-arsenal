# Ansible Playbook: Atomic Red Team

This playbook sets up Atomic Red Team, a library of simple tests mapped to the
MITRE ATT&CK framework, on Ubuntu and Kali Linux hosts. Atomic Red Team enables
security teams to test their controls and validate detection capabilities.

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
ansible-playbook atomic-red-team.yml -i inventory
```

### Local Machine Setup

For setting up your local machine:

```bash
ansible-playbook atomic-red-team.yml -i inventory --connection=local
```

### With specific hosts

```bash
ansible-playbook atomic-red-team.yml -i inventory --limit "atomic-test-servers"
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
~/security/ansible-collection-arsenal/playbooks/atomic-red-team/atomic-red-team.yml
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

### Custom Roles Path

The Molecule configuration includes a custom roles path for testing:

```bash
export ANSIBLE_ROLES_PATH="../../roles:~/.ansible/roles:/etc/ansible/roles:$HOME/.ansible/roles"
```

---

## Configuration

The playbook performs the following tasks:

1. **User Setup**: Creates and configures the Atomic Red Team user using the
   `cowdogmoo.workstation.user_setup` role
1. **Atomic Red Team Installation**: Installs and configures Atomic Red Team
   using the `l50.ansible_atomic_red_team` role

### Roles Used

- `cowdogmoo.workstation.user_setup` - Creates and configures user accounts
- `l50.ansible_atomic_red_team` - Installs and configures the Atomic Red Team framework

---

## Example Inventory

### Local Setup

```ini
[all]
localhost ansible_connection=local
```

### Remote Atomic Red Team Servers

```ini
[atomic_test_servers]
atomic1 ansible_host=192.168.1.150
atomic2 ansible_host=192.168.1.151

[atomic_test_servers:vars]
ansible_user=ubuntu
ansible_become=true
```

### Multiple Environment Setup

```ini
[dev_atomic]
dev-atomic-01 ansible_host=10.0.1.60
dev-atomic-02 ansible_host=10.0.1.61

[staging_atomic]
staging-atomic ansible_host=10.0.2.60

[prod_atomic]
prod-atomic ansible_host=10.0.3.60

[all:children]
dev_atomic
staging_atomic
prod_atomic

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
- `l50.ansible_atomic_red_team` role

---

## Security Considerations

- Atomic Red Team executes real attack techniques and should only be used in
  isolated, authorized environments
- Never run atomic tests against production systems without explicit authorization
- Implement network segmentation to prevent test traffic from affecting
  production networks
- Monitor and log all atomic test executions for compliance and analysis
- Review and understand each atomic test before execution
- Ensure proper cleanup after test execution to remove any artifacts

---

## Common Use Cases

### Detection Validation

```bash
# Run specific atomic tests
ansible-playbook atomic-red-team.yml -i inventory -e "atomic_test_numbers=['T1003.001', 'T1055']"
```

### Purple Team Exercises

```bash
# Deploy to purple team environment
ansible-playbook atomic-red-team.yml -i inventory --limit "purple_team"
```

### SOC Training

```bash
# Deploy to training environment
ansible-playbook atomic-red-team.yml -i inventory --limit "soc_training"
```

---

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure the ansible user has sudo privileges
1. **Role Not Found**: Run `ansible-galaxy install -r requirements.yml` to
   install dependencies
1. **PowerShell Issues**: On Linux hosts, ensure PowerShell Core is installed
   for certain atomic tests
1. **Path Issues**: Verify the ANSIBLE_ROLES_PATH is correctly set

### Debug Mode

Run with increased verbosity for troubleshooting:

```bash
ansible-playbook atomic-red-team.yml -i inventory -vvv
```

---

## Post-Installation

After installation, you can execute atomic tests using:

```bash
# List available tests
Invoke-AtomicTest All -ShowDetailsBrief

# Execute a specific technique
Invoke-AtomicTest T1003.001

# Execute with cleanup
Invoke-AtomicTest T1003.001 -Cleanup
```
