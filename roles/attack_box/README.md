# Ansible Role: Attack Box

This role sets up an attack box for penetration testing and red teaming on Kali
Linux hosts.

---

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

Path to the wordlists directory.

```yaml
wordlists_path: /usr/share/wordlists
```

User to configure for the attack box (defaults to the current user).

```yaml
attack_box_user: "{{ ansible_user_id }}"
```

Packages to install for the attack box.

```yaml
attack_box_packages:
  - gzip
  - kali-linux-default
  - vim
  - wordlists
  - zsh
```

---

## Example Playbooks

### Install the attack box on a Kali Linux host

```yaml
- hosts: all
  become: true
  vars:
    attack_box_user: kali
  roles:
    - role: l50.attack_box
```

### Install and configure the attack box with custom user and packages

```yaml
- hosts: all
  become: true
  vars:
    attack_box_user: custom_user
    attack_box_packages:
      - git
      - curl
      - nmap
  roles:
    - role: l50.attack_box
```

### Connect with Ansible using the playbook through SSM and the provided S3 bucket

```sh
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

To test changes made to this role, run the following commands:

```bash
# If on an Apple Silicon machine:
if [[ "$(uname -a | awk '{ print $NF }')" == "arm64" ]]; then
  export DOCKER_DEFAULT_PLATFORM=linux/arm64
fi
molecule create
molecule converge
molecule idempotence
# If everything passed, tear down the docker container spawned by molecule:
molecule destroy
```
