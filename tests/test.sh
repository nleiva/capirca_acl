#!/bin/bash

VERSION=0.1.1
TEST=02

# Test locally
rm -rf collections
ansible-galaxy collection build --force
ansible-galaxy collection install nleiva-capirca_acl-${VERSION}.tar.gz -p ./collections

ansible-playbook test${TEST}.yml -vvv

# Test Collection
mkdir ../temp
ansible-galaxy collection install nleiva-capirca_acl-${VERSION}.tar.gz -p ../temp
cd ../temp/ansible_collections/nleiva/capirca_acl
# https://github.com/ansible/ansible/pull/69341
ansible-test integration --list-targets
ansible-test integration --docker ubuntu1804
cd ../../../..