#!/bin/bash

VERSION=0.1.1
IMAGE=ubuntu1804

ansible-galaxy collection build --force

# Test Collection. Need to do it in a different folder: https://github.com/ansible/ansible/pull/69341
mkdir ../temp
ansible-galaxy collection install --force nleiva-capirca_acl-${VERSION}.tar.gz -p ../temp
cd ../temp/ansible_collections/nleiva/capirca_acl
ansible-test integration --list-targets
ansible-test integration --docker ${IMAGE}
cd ../../../..