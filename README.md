# ferm

[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-ferm/master.svg?label=travis_master)](https://travis-ci.org/Temelio/ansible-role-ferm)
[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-ferm/develop.svg?label=travis_develop)](https://travis-ci.org/Temelio/ansible-role-ferm)
[![Updates](https://pyup.io/repos/github/Temelio/ansible-role-ferm/shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-ferm/)
[![Python 3](https://pyup.io/repos/github/Temelio/ansible-role-ferm/python-3-shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-ferm/)
[![Ansible Role](https://img.shields.io/ansible/role/7902.svg)](https://galaxy.ansible.com/Temelio/ferm/)

Install ferm package.

## Requirements

This role requires Ansible 2.4 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- CentOS 7
- Debian Jessie
- Debian Stretch
- Ubuntu Xenial
- Ubuntu Bionic

and use:
- Ansible 2.4.x
- Ansible 2.5.x
- Ansible 2.6.x
- Ansible 2.7.x

### Running tests

#### Using Docker driver

```
$ tox
```

You can also configure molecule options and molecule command using environment variables:
* `MOLECULE_OPTIONS` Default: "--debug"
* `MOLECULE_COMMAND` Default: "test"

```
$ MOLECULE_OPTIONS='' MOLECULE_COMMAND=converge tox
```

## Role Variables

### Default role variables

``` yaml
# Repository management
ferm_repository_cache_valid_time: 3600
ferm_repository_update_cache: True

# Packages management
ferm_packages: "{{ _ferm_packages }}"

# Service management
ferm_service_enabled: True
ferm_service_name: "{{ _ferm_service_name }}"

# Paths management
ferm_config_directories_owner: 'root'
ferm_config_directories_group: 'root'
ferm_config_directories_mode: '0700'

ferm_config_files_owner: 'root'
ferm_config_files_group: 'root'
ferm_config_files_mode: '0400'

ferm_main_config_directory: '/etc/ferm'


# Configuration
# -----------------------------------------------------------------------------
ferm_variables: None
ferm_functions: None
ferm_rules: "{{ _ferm_rules }}"
ferm_hooks: |
  # Reload fail2ban rules automaticaly
  @hook post "type fail2ban-server > /dev/null && (fail2ban-client ping > /dev/null && fail2ban-client reload > /dev/null || true) || true";
  @hook flush "type fail2ban-server > /dev/null && (fail2ban-client ping > /dev/null && fail2ban-client reload > /dev/null || true) || true";
```

### Debian OS family variables

``` yaml
# Package management
_ferm_packages:
  - name: 'iptables'
  - name: 'ferm'

# Service management
_ferm_service_name: 'ferm'

# Configuration
_ferm_rules: |
  table filter {
    chain INPUT {
      policy DROP;
      # connection tracking
      mod state state INVALID DROP;
      mod state state (ESTABLISHED RELATED) ACCEPT;
      # allow local packet
      interface lo ACCEPT;
      # respond to ping
      proto icmp ACCEPT;
      # allow IPsec
      proto udp dport 500 ACCEPT;
      proto (esp ah) ACCEPT;
      # allow SSH connections
      proto tcp dport ssh ACCEPT;
    }
    chain OUTPUT {
      policy ACCEPT;
      # connection tracking
      mod state state INVALID DROP;
      mod state state (ESTABLISHED RELATED) ACCEPT;
    }
    chain FORWARD {
      policy DROP;
      # connection tracking
      mod state state INVALID DROP;
      mod state state (ESTABLISHED RELATED) ACCEPT;
    }
  }
```

## How manage configuration

Because Ferm configuration is rich, and I want this role keep simple, the
configuration is done via four variables:
* ferm_variables
* ferm_functions
* ferm_rules
* ferm_hooks

No process is done on these variables, their content is copied in configuration
file

Example, to define hooks to reload fail2ban automaticaly:
``` yaml
ferm_hooks: |
  @hook post "type fail2ban-server > /dev/null && (fail2ban-client ping > /dev/null && fail2ban-client reload > /dev/null || true) || true";
  @hook flush "type fail2ban-server > /dev/null && (fail2ban-client ping > /dev/null && fail2ban-client reload > /dev/null || true) || true";
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: Temelio.ferm }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Temelio company)
- http://www.temelio.com
- alexandre.chaussier [at] temelio.com
