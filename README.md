# Capirca ACL Collection for Ansible

[![Build Status](https://travis-ci.org/nleiva/capirca_acl.svg?branch=master)](https://travis-ci.org/nleiva/capirca_acl)

This repo hosts an unofficial [Capirca](https://github.com/google/capirca) Ansible Collection.

The collection includes a module to use Caprica from your Ansible playbooks.

## Included content

Click on the name of a plugin or module to view that content's documentation:

  - **Modules**:
    - [translate](docs/translate.md)

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy CLI:

    ansible-galaxy collection install nleiva.capirca_acl

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: nleiva.capirca_acl
    version: 0.1.4
```

### Using modules from the Capirca ACL Collection in your playbooks

You can either call modules by their Fully Qualified Collection Namespace (FQCN), like `nleiva.capirca_acl.translate`, or you can call modules by their short name if you list the `nleiva.capirca_acl` collection in the playbook's `collections`, like so:

```yaml
---
- hosts: localhost
  gather_facts: no
  connection: local

  collections:
    - nleiva.capirca_acl

  tasks:
    - name: Run this module to generate an ACL
      translate:
        platform: 'ciscoxr'
        def_folder: "files/def"
        pol_file: "files/policies/terms.pol"
      register: testout

    - name: Dump the resulting ACL
      debug:
        msg: '{{ testout.message }}'
```

See [translate](docs/translate.md) for mode details.

## Pushing a new version

Example

```
export TAG=0.1.5
make build
```

## License

GNU General Public License v3.0 or later

See [LICENCE](LICENSE) to see the full text.