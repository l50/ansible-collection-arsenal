# Ansible Playbook: Sliver

This playbook sets up a Sliver C2 (Command and Control) server on Ubuntu and
Kali Linux hosts. Sliver is an open-source adversary emulation/red team framework.

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
ansible-playbook sliver.yml -i inventory
```

### Local Machine Setup

For setting up your local machine:

```bash
ansible-playbook sliver.yml -i inventory --connection=local
```

### With specific hosts

```bash
ansible-playbook sliver.yml -i inventory --limit "sliver-servers"
```

### Connect with Ansible using the playbook through SSM and the provided S3 bucket

```bash
ansible-playbook -i playbooks/sliver/sliver_inventory_aws_ec2.yml \
  -e ansible_aws_ssm_bucket_name=$AWS_S3_BUCKET_NAME \
  -e ansible_connection=aws_ssm \
  -e ansible_aws_ssm_region=$AWS_DEFAULT_REGION \
  -e ansible_shell_executable=/bin/bash \
  -e ansible_aws_ssm_s3_addressing_style=virtual \
  -vvvv \
~/security/ansible-collection-arsenal/playbooks/sliver/sliver.yml
```

### AWS EC2 Dynamic Inventory

This playbook includes an AWS EC2 dynamic inventory configuration that
automatically discovers instances tagged with `Name: sliver`:

```bash
# Set your AWS region
export AWS_DEFAULT_REGION=us-west-1

# Run playbook with dynamic inventory
ansible-playbook -i sliver_inventory_aws_ec2.yml sliver.yml
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

The playbook configures the following:

- Creates a dedicated `sliver` user and group
- Installs Golang 1.23.5 via ASDF version manager
- Sets up the Sliver C2 framework using the `l50.arsenal.sliver` role

### Default Variables

```yaml
sliver_username: "sliver"
sliver_usergroup: "sliver"
sliver_shell: "/bin/bash"
```

---

## Example Inventory

### Local Setup

```ini
[all]
localhost ansible_connection=local
```

### Remote Sliver Servers

```ini
[sliver_servers]
sliver1 ansible_host=192.168.1.100
sliver2 ansible_host=192.168.1.101

[sliver_servers:vars]
ansible_user=ubuntu
ansible_become=true
```

### AWS EC2 Instances

The included `sliver_inventory_aws_ec2.yml` automatically discovers EC2
instances tagged with `Name: packer-sliver` in your configured AWS region.

---

## Requirements

This playbook depends on the `l50.arsenal.sliver` role. Ensure you have the
required collections and roles installed:

```bash
ansible-galaxy install -r requirements.yml
```

---

## Security Considerations

- The Sliver C2 framework is a powerful tool for adversary emulation and should
  only be deployed in authorized environments
- Ensure proper network segmentation and access controls are in place
- Regularly update Sliver and its dependencies
- Monitor and log all C2 activities for compliance and security purposes
