DOCUMENTATION = '''
    name: network
    author:
      - Maximilian Eschenbacher <olrdavey@m.t.kajt.de>
    short_description: lookup capirca definition symbols of type network
    description:
      - Lookup capirca network definition symbols, returning a list of networks
    options:
      _terms:
        description: list of symbols to lookup
        required: true
      def_folder:
        description:
          - Directory where Capirca definitions are stored
          - Search paths are:
            - variable value (def_folder)
            - environment variable value (CAPIRCA_DEF)
            - .capirca-def
            - capirca-acl-def
            - ~/.capirca-def
        type: path
        env:
          - name: CAPIRCA_DEF
      missing:
        description:
          - List of preference about what to do if the symbol is missing.
        type: str
        default: error
        choices:
          - error
          - warn
          - ignore
'''
EXAMPLES = """
tasks.yml: |
  ---

  # lookup one network
  - name: Basic lookup. Fail if the symbol does not exist
    ansible.builtin.debug:
      msg: "{{ lookup('nleiva.capirca_acl.network', 'VLAN_233') }}"

  # lookup more networks
  - name: Basic lookup. Fail if one of the symbols do not exist
    ansible.builtin.debug:
      msg: "{{ lookup('nleiva.capirca_acl.network', 'VLAN_233', 'VLAN_100') }}"

  # lookup more networks
  - name: Basic lookup. Warn if one of the symbols does not exist
    ansible.builtin.debug:
      msg: "{{ lookup('nleiva.capirca_acl.network', 'VLAN_233', 'VLAN_100', missing='warn') }}"
"""

RETURN = """
_raw:
  description:
    - list of networks
  type: list
  elements:
    - capirca.lib.nadaddr.IPv6
    - capirca.lib.nadaddr.IPv4
"""

from .base import CapircaLookup

from capirca.lib import naming

from ansible.errors import AnsibleError
from ansible.utils.display import Display

display = Display()

class LookupModule(CapircaLookup):


    def run(self, args, **kwargs):
        self.setup(*args, **kwargs)
        ret = []
        for symbol in args:
            try:
                for net in self._capirca_definitions.GetNet(symbol):
                    ret.append(str(net))
            except naming.UndefinedAddressError:
                missing = kwargs.get('missing', 'error')
                if missing == 'warn':
                    display.warning('lookup: capirca network: symbol {} not found'.format(symbol))
                elif missing == 'error':
                    raise AnsibleError('lookup: capirca network: symbol {} not found'.format(symbol))
        return ret
