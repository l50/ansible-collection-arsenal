<!-- DOCSIBLE START -->
# coercion_tools

## Description

Install and configure network poisoning and relay attack tools

## Requirements

- Ansible >= 2.14

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `coercion_tools_kali_packages` | list | <code>&#91;&#93;</code> | No description |
| `coercion_tools_kali_packages.0` | str | <code>responder</code> | No description |
| `coercion_tools_kali_packages.1` | str | <code>samba-common-bin</code> | No description |
| `coercion_tools_kali_packages.2` | str | <code>python3-dev</code> | No description |
| `coercion_tools_kali_packages.3` | str | <code>python3-venv</code> | No description |
| `coercion_tools_kali_packages.4` | str | <code>build-essential</code> | No description |
| `coercion_tools_kali_packages.5` | str | <code>git</code> | No description |
| `coercion_tools_ubuntu_packages` | list | <code>&#91;&#93;</code> | No description |
| `coercion_tools_ubuntu_packages.0` | str | <code>git</code> | No description |
| `coercion_tools_ubuntu_packages.1` | str | <code>python3</code> | No description |
| `coercion_tools_ubuntu_packages.2` | str | <code>python3-pip</code> | No description |
| `coercion_tools_ubuntu_packages.3` | str | <code>python3-dev</code> | No description |
| `coercion_tools_ubuntu_packages.4` | str | <code>python3-venv</code> | No description |
| `coercion_tools_ubuntu_packages.5` | str | <code>build-essential</code> | No description |
| `coercion_tools_ubuntu_packages.6` | str | <code>linux-libc-dev</code> | No description |
| `coercion_tools_ubuntu_packages.7` | str | <code>samba-common-bin</code> | No description |
| `coercion_tools_install_responder` | bool | <code>True</code> | No description |
| `coercion_tools_responder_repo` | str | <code>https://github.com/lgandx/Responder.git</code> | No description |
| `coercion_tools_responder_install_dir` | str | <code>/opt/Responder</code> | No description |
| `coercion_tools_responder_version` | str | <code>v3.1.4.0</code> | No description |
| `coercion_tools_install_mitm6` | bool | <code>True</code> | No description |
| `coercion_tools_mitm6_package` | str | <code>mitm6</code> | No description |
| `coercion_tools_mitm6_install_dir` | str | <code>/opt/mitm6</code> | No description |
| `coercion_tools_install_coercer` | bool | <code>True</code> | No description |
| `coercion_tools_coercer_package` | str | <code>coercer</code> | No description |
| `coercion_tools_install_petitpotam` | bool | <code>True</code> | No description |
| `coercion_tools_petitpotam_repo` | str | <code>https://github.com/ly4k/PetitPotam.git</code> | No description |
| `coercion_tools_petitpotam_install_dir` | str | <code>/opt/PetitPotam</code> | No description |
| `coercion_tools_petitpotam_version` | str | <code>main</code> | No description |
| `coercion_tools_install_krbrelayx` | bool | <code>True</code> | No description |
| `coercion_tools_krbrelayx_repo` | str | <code>https://github.com/dirkjanm/krbrelayx.git</code> | No description |
| `coercion_tools_krbrelayx_install_dir` | str | <code>/opt/krbrelayx</code> | No description |
| `coercion_tools_krbrelayx_version` | str | <code>master</code> | No description |
| `coercion_tools_install_ntlmrelayx` | bool | <code>True</code> | No description |
| `coercion_tools_impacket_from_source` | bool | <code>True</code> | No description |
| `coercion_tools_impacket_repo` | str | <code>https://github.com/fortra/impacket.git</code> | No description |
| `coercion_tools_impacket_version` | str | <code>impacket_0_13_0</code> | No description |
| `coercion_tools_impacket_install_dir` | str | <code>/opt/impacket</code> | No description |
| `coercion_tools_install_dfscoerce` | bool | <code>True</code> | No description |
| `coercion_tools_dfscoerce_repo` | str | <code>https://github.com/Wh04m1001/DFSCoerce.git</code> | No description |
| `coercion_tools_dfscoerce_install_dir` | str | <code>/opt/DFSCoerce</code> | No description |
| `coercion_tools_dfscoerce_version` | str | <code>main</code> | No description |
| `coercion_tools_update_cache` | bool | <code>True</code> | No description |
| `coercion_tools_pip_break_system_packages` | bool | <code>False</code> | No description |
| `coercion_tools_binaries` | dict | <code>{}</code> | No description |
| `coercion_tools_binaries.responder` | str | <code>/usr/local/bin/responder</code> | No description |
| `coercion_tools_binaries.mitm6` | str | <code>/usr/local/bin/mitm6</code> | No description |
| `coercion_tools_binaries.coercer` | str | <code>/usr/local/bin/coercer</code> | No description |
| `coercion_tools_binaries.petitpotam` | str | <code>/usr/local/bin/petitpotam</code> | No description |
| `coercion_tools_binaries.krbrelayx` | str | <code>/usr/local/bin/krbrelayx</code> | No description |
| `coercion_tools_binaries.addspn` | str | <code>/usr/local/bin/addspn</code> | No description |
| `coercion_tools_binaries.dnstool` | str | <code>/usr/local/bin/dnstool</code> | No description |
| `coercion_tools_binaries.ntlmrelayx` | str | <code>/usr/local/bin/impacket-ntlmrelayx</code> | No description |
| `coercion_tools_binaries.dfscoerce` | str | <code>/usr/local/bin/dfscoerce</code> | No description |

## Tasks

### impacket_source.yml


- **Install git for cloning impacket** (ansible.builtin.apt) - Conditional
- **Remove conflicting apt impacket packages (Ubuntu only - Kali netexec depends on them)** (ansible.builtin.apt) - Conditional
- **Check if impacket is installed from source** (ansible.builtin.stat)
- **Check if impacket repo already exists** (ansible.builtin.stat)
- **Clone impacket repository from GitHub (initial clone)** (ansible.builtin.git) - Conditional
- **Set impacket venv path** (ansible.builtin.set_fact)
- **Check if impacket venv exists** (ansible.builtin.stat)
- **Check if we need to install or reinstall impacket** (ansible.builtin.set_fact)
- **Create impacket virtual environment** (ansible.builtin.command) - Conditional
- **Install impacket from source** (ansible.builtin.pip) - Conditional
- **Upgrade pycryptodome in impacket venv (CVE fix - GHSA-j225-cvw7-qrx7)** (ansible.builtin.pip) - Conditional
- **Check if impacket is correctly installed in venv** (ansible.builtin.command)
- **Make impacket example scripts executable** (ansible.builtin.shell)
- **Check if \_\_init\_\_.py exists in impacket/examples** (ansible.builtin.stat)
- **Create \_\_init\_\_.py in impacket/examples to make it a proper Python package** (ansible.builtin.copy) - Conditional
- **Check system impacket version (Kali)** (ansible.builtin.command) - Conditional
- **Install source impacket into system Python (Kali apt netexec needs it system-wide)** (ansible.builtin.pip) - Conditional
- **Enumerate impacket example scripts** (ansible.builtin.find)
- **Fail loudly if impacket examples were not found** (ansible.builtin.assert)
- **Install venv-aware bash wrappers for impacket example scripts (no .py suffix)** (ansible.builtin.copy)
- **Install venv-aware bash wrappers for impacket example scripts (.py suffix)** (ansible.builtin.copy)
- **Verify impacket regsecrets module is available** (ansible.builtin.command)
- **Report impacket installation status** (ansible.builtin.debug)

### linux.yml


- **Wait for apt locks to be released** (ansible.builtin.shell) - Conditional
- **Set DEBIAN_FRONTEND to noninteractive** (ansible.builtin.lineinfile) - Conditional
- **Update apt cache** (ansible.builtin.apt) - Conditional
- **Remove conflicting python3-responder package on Kali** (ansible.builtin.apt) - Conditional
- **Install Kali-specific poisoning tools (includes responder from apt)** (ansible.builtin.apt) - Conditional
- **Install Ubuntu-compatible dependencies** (ansible.builtin.apt) - Conditional
- **Check if Coercer is already installed (non-Kali)** (ansible.builtin.command) - Conditional
- **Install Coercer via pip (non-Kali)** (ansible.builtin.pip) - Conditional
- **Install Impacket from source for ntlmrelayx** (ansible.builtin.include_tasks) - Conditional
- **Check for ntlmrelayx.py wrapper** (ansible.builtin.stat) - Conditional
- **Create ntlmrelayx wrapper script** (ansible.builtin.copy) - Conditional
- **Clone Responder from GitHub** (ansible.builtin.git) - Conditional
- **Check if Responder dependencies are installed** (ansible.builtin.command) - Conditional
- **Install Responder dependencies (non-Kali)** (ansible.builtin.pip) - Conditional
- **Make Responder.py executable** (ansible.builtin.file) - Conditional
- **Create symlink for Responder** (ansible.builtin.file) - Conditional
- **Install mitm6 via venv (non-Kali)** (ansible.builtin.include_tasks) - Conditional
- **Install mitm6 via apt (Kali)** (ansible.builtin.apt) - Conditional
- **Install Coercer via apt (Kali)** (ansible.builtin.apt) - Conditional
- **Clone PetitPotam from GitHub (ly4k's improved version)** (ansible.builtin.git) - Conditional
- **Make petitpotam.py executable** (ansible.builtin.file) - Conditional
- **Create symlink for PetitPotam (Kali)** (ansible.builtin.file) - Conditional
- **Stat existing PetitPotam launcher (non-Kali)** (ansible.builtin.stat) - Conditional
- **Remove legacy PetitPotam symlink so the wrapper can replace it** (ansible.builtin.file) - Conditional
- **Install venv-aware bash wrapper for PetitPotam (non-Kali)** (ansible.builtin.copy) - Conditional
- **Clone krbrelayx from GitHub** (ansible.builtin.git) - Conditional
- **Configure git to ignore filemode changes in krbrelayx repo** (ansible.builtin.command) - Conditional
- **Create virtual environment for krbrelayx** (ansible.builtin.command) - Conditional
- **Install krbrelayx dependencies in venv** (ansible.builtin.pip) - Conditional
- **Create wrapper scripts for krbrelayx tools** (ansible.builtin.copy) - Conditional
- **Clone dfscoerce from GitHub** (ansible.builtin.git) - Conditional
- **Make dfscoerce.py executable** (ansible.builtin.file) - Conditional
- **Create symlink for dfscoerce** (ansible.builtin.file) - Conditional

### main.yml


- **Include Linux tasks** (ansible.builtin.include_tasks) - Conditional

### mitm6_venv.yml


- **Install mitm6 in an isolated virtualenv** (ansible.builtin.pip)
- **Create wrapper script for mitm6** (ansible.builtin.copy)
- **Symlink mitm6 into /usr/bin** (ansible.builtin.file)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - coercion_tools
```

## Author Information

- **Author**: Jayson Grace
- **Company**: techvomit
- **License**: MIT

## Platforms


- Ubuntu: all
- Debian: all
- Kali: all
<!-- DOCSIBLE END -->
