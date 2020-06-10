net_os = "ciscoxr"
name = "testing"

module_args = dict(
        net_os  = dict(type='str', required=True),
        name    = dict(type='str', required=False, default="Default ACL Name"),
        new     = dict(type='bool', required=False, default=False)
    )

module_args['net_os'] = net_os
module_args['name'] = name

from string import Template

header_base = '''
header {
  comment:: "this is a test acl"
  target:: $net_os $name
}
'''

print(module_args)
print(module_args['net_os'])

header = Template(header_base)

print(header.safe_substitute(module_args))