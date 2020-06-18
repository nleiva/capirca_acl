# Translate module

This modules uses [Capirca](https://github.com/google/capirca) to translate a generic ACL into different target formats. 

See [Capirca Design Doc](https://github.com/google/capirca/wiki/Capirca-design) or their [Wiki](https://github.com/google/capirca/wiki/) for more info.

## Requirements

These are the minimum requirement to run this in CentOS/RHEL. Replace `yum` for `apt/get` for Ubuntu.

```bash
yum install -y python3 python-pip
pip3 install absl-py ipaddress capirca ansible
```

## Examples

You first need to install the Collection with `ansible-galaxy collection install nleiva-capirca_acl`

Then use it as follows:

```yaml
  tasks:
  - name: Run this module to generate an ACL
    nleiva.capirca_acl.translate:
      platform: 'ciscoxr'
      filter_options: 
        - ACL-Name
      def_folder: "sample"
      pol_file: "sample/terms.pol"
    register: testout
  
  - name: Dump the resulting ACL
    debug:
      msg: "{{ testout.message }}"
```

Where `platform`, `filter_options`, `def_folder`, and `pol_file` are inputs that are explained below.

### platform

Is the target platform, one of:

- `arista`: Arista EOS
- `aruba`: Aruba ArubaOS
- `brocade`: Brocade Network OS
- `cisco`: Cisco IOS
- `ciscoasa`: Cisco ASA FW
- `ciscoxr`: Cisco IOS XR
- `cloudarmor`: Google Cloud Armor
- `gce`: Google Compute Engine
- `ipset`: Linux ipset
- `iptables`: Linux iptables
- `juniper`: Juniper JunOS
- `srx`: Juniper SRX
- `nftables`: Linux nftables
- `nsxv`: VMWare NSX
- `packetfilter`: OpenBSD PF
- `paloalto`: Palo Alto PAN-OS
- `pcap`: PCAP filter
- `speedway`: Speedway produces Iptables filtering output that is suitable for passing to the 'iptables-restore' command
- `srxlo`: SRX Loopback is a stateless Juniper ACL with minor changes.
- `windows_advfirewall`: Windows Advanced Firewall


### filter_options

It a list used to define the type of filter, a descriptor or name, direction (if applicable) and format (ipv4/ipv6). The order of the options is relevant and they are platform specific. The following tables describe their purpose. More details in [Capirca Policy-format](https://github.com/google/capirca/wiki/Policy-format). We have grouped together platforms that have similar options for the ease of reading:

#### Group 1

|   Platform  |   Option 1    |  Option 2                       | Option 3 | Option 4 |
| ----------- | ------------- | ------------------------------- |----------|----------|
|`arista`     | [filter name] | {standard/extended/object-group/inet6} |||
|`brocade`    | [filter name] | {extended/standard/object-group/inet6/mixed} |{dsmo} ||
|`cisco`      | [filter name] | {extended/standard/object-group/inet6/mixed} |{dsmo} ||
|`ciscoxr`    | [filter name] | {extended/standard/object-group/inet6/mixed} |{dsmo} ||
|`ciscoasa`   | [filter name] | |||
|`aruba`      | [filter name] | {ipv6} |||
|`gce`        | [filter name] | [direction] |||
|`pcap`       | [filter name] | [direction] |||
|`juniper`    | [filter name] | {inet/inet6/bridge} |{dsmo} |{not-interface-specific} |
|`srxlo`      | [filter name] | {inet/inet6/bridge} |{dsmo} |{not-interface-specific} |

Where:

- `filter name`: defines the name or number of the filter (**NO SPACES**)
- `extended`: specifies that the output should be an extended access list, and the filter name should be non-numeric. This is the default option.
- `standard`: specifies that the output should be a standard access list, and the filter name should be numeric and in the range of 1-99.
- `object-group`: specifies this is an extended access list, and that object-groups should be used for ports and addresses.
- `inet`: specifies the output should be for IPv4 only filters. This is the default format.
- `inet6`: specifies the output be for IPv6 only filters.
- `mixed`: specifies output will include both IPv6 and IPv4 filters.
- `dsmo`: Enable discontinuous subnet mask summarization.
- `ipv6`: specifies the output be for IPv6 only filters (`aruba`).
- `bridge`: specifies the output should render a Juniper bridge filter.
- `direction`: defines the direction, valid inputs are INGRESS and EGRESS (default:INGRESS) (`gce`).
- `not-interface-specific`: Toggles "interface-specific" inside of a term.

#### Group 2

|   Platform  |   Option 1    |  Option 2                           | Option 3 | Option 4 |  Option 5  |
| ----------- | ------------- | ------------------------------------|----------|--------- | ---------- |
|`ipset`      | [INPUT/OUTPUT/FORWARD/custom] |{ACCEPT/DROP} |{abbreviateterms} |{nostate} |{inet/inet6} |
|`iptables`   | [INPUT/OUTPUT/FORWARD/custom] |{ACCEPT/DROP} |{abbreviateterms} |{nostate} |{inet/inet6} |
|`speedway`   | [INPUT/OUTPUT/FORWARD/custom] |{ACCEPT/DROP} |{abbreviateterms} |{nostate} |{inet/inet6} |


Where:

- `INPUT`: apply the terms to the input filter.
- `OUTPUT`: apply the terms to the output filter.
- `FORWARD`: apply the terms to the forwarding filter.
- `custom`: create the terms under a custom filter name, which must then be linked/jumped to from one of the default filters (e.g. `iptables -A input -j custom`)
- `ACCEPT`: specifies that the default policy on the filter should be 'accept'.
- `DROP`: specifies that the default policy on the filter should be to 'drop'.
- `abbreviateterms`: specifies to abbreviate term names if necessary (see lib/iptables.py:CheckTerMLength for abbreviation table)
- `nostate`: specifies to produce 'stateless' filter output (e.g. no connection tracking)


#### Group 3

|   Platform  |   Option 1    |  Option 2                       | Option 3 | Option 4 | Option 5 |
| ----------- | ------------- | ------------------------------- |----------|----------|--------- |
|`srx`        | [from-zone name] | [to-zone name] | {inet} |||
|`paloalto`   | [from-zone name] | [to-zone name] ||||
|`nftables`   | [chain name] | [filter name] | [priority] | [inet|inet6] ||
|`packetfilter` | {inet/inet6/mixed} ||||
|`windows_advfirewall` | {out/in} | {inet/inet6/mixed} |||
|`nsxv`       | {section_name} | {inet/inet6/mixed} | section-id | securitygroup | securitygroupId     |

Where:

- `zone name`: from/to specified zone name.
- `chain name`: defines the name of the nftables chain.
- `priority`: defines the integer of the nftables chain priority.
- `out`: Specifies that the direction of packet flow is out. (default)
- `in`: Specifies that the direction of packet flow is in.
- `sectionId`: specifies the Id for the section [optional]
- `securitygroup`: specifies that the appliedTo should be security group [optional]
- `securitygroupId`: specifies the Id of the security group [mandatory if securitygroup is given]


#### Examples

```yaml
  tasks:
  - name: Run this module to generate an ACL
    nleiva.capirca_acl.translate:
      platform: 'ciscoxr'
      filter_options:
        - ipv6-test-filter
        - inet6
      def_folder: "sample"
      pol_file: "sample/terms.pol"
    register: testout
```

```yaml
  tasks:
  - name: Run this module to generate an ACL
    nleiva.capirca_acl.translate:
      platform: 'iptables'
      filter_options: ['INPUT', 'ACCEPT', 'abbreviateterms']
      def_folder: "sample"
      pol_file: "sample/terms.pol"
    register: testout
```

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

The policy file will consist of terms, comments, and other directives. Terms are the specific rules relating a variety of properties such as source/destination addresses, protocols, ports, actions, etc. See [Term Definition Format](https://github.com/google/capirca/wiki/Capirca-design#term-definition-format) for details. 

This is Policy example:


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

You can run this module with the examples files displayed in here by running `make example` after cloning the repo. Make sure you meet the requirement like having `absl-py`, `ipaddress`, and `capirca` libraries installed.

```swift
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

If you switched the `platform` to `juniper`.

```yaml
  tasks:
  - name: Run this module to generate an ACL
    nleiva.capirca_acl.translate:
      platform: 'junos'
      def_folder: "sample"
      pol_file: "sample/terms.pol"
    register: testout
...
```

Then the output would be:

```swift
...
TASK [Dump the resulting ACL] ***********************************************************************************************************************************************
ok: [localhost] => {}

MSG:

firewall {
    family inet {
        replace:
        /*
        ** $Id:$
        ** $Date:$
        ** $Revision:$
        **
        ** Default Comment
        */
        filter Default-ACL-Name {
            interface-specific;
            term discard-spoofs {
                from {
                    source-address {
                        /* company production networks */
                        10.0.0.0/8;
                        /* company remote offices */
                        172.16.0.0/12;
                        /* company DMZ networks */
                        192.168.0.0/16;
                    }
                }
                then {
                    discard;
                }
            }
            /*
            ** Allow name resolution using honestdns.
            */
            term accept-to-honestdns {
                from {
                    destination-address {
                        /* IPv4 Anycast */
                        8.8.4.4/32;
                        /* IPv4 Anycast */
                        8.8.8.8/32;
                    }
                    protocol udp;
                    destination-port 53;
                }
                then accept;
            }
            /*
            ** Allow what's left.
            */
            term default-permit {
                then accept;
            }
        }
    }
}

...

```

## Capirca resources

- [Multi-Platform ACL Generation and Testing](https://rvasec.com/slides/2013/Watson-Capirca.pdf)
- [Wiki](https://github.com/google/capirca/wiki)

## Port to Service mapping

A good place to start is `/etc/services`.

```python
⇨  cat /etc/services
...
chargen         19/tcp          ttytst source
chargen         19/udp          ttytst source
ftp-data        20/tcp
ftp             21/udp          fsp fspd
ssh             22/tcp                          # The Secure Shell (SSH) Protocol
ssh             22/udp                          # The Secure Shell (SSH) Protocol
telnet          23/tcp
telnet          23/udp
lmtp            24/tcp                          # LMTP Mail Delivery
lmtp            24/udp                          # LMTP Mail Delivery
smtp            25/tcp          mail
smtp            25/udp          mail
time            37/tcp          timserver
...
```