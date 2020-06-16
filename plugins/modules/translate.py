#!/usr/bin/python

# Copyright: (c) 2020, Nicolas Leiva <nleiva@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '0.1.4',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: translate

short_description: Generate ACL's for different Operating Systems using Capirca.

version_added: "2.9"

description:
    - "Generate an ACL out of three input files; prefixes, ports and terms."

options:
    net_os:
        description:
            - This is the target Operating System
        required: true
    name:
        description:
            - This is the name of the ACL to generate
        required: false
    comment:
        description:
            - This is a comment/description of the ACL to generate
        required: false
    def_folder:
        description:
            - This is the folder where IP prefixes and Services are defined
        required: false
    pol_file:
        description:
            - This is the file where your ACL terms are defined
        required: false
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

requirements:
    - absl-py
    - ipaddress
    - capirca
author:
    - Nicolas Leiva (@nleiv4)
    
'''

EXAMPLES = '''
# Generate ACL for JunOS and save the output
- name: Run this module to generate an ACL
  nleiva.capirca_acl.translate:
    net_os: 'juniper'
  register: testout

# Generate ACL for Cisco IOS XR and save the output
- name: Run this module to generate an ACL
  nleiva.capirca_acl.translate:
    net_os: 'ciscoxr'
  register: testout
'''

RETURN = '''
original_message:
    description: The OPerating System option passed to the module
    type: str
    returned: always
message:
    description: The ACL that this module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
# from ansible.errors import AnsibleError

from string import Template

from capirca.lib import ciscoxr, ciscoasa, cisco, juniper, brocade, arista, aruba, ipset
from capirca.lib import iptables, nsxv, packetfilter, pcap, speedway, junipersrx, srxlo
from capirca.lib import windows_advfirewall, nftables, gce, paloaltofw, cloudarmor

from capirca.lib import naming, policy
#from capirca.lib import nacaddr


def get_acl(inputs):
    """Generates an ACL using Capirca.
    Args:
      inputs: Module parameters.
    Returns:
      ACL string.
    """
    header_base = '''
    header {
      comment:: "$comment"
      target:: $net_os $name
    }
    '''
    result = ""

    # Make sure ACL name doesn't have spaces.
    inputs['name'] = inputs['name'].replace(" ", "")

    header_template = Template(header_base)
    header = header_template.safe_substitute(inputs)

    defs = naming.Naming(inputs['def_folder'])
    terms = open(inputs['pol_file']).read()
    pol = policy.ParsePolicy(header + '\n' + terms, defs, optimize=True)

    # Exp info in weeks
    EXP_INFO = 2

    # List from https://github.com/google/capirca/blob/master/capirca/aclgen.py#L202
    # Does Python have a Switch statement?
    if inputs['net_os'] == 'juniper':
        result = juniper.Juniper(pol, EXP_INFO)
    if inputs['net_os'] == 'cisco':
        result = cisco.Cisco(pol, EXP_INFO)
    if inputs['net_os'] == 'ciscoasa':
        result = ciscoasa.CiscoASA(pol, EXP_INFO)
    if inputs['net_os'] == 'brocade':
        result = brocade.Brocade(pol, EXP_INFO)
    if inputs['net_os'] == 'arista':
        result = arista.Arista(pol, EXP_INFO)
    if inputs['net_os'] == 'aruba':
        result = aruba.Aruba(pol, EXP_INFO)
    if inputs['net_os'] == 'ipset':
        result = ipset.Ipset(pol, EXP_INFO)
    if inputs['net_os'] == 'iptables':
        result = iptables.Iptables(pol, EXP_INFO)
    if inputs['net_os'] == 'nsxv':
        result = nsxv.Nsxv(pol, EXP_INFO)
    if inputs['net_os'] == 'packetfilter':
        result = packetfilter.PacketFilter(pol, EXP_INFO)
    if inputs['net_os'] == 'pcap':
        result = pcap.PcapFilter(pol, EXP_INFO)
    if inputs['net_os'] == 'speedway':
        result = speedway.Speedway(pol, EXP_INFO)
    if inputs['net_os'] == 'srx':
        result = junipersrx.JuniperSRX(pol, EXP_INFO)
    if inputs['net_os'] == 'srxlo':
        result = srxlo.SRXlo(pol, EXP_INFO)
    if inputs['net_os'] == 'windows_advfirewall':
        result = windows_advfirewall.WindowsAdvFirewall(pol, EXP_INFO)   
    if inputs['net_os'] == 'ciscoxr':
        result = ciscoxr.CiscoXR(pol, EXP_INFO)
    if inputs['net_os'] == 'nftables':
        result = nftables.Nftables(pol, EXP_INFO)
    if inputs['net_os'] == 'gce':
        result = gce.GCE(pol, EXP_INFO)
    if inputs['net_os'] == 'paloalto':
        result = paloaltofw.PaloAltoFW(pol, EXP_INFO)  
    if inputs['net_os'] == 'cloudarmor':
        result = cloudarmor.CloudArmor(pol, EXP_INFO)  

    return str(result)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        # TODO: Complete net_os choice list.
        # Supported Capirca OSes: https://github.com/google/capirca/blob/master/capirca/aclgen.py#L202
        net_os      = dict(type='str', required=True, choices=['juniper', 'cisco', 'ciscoasa', 'ciscoxr', 'brocade', \
                                                                'arista', 'aruba', 'ipset', 'iptables', 'nsxv', \
                                                                'packetfilter', 'pcap', 'speedway', 'srx', 'srxlo', \
                                                                'windows_advfirewall', 'nftables', 'gce', 'paloalto', 'cloudarmor' \
                                                                'fail me']),
        name        = dict(type='str', required=False, default="Default-ACL-Name"),
        comment     = dict(type='str', required=False, default="Default Comment"),
        def_folder  = dict(type='str', required=False, default="integration/targets/translate/files/def"),
        pol_file    = dict(type='str', required=False, default="integration/targets/translate/files/policies/terms.pol"),
        new         = dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec       = module_args,
        supports_check_mode = True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    acl = get_acl(module.params)

    result['original_message'] = module.params['net_os']
    result['message'] = acl

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['net_os'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
