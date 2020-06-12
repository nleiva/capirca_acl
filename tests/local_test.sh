#!/bin/bash

VERSION=0.1.1
END=2
DST_FOLDER=tests/collections

export ANSIBLE_STDOUT_CALLBACK=debug

rm -rf $DST_FOLDER
ansible-galaxy collection build --force
ansible-galaxy collection install --force nleiva-capirca_acl-${VERSION}.tar.gz -p $DST_FOLDER

for i in $(seq -f "%02g" 1 $END); do ansible-playbook tests/test${i}.yml -vvv; done