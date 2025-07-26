# Ansible Playbook: Workstation

This role sets up an attack box for penetration testing and red teaming on Kali
Linux hosts.

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
ansible-playbook attack_box.yml -i inventory
```

### Local Machine Setup

For setting up your local machine:

```bash
ansible-playbook attack_box.yml -i inventory --connection=local
```

### With specific hosts

```bash
ansible-playbook attack_box.yml -i inventory --limit "dev-workstations"
```

### Connect with Ansible using the playbook through SSM and the provided S3 bucket

````bash
ansible-playbook -i playbooks/attack_box/attack_box_inventory_aws_ec2.yml \
  -e ansible_aws_ssm_bucket_name=$AWS_S3_BUCKET_NAME \
  -e ansible_connection=aws_ssm \
  -e ansible_aws_ssm_region=$AWS_DEFAULT_REGION \
  -e ansible_shell_executable=/bin/zsh \
  -e ansible_aws_ssm_s3_addressing_style=virtual \
  -vvvv \
~/security/ansible-collection-arsenal/playbooks/attack_box/attack_box.yml
```
---

## Testing

This playbook includes Molecule tests. To test the playbook:

```bash
# Run the full test sequence
molecule test

# Or run individual steps
molecule converge    # Deploy the playbook
molecule idempotence # Test idempotency
molecule verify      # Run verification tests
molecule destroy     # Clean up test instances
````

---

## Example Inventory

### Local Setup

```ini
[all]
localhost ansible_connection=local
```

### Remote Workstations

```ini
[dev_workstations]
dev1 ansible_host=192.168.1.50
dev2 ansible_host=192.168.1.51

[dev_workstations:vars]
ansible_user=kali
ansible_become=true
```
