# README

The `test_tempfile.py` module added here is only used for the `setup_remote_tmp_dir.yml` temporary directory setup task. It is a clone of the `tempfile.py` community-supported Ansible module, and has to be included with the tests here because it is not available in the `ansible-base` distribution against which this collection is tested.

Idea stolen from: [ansible-collections/community.kubernetes](https://github.com/ansible-collections/community.kubernetes/blob/master/tests/integration/targets/kubernetes/library/README.md)