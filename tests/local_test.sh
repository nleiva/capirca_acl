#!/bin/bash

VERSION=0.3.0
END=10
DST_FOLDER=tests/collections

export ANSIBLE_STDOUT_CALLBACK=debug

rm -rf $DST_FOLDER
pip install -r requirements.txt --user
ansible-galaxy collection build --force
ansible-galaxy collection install --force nleiva-capirca_acl-${VERSION}.tar.gz -p $DST_FOLDER

for i in $(seq -f "%02g" 1 $END); do ansible-playbook tests/test${i}.yml -vvv; done
