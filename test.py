from capirca.lib import ciscoxr
from capirca.lib import nacaddr
from capirca.lib import naming
from capirca.lib import policy

GOOD_HEADER_1 = """
header {
  comment:: "this is a test acl"
  target:: ciscoxr test-filter
}
"""

GOOD_TERM_1 = """
term good-term-1 {
  source-address:: SOME_HOST
  protocol:: icmp
  action:: accept
}
"""

EXP_INFO = 2

defs = naming.Naming('./def/')

conf = open('./policies/sample.pol').read()
pol = policy.ParsePolicy(conf, defs, optimize=True)
# pol = policy.ParsePolicy(GOOD_HEADER_1 + GOOD_TERM_1,
#                              self.naming)

acl = ciscoxr.CiscoXR(pol, EXP_INFO)
print(acl)