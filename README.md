# Capirca ACL Collection for Ansible

[![Build Status](https://travis-ci.org/nleiva/capirca_acl.svg?branch=master)](https://travis-ci.org/nleiva/capirca_acl)

This repo hosts an unofficial [Capirca](https://github.com/google/capirca) Ansible Collection.

This collection includes a module ([translate](docs/translate.md)) to use [Capirca](https://github.com/google/capirca) from your Ansible playbooks.

## Included content

Click on the name of a plugin or module to view that content's documentation:

  - **Modules**:
    - [translate](docs/translate.md)

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible [Galaxy](https://galaxy.ansible.com/nleiva/capirca_acl) CLI:

    ansible-galaxy collection install nleiva.capirca_acl

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: nleiva.capirca_acl
    version: 0.2.2
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
        filter_options:
          - ipv6-test-filter
          - inet6
        def_folder: "files/def"
        pol_file: "files/policies/terms.pol"
      register: testout

    - name: Dump the resulting ACL
      debug:
        msg: '{{ testout.message }}'
```

See [translate](docs/translate.md) for mode details.

## Publishing a new version

We first need to make sure the test cases run successfully:

```bash
make test-local
```

Then we need to TAG the version with a version number greater than the latest one:

```
export TAG=0.2.3
```

And finally build:

```
make build
```

It will end up in [Galaxy](https://galaxy.ansible.com/nleiva/capirca_acl)

## License

GNU General Public License v3.0 or later

See [LICENCE](LICENSE) to see the full text.