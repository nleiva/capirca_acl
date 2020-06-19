#!/bin/bash

VERSION=0.2.4
DST_FOLDER=docs/collections

export ANSIBLE_STDOUT_CALLBACK=debug

rm -rf $DST_FOLDER
ansible-galaxy collection build --force
ansible-galaxy collection install --force nleiva-capirca_acl-${VERSION}.tar.gz -p $DST_FOLDER

cd docs && ansible-playbook example.yml
cd ..
