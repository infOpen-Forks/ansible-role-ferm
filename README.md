# ferm

[![Build Status](https://travis-ci.org/Temelio/ansible-role-ferm.svg?branch=master)](https://travis-ci.org/Temelio/ansible-role-ferm)

Install ferm package.

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Locally, you can run tests on Docker (default driver) or Vagrant.
Travis run tests using Docker driver only.

Currently, tests are done on:
- Debian Jessie
- Ubuntu Trusty
- Ubuntu Xenial

and use:
- Ansible 2.0.x
- Ansible 2.1.x
- Ansible 2.2.x
- Ansible 2.3.x

### Running tests

#### Using Docker driver

```
$ tox
```

#### Using Vagrant driver

```
$ MOLECULE_DRIVER=vagrant tox
```

## Role Variables

### Default role variables

``` yaml
ferm_repository_cache_valid_time: 3600
ferm_service_enabled: True

ferm_config_directories_owner: 'root'
ferm_config_directories_group: 'root'
ferm_config_directories_mode: '0700'

ferm_config_files_owner: 'root'
ferm_config_files_group: 'root'
ferm_config_files_mode: '0400'

ferm_main_config_directory: '/etc/ferm'

# Configuration
ferm_tables:
  filter:
    INPUT:
      policy: 'ACCEPT'
      rules:
        # Connection tracking.
        - 'mod state state INVALID DROP;'
        - 'mod state state (ESTABLISHED RELATED) ACCEPT;'
        # Allow local connections.
        - 'interface lo ACCEPT;'
        # Respond to ping.
        - 'proto icmp icmp-type echo-request ACCEPT;'
        # Allow ssh connections.
        - 'proto tcp dport ssh ACCEPT;'
        - 'DROP;'
    OUTPUT:
      policy: 'ACCEPT'
      rules: []
    FORWARD:
      policy: 'DROP'
      rules: []
  nat:
    PREROUTING:
      policy: 'ACCEPT'
      rules: []
    POSTROUTING:
      policy: 'ACCEPT'
      rules: []
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
