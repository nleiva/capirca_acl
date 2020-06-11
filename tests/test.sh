#!/bin/bash

VERSION=0.1.1
TEST=02

rm -rf collections
ansible-galaxy collection build --force
ansible-galaxy collection install nleiva-capirca_acl-${VERSION}.tar.gz -p ./collections

ansible-playbook test${TEST}.yml -vvv