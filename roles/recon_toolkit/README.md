<!-- DOCSIBLE START -->
# recon_toolkit

## Description

Install reconnaissance tools for subdomain enumeration, HTTP discovery, web crawling, vulnerability scanning, and parameter analysis

## Requirements

- Ansible >= 2.14

## Dependencies


- cowdogmoo.workstation.package_management
- cowdogmoo.workstation.mise

## Role Variables

### Default Variables (main.yml)

| Variable | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `recon_toolkit_cleanup` | bool | <code>False</code> | No description |
| `recon_toolkit_install_path` | str | <code>/opt/recon_toolkit</code> | No description |
| `recon_toolkit_username` | str | <code>{% if ansible_facts&#91;'os_family'&#93; == 'Darwin' %}{{ ansible_facts&#91;'user_id'&#93; }}{% else %}{{ ansible_facts&#91;'distribution'&#93; &#124; lower }}{% endif %}</code> | No description |
| `recon_toolkit_usergroup` | str | <code>{% if ansible_facts&#91;'os_family'&#93; == 'Darwin' %}staff{% elif ansible_facts&#91;'os_family'&#93; == 'Debian' %}{{ ansible_facts&#91;'user_id'&#93; }}{% elif ansible_facts&#91;'os_family'&#93; == 'RedHat' %}{{ ansible_facts&#91;'user_id'&#93; }}{% else %}{{ ansible_facts&#91;'distribution'&#93; &#124; lower }}{% endif %}</code> | No description |
| `recon_toolkit_shell` | str | <code>{% if ansible_facts&#91;'os_family'&#93; == 'Darwin' %}/bin/zsh{% else %}/bin/bash{% endif %}</code> | No description |
| `recon_toolkit_mise_plugins` | list | <code>&#91;&#93;</code> | No description |
| `recon_toolkit_mise_plugins.0` | dict | <code>{}</code> | No description |
| `recon_toolkit_mise_plugins.1` | dict | <code>{}</code> | No description |
| `recon_toolkit_mise_plugins.2` | dict | <code>{}</code> | No description |
| `recon_toolkit_core_packages` | list | <code>&#91;&#93;</code> | No description |
| `recon_toolkit_core_packages.0` | str | <code>curl</code> | No description |
| `recon_toolkit_core_packages.1` | str | <code>jq</code> | No description |
| `recon_toolkit_core_packages.2` | str | <code>dnsutils</code> | No description |
| `recon_toolkit_core_packages.3` | str | <code>git</code> | No description |
| `recon_toolkit_core_packages.4` | str | <code>wget</code> | No description |
| `recon_toolkit_core_packages.5` | str | <code>unzip</code> | No description |
| `recon_toolkit_core_packages.6` | str | <code>build-essential</code> | No description |
| `recon_toolkit_install_subfinder` | bool | <code>True</code> | No description |
| `recon_toolkit_install_amass` | bool | <code>True</code> | No description |
| `recon_toolkit_install_assetfinder` | bool | <code>True</code> | No description |
| `recon_toolkit_install_ctfr` | bool | <code>True</code> | No description |
| `recon_toolkit_ctfr_repo` | str | <code>https://github.com/UnaPibaGeek/ctfr.git</code> | No description |
| `recon_toolkit_ctfr_install_dir` | str | <code>/opt/ctfr</code> | No description |
| `recon_toolkit_install_massdns` | bool | <code>True</code> | No description |
| `recon_toolkit_install_puredns` | bool | <code>True</code> | No description |
| `recon_toolkit_install_shuffledns` | bool | <code>True</code> | No description |
| `recon_toolkit_massdns_repo` | str | <code>https://github.com/blechschmidt/massdns.git</code> | No description |
| `recon_toolkit_massdns_install_dir` | str | <code>/opt/massdns</code> | No description |
| `recon_toolkit_install_httpx` | bool | <code>True</code> | No description |
| `recon_toolkit_install_dnsx` | bool | <code>True</code> | No description |
| `recon_toolkit_install_nmap` | bool | <code>True</code> | No description |
| `recon_toolkit_install_rustscan` | bool | <code>True</code> | No description |
| `recon_toolkit_install_masscan` | bool | <code>True</code> | No description |
| `recon_toolkit_install_whatweb` | bool | <code>True</code> | No description |
| `recon_toolkit_install_smap` | bool | <code>True</code> | No description |
| `recon_toolkit_rustscan_version` | str | <code>2.4.1</code> | No description |
| `recon_toolkit_rustscan_archives` | dict | <code>{}</code> | No description |
| `recon_toolkit_rustscan_archives.x86_64` | str | <code>x86_64-linux-rustscan.tar.gz.zip</code> | No description |
| `recon_toolkit_rustscan_archives.aarch64` | str | <code>aarch64-linux-rustscan.zip</code> | No description |
| `recon_toolkit_install_katana` | bool | <code>True</code> | No description |
| `recon_toolkit_install_gospider` | bool | <code>True</code> | No description |
| `recon_toolkit_install_hakrawler` | bool | <code>True</code> | No description |
| `recon_toolkit_install_gau` | bool | <code>True</code> | No description |
| `recon_toolkit_install_waybackurls` | bool | <code>True</code> | No description |
| `recon_toolkit_install_linkfinder` | bool | <code>True</code> | No description |
| `recon_toolkit_install_secretfinder` | bool | <code>True</code> | No description |
| `recon_toolkit_linkfinder_repo` | str | <code>https://github.com/GerbenJavado/LinkFinder.git</code> | No description |
| `recon_toolkit_linkfinder_install_dir` | str | <code>/opt/LinkFinder</code> | No description |
| `recon_toolkit_secretfinder_repo` | str | <code>https://github.com/m4ll0k/SecretFinder.git</code> | No description |
| `recon_toolkit_secretfinder_install_dir` | str | <code>/opt/SecretFinder</code> | No description |
| `recon_toolkit_install_nuclei` | bool | <code>True</code> | No description |
| `recon_toolkit_install_trufflehog` | bool | <code>True</code> | No description |
| `recon_toolkit_install_gitleaks` | bool | <code>True</code> | No description |
| `recon_toolkit_install_uncover` | bool | <code>True</code> | No description |
| `recon_toolkit_install_shodan` | bool | <code>True</code> | No description |
| `recon_toolkit_install_gf` | bool | <code>True</code> | No description |
| `recon_toolkit_install_arjun` | bool | <code>True</code> | No description |
| `recon_toolkit_install_retire` | bool | <code>True</code> | No description |
| `recon_toolkit_install_paramspider` | bool | <code>True</code> | No description |
| `recon_toolkit_gf_patterns_repo` | str | <code>https://github.com/1ndianl33t/Gf-Patterns.git</code> | No description |
| `recon_toolkit_paramspider_repo` | str | <code>https://github.com/devanshbatham/ParamSpider.git</code> | No description |

### Role Variables (main.yml)

| Variable | Type | Value | Description |
| -------- | ---- | ----- | ----------- |
| `recon_toolkit_packages` | dict | `{}` | No description |
| `recon_toolkit_packages.essential` | list | `[]` | No description |
| `recon_toolkit_packages.essential.0` | str | `curl` | No description |
| `recon_toolkit_packages.essential.1` | str | `dnsutils` | No description |
| `recon_toolkit_packages.essential.2` | str | `git` | No description |
| `recon_toolkit_packages.essential.3` | str | `jq` | No description |
| `recon_toolkit_packages.essential.4` | str | `unzip` | No description |
| `recon_toolkit_packages.essential.5` | str | `wget` | No description |
| `recon_toolkit_packages.build_only` | list | `[]` | No description |
| `recon_toolkit_packages.build_only.0` | str | `build-essential` | No description |
| `recon_toolkit_packages.build_only.1` | str | `g++` | No description |
| `recon_toolkit_packages.build_only.2` | str | `gcc` | No description |
| `recon_toolkit_packages.build_only.3` | str | `make` | No description |
| `recon_toolkit_packages.build_only.4` | str | `libffi-dev` | No description |
| `recon_toolkit_packages.build_only.5` | str | `libssl-dev` | No description |
| `recon_toolkit_packages.runtime_debian` | list | `[]` | No description |
| `recon_toolkit_packages.runtime_debian.0` | str | `masscan` | No description |
| `recon_toolkit_packages.runtime_debian.1` | str | `nmap` | No description |
| `recon_toolkit_packages.runtime_debian.2` | str | `whatweb` | No description |
| `recon_toolkit_common_install_packages` | str | `{{ recon_toolkit_packages.essential + recon_toolkit_packages.build_only }}` | No description |
| `recon_toolkit_debian_packages` | str | `{{ recon_toolkit_packages.runtime_debian }}` | No description |
| `recon_toolkit_cleanup_packages_debian` | str | `{{ recon_toolkit_packages.build_only }}` | No description |
| `recon_toolkit_cleanup_paths` | list | `[]` | No description |
| `recon_toolkit_cleanup_paths.0` | str | `{{ recon_toolkit_user_home }}/go` | No description |
| `recon_toolkit_cleanup_paths.1` | str | `{{ recon_toolkit_user_home }}/.cache` | No description |
| `recon_toolkit_cleanup_paths.2` | str | `{{ recon_toolkit_user_home }}/.local` | No description |
| `recon_toolkit_cleanup_paths.3` | str | `{{ recon_toolkit_user_home }}/.config` | No description |
| `recon_toolkit_cleanup_paths.4` | str | `/root/go` | No description |
| `recon_toolkit_cleanup_paths.5` | str | `/root/.cache` | No description |
| `recon_toolkit_cleanup_paths.6` | str | `/root/.local` | No description |
| `recon_toolkit_cleanup_paths.7` | str | `/root/.ssh` | No description |
| `recon_toolkit_cleanup_paths.8` | str | `/tmp/*` | No description |
| `recon_toolkit_cleanup_paths.9` | str | `/var/tmp/*` | No description |

## Tasks

### http_discovery.yml


- **Install httpx** (ansible.builtin.shell) - Conditional
- **Install dnsx** (ansible.builtin.shell) - Conditional
- **Install rustscan** (block) - Conditional
- **Check if rustscan is already installed** (ansible.builtin.command)
- **Set rustscan archive name based on architecture** (ansible.builtin.set_fact) - Conditional
- **Download rustscan binary archive** (ansible.builtin.get_url) - Conditional
- **Create rustscan temp extraction directory** (ansible.builtin.file) - Conditional
- **Extract rustscan archive (zip layer)** (ansible.builtin.unarchive) - Conditional
- **Find nested tar.gz in extracted files (x86_64 has zip-wrapped tar.gz)** (ansible.builtin.find) - Conditional
- **Extract nested tar.gz if present** (ansible.builtin.unarchive) - Conditional
- **Find rustscan binary in extracted files** (ansible.builtin.find) - Conditional
- **Install rustscan binary to /usr/local/bin** (ansible.builtin.copy) - Conditional
- **Clean up rustscan temp files** (ansible.builtin.file)
- **Install smap** (ansible.builtin.shell) - Conditional

### main.yml


- **Set recon_toolkit user home directory** (ansible.builtin.include_tasks)
- **Install required packages for recon_toolkit** (ansible.builtin.include_role)
- **Create user** (ansible.builtin.include_role)
- **Ensure home directory exists for recon_toolkit user** (ansible.builtin.file)
- **Check if .bashrc exists for recon_toolkit user** (ansible.builtin.stat)
- **Ensure .bashrc exists for recon_toolkit user** (ansible.builtin.file) - Conditional
- **Check if mise is installed for recon_toolkit user** (ansible.builtin.stat)
- **Check if mise binary is installed** (ansible.builtin.stat)
- **Install mise and associated plugins for recon_toolkit user** (ansible.builtin.include_role) - Conditional
- **Ensure golang is installed for user** (ansible.builtin.shell)
- **Add recon toolkit paths to user's bashrc** (ansible.builtin.blockinfile)
- **Include subdomain enumeration tool tasks** (ansible.builtin.include_tasks)
- **Include HTTP and service discovery tool tasks** (ansible.builtin.include_tasks)
- **Include web crawling and JS analysis tool tasks** (ansible.builtin.include_tasks)
- **Include vulnerability and secret scanning tool tasks** (ansible.builtin.include_tasks)
- **Include parameter and pattern analysis tool tasks** (ansible.builtin.include_tasks)

### param_analysis.yml


- **Install gf** (block) - Conditional
- **Install gf binary via go install** (ansible.builtin.shell)
- **Ensure .gf patterns directory exists** (ansible.builtin.file)
- **Clone gf patterns** (ansible.builtin.git)
- **Find gf pattern files** (ansible.builtin.find) - Conditional
- **Copy gf pattern files to .gf directory** (ansible.builtin.copy) - Conditional
- **Clean up gf patterns temp directory** (ansible.builtin.file)
- **Install arjun via pipx** (block) - Conditional
- **Check if pipx is available for arjun** (ansible.builtin.command)
- **Install pipx for arjun** (ansible.builtin.apt) - Conditional
- **Check if arjun is already installed via pipx** (ansible.builtin.command)
- **Install arjun via pipx** (ansible.builtin.command) - Conditional
- **Install retire.js** (block) - Conditional
- **Ensure nodejs is installed via mise** (ansible.builtin.shell)
- **Check if retire.js is already installed** (ansible.builtin.shell)
- **Install retire.js globally via npm** (ansible.builtin.shell) - Conditional
- **Install paramspider via pipx** (block) - Conditional
- **Check if pipx is available for paramspider** (ansible.builtin.command)
- **Install pipx for paramspider** (ansible.builtin.apt) - Conditional
- **Check if paramspider is already installed via pipx** (ansible.builtin.command)
- **Install paramspider via pipx** (ansible.builtin.command) - Conditional

### recon_toolkit_get_user_home.yml


- **Gather available local users** (ansible.builtin.getent) - Conditional
- **Set user home directory** (ansible.builtin.set_fact) - Conditional
- **Set user home directory for macOS** (ansible.builtin.set_fact) - Conditional

### subdomain_enum.yml


- **Install subfinder** (ansible.builtin.shell) - Conditional
- **Install amass** (ansible.builtin.shell) - Conditional
- **Install assetfinder** (ansible.builtin.shell) - Conditional
- **Install ctfr** (block) - Conditional
- **Clone ctfr repository** (ansible.builtin.git)
- **Install ctfr Python dependencies** (ansible.builtin.pip)
- **Create ctfr wrapper in /usr/local/bin** (ansible.builtin.copy)
- **Install massdns** (block) - Conditional
- **Check if massdns is already installed** (ansible.builtin.command)
- **Clone massdns repository** (ansible.builtin.git) - Conditional
- **Build massdns** (ansible.builtin.command) - Conditional
- **Install massdns binary to /usr/local/bin** (ansible.builtin.copy) - Conditional
- **Install puredns** (ansible.builtin.shell) - Conditional
- **Install shuffledns** (ansible.builtin.shell) - Conditional

### vuln_scanning.yml


- **Install nuclei** (ansible.builtin.shell) - Conditional
- **Install trufflehog** (block) - Conditional
- **Check if trufflehog is already installed** (ansible.builtin.command)
- **Install trufflehog via install script** (ansible.builtin.shell) - Conditional
- **Install gitleaks** (ansible.builtin.shell) - Conditional
- **Install uncover** (ansible.builtin.shell) - Conditional
- **Install shodan CLI** (block) - Conditional
- **Check if pipx is available for shodan** (ansible.builtin.command)
- **Install pipx for shodan** (ansible.builtin.apt) - Conditional
- **Check if shodan is already installed via pipx** (ansible.builtin.command)
- **Install shodan via pipx** (ansible.builtin.command) - Conditional

### web_crawling.yml


- **Install katana** (ansible.builtin.shell) - Conditional
- **Install gospider** (ansible.builtin.shell) - Conditional
- **Install hakrawler** (ansible.builtin.shell) - Conditional
- **Install gau** (ansible.builtin.shell) - Conditional
- **Install waybackurls** (ansible.builtin.shell) - Conditional
- **Install LinkFinder** (block) - Conditional
- **Clone LinkFinder repository** (ansible.builtin.git)
- **Install LinkFinder Python dependencies** (ansible.builtin.pip)
- **Create LinkFinder wrapper in /usr/local/bin** (ansible.builtin.copy)
- **Install SecretFinder** (block) - Conditional
- **Clone SecretFinder repository** (ansible.builtin.git)
- **Install SecretFinder Python dependencies** (ansible.builtin.pip)
- **Create SecretFinder wrapper in /usr/local/bin** (ansible.builtin.copy)

## Example Playbook

```yaml
- hosts: servers
  roles:
    - recon_toolkit
```

## Author Information

- **Author**: Jayson Grace
- **Company**: techvomit
- **License**: MIT

## Platforms


- Ubuntu: all
- Kali: all
<!-- DOCSIBLE END -->
