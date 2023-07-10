import os

from capirca.lib import naming

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

class CapircaLookup(LookupBase):

    def setup(self, *args, **kwargs):
        self._capirca_definitions = None
        for folder in [
                    kwargs.get('def_folder'),
                    os.environ.get('CAPIRCA_DEF'),
                    '.capirca-def',
                    'capirca-acl-def',
                    '~/.capirca-def',
                ]:
            if not folder or not os.path.exists(folder):
                continue
            try:
                self._capirca_definitions = naming.Naming(folder)
            except naming.NoDefinitionsError:
                continue
            break
        if not self._capirca_definitions:
            raise AnsibleError("could not find a valid a capirca definitions folder. Looked in lookup(def_folder=), environment CAPIRCA_DEF, .capirca-def, capirca-acl-def, ~/.capirca-def")
