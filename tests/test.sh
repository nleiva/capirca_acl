#!/bin/bash

VERSION=0.1.1
TEST=02

rm -rf collections
ansible-galaxy collection build --force
ansible-galaxy collection install nleiva-capirca_acl-${VERSION}.tar.gz -p ./collections

ansible-playbook test${TEST}.yml -vvv

cd collections/ansible_collections/nleiva/capirca_acl
# https://github.com/ansible/ansible/pull/69341
# ansible-test integration --docker fedora29
ansible-test integration --list-targets
cd ../../../..