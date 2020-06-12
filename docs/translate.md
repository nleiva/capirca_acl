# Translate module

This modules uses [Capirca](https://github.com/google/capirca) to translate a generic ACL into different target formats. 

See [Capirca Design Doc](https://github.com/google/capirca/wiki/Capirca-design) or their [Wiki](https://github.com/google/capirca/wiki/) for more info.

## Requirements

These are the minimun requirement to run this in CentOS/RHEL. Replace `yum` for `apt/get` for Ubuntu.

```bash
yum install -y python3 python-pip
pip3 install absl-py ipaddress capirca ansible
```

## Examples

You first need to install the Collection with `ansible-galaxy collection install nleiva-capirca_acl`

Then use it as follwos:

```yaml
  tasks:
  - name: Run this module to generate an ACL
    nleiva.capirca_acl.translate:
      net_os: 'ciscoxr'
      def_folder: "sample"
      pol_file: "sample/terms.pol"
    register: testout
  
  - name: Dump the resulting ACL
    debug:
      msg: "{{ testout.message }}"
```

Where `net_os`, `def_folder`, and `pol_file` are inputs that are explained below.

### net_os

Is the target platform, one of:

- `juniper`: Juniper JunOS
- `cisco`: Cisco IOS
- `ciscoasa`: Cisco ASA FW
- `ciscoxr`: Cisco IOS XR

We are extending the module to support all platforms supported by [Capirca](https://github.com/google/capirca).

### def_folder

It's a folder where we keep the [Naming definitions](https://github.com/google/capirca/wiki/Naming-definitions);  network and service "address books" that are used in the creation of policy files.

For example, here is an example of a service definition:

```bash
DNS = 53/tcp  # transfers
      53/udp  # queries
```

Likewise, here is an example of a network definition:

```bash
RFC1918 = 192.168.0.0/16  # company DMZ networks
           172.16.0.0/12   # company remote offices
           10.0.0.0/8      # company production networks
INTERNAL = RFC1918

GOOGLE_DNS = 8.8.4.4/32               # IPv4 Anycast
             8.8.8.8/32               # IPv4 Anycast
             2001:4860:4860::8844/128 # IPv6 Anycast
             2001:4860:4860::8888/128 # IPv6 Anycast
```

See the files we use for testing [here](../tests/integration/targets/translate/files/def): [service definition](../tests/integration/targets/translate/files/def/ports.svc) and [network definition](../tests/integration/targets/translate/files/def/prefixes.net).


### pol_file

[Term Definition Format](https://github.com/google/capirca/wiki/Capirca-design#term-definition-format)

```ruby
term discard-spoofs {
  source-address:: RFC1918
  action:: deny
}

term accept-to-honestdns {
  comment:: "Allow name resolution using honestdns."
  destination-address:: GOOGLE_DNS
  destination-port:: DNS
  protocol:: udp
  action:: accept
}

term default-permit {
  comment:: "Allow what's left."
  action:: accept
}
```

## In action

```
⇨  make example
...

PLAY [Dump generated ACL for a given OS.] ***********************************************************************************************************************************

TASK [Run this module to generate an ACL] ***********************************************************************************************************************************
ok: [localhost]

TASK [Dump the resulting ACL] ***********************************************************************************************************************************************
ok: [localhost] => {}

MSG:

! $Id:$
! $Date:$
! $Revision:$
no ipv4 access-list Default-ACL-Name
ipv4 access-list Default-ACL-Name
 remark $Id:$
 remark Default Comment


 remark discard-spoofs
 deny ipv4 10.0.0.0 0.255.255.255 any
 deny ipv4 172.16.0.0 0.15.255.255 any
 deny ipv4 192.168.0.0 0.0.255.255 any


 remark accept-to-honestdns
 remark Allow name resolution using honestdns.
 permit udp any host 8.8.4.4 eq 53
 permit udp any host 8.8.8.8 eq 53


 remark default-permit
 remark Allow what's left.
 permit ipv4 any any

exit


PLAY RECAP ******************************************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```