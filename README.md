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
    version: 0.2.3
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

### Run an example

The example documented in [translate](docs/translate.md) can be run with:

```bash
make example
```

## Testing and Development

### Testing with `ansible-test`

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

You can run the collection's test suites with the command:

```bash
make test-remote
```

### Testing locally with ansible

You can run the collection's test suites without [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html) with the command:

```bash
make test-local
```

## Publishing New Versions

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

It will end up in [Capirca Collection Galaxy page](https://galaxy.ansible.com/nleiva/capirca_acl) if you have access to the namespace.

## More Information

For more information about [Capirca](https://github.com/google/capirca), join the `#capirca` channel on [NetworkToCode Slack](https://networktocode.slack.com/), and browse the resources in the [Capirca Wiki](https://github.com/google/capirca/wiki) page.

- [Multi-Platform ACL Generation and Testing](https://rvasec.com/slides/2013/Watson-Capirca.pdf)
- [Capirca Wiki](https://github.com/google/capirca/wiki)

## License

GNU General Public License v3.0 or later

See [LICENCE](LICENSE) to see the full text.