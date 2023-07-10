DOCUMENTATION = '''
    name: service
    author:
      - Maximilian Eschenbacher <olrdavey@m.t.kajt.de>
    short_description: lookup capirca definition symbols of type service
    description:
      - Lookup capirca service definition symbols, returning a list of services
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

  # lookup one service
  - name: Basic lookup. Fail if the symbol does not exist
    ansible.builtin.debug:
      msg: "{{ lookup('nleiva.capirca_acl.service', 'BGP') }}"

  # lookup more services
  - name: Basic lookup. Fail if one of the symbols do not exist
    ansible.builtin.debug:
      msg: "{{ lookup('nleiva.capirca_acl.service', 'BGP', 'DNS') }}"

  # lookup more services
  - name: Basic lookup. Warn if one of the symbols does not exist
    ansible.builtin.debug:
      msg: "{{ lookup('nleiva.capirca_acl.service', 'BGP', 'DNS', missing='warn') }}"
"""

RETURN = """
_raw:
  description:
    - list of services
  type: list
  elements: str
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
                for service in self._capirca_definitions.GetService(symbol):
                    ret.append(service)
            except naming.UndefinedServiceError:
                missing = kwargs.get('missing', 'error')
                if missing == 'warn':
                    display.warning('lookup: capirca service: symbol {} not found'.format(symbol))
                elif missing == 'error':
                    raise AnsibleError('lookup: capirca service: symbol {} not found'.format(symbol))
        return ret
