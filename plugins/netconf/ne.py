#
# (c) 2017 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
netconf: ne
short_description: Use ne netconf plugin to run netconf commands on Huawei NetEngine platform
description:
  - This ne plugin provides low level abstraction apis for
    sending and receiving netconf commands from Huawei NetEngine network devices.
version_added: "2.9"
options:
  ncclient_device_handler:
    type: str
    default: huaweiyang
    description:
      - Specifies the ncclient device handler name for Huawei NetEngine.
        To identify the ncclient device handler name refer ncclient library documentation.
"""

import json
import re

from ansible import constants as C
from ansible.module_utils._text import to_text, to_bytes
from ansible.errors import AnsibleConnectionFailure, AnsibleError
from ansible.plugins.netconf import NetconfBase, ensure_ncclient

try:
    from ncclient import manager
    from ncclient.operations import RPCError
    from ncclient.transport.errors import SSHUnknownHostError
    from ncclient.xml_ import to_ele, to_xml, new_ele, sub_ele
except ImportError:
    raise AnsibleError("ncclient is not installed")


class Netconf(NetconfBase):

    @ensure_ncclient
    def get_text(self, ele, tag):
        try:
            return to_text(ele.find(tag).text, errors='surrogate_then_replace').strip()
        except AttributeError:
            pass

    @ensure_ncclient
    def get_device_info(self):
        device_info = dict()
        device_info['network_os'] = 'ne'
        return device_info

    def execute_rpc(self, name):
        """RPC to be execute on remote device
           :name: Name of rpc in string format"""
        return self.rpc(name)

    @ensure_ncclient
    def load_configuration(self, *args, **kwargs):
        """Loads given configuration on device
        :format: Format of configuration (xml, text, set)
        :action: Action to be performed (merge, replace, override, update)
        :target: is the name of the configuration datastore being edited
        :config: is the configuration in string format."""
        if kwargs.get('config'):
            kwargs['config'] = to_bytes(kwargs['config'], errors='surrogate_or_strict')
            if kwargs.get('format', 'xml') == 'xml':
                kwargs['config'] = to_ele(kwargs['config'])

        try:
            return self.m.load_configuration(*args, **kwargs).data_xml
        except RPCError as exc:
            raise Exception(to_xml(exc.xml))

    def get_capabilities(self):
        result = dict()
        result['rpc'] = self.get_base_rpc() + ['commit', 'discard_changes', 'lock',
                                               'unlock', 'execute_rpc', 'command', 'get', 'get_config', 'edit_config', 'copy_config']
        result['network_api'] = 'netconf'
        result['device_info'] = self.get_device_info()
        result['server_capabilities'] = [c for c in self.m.server_capabilities]
        result['client_capabilities'] = [c for c in self.m.client_capabilities]
        result['session_id'] = self.m.session_id
        result['device_operations'] = self.get_device_operations(result['server_capabilities'])
        return json.dumps(result)

    @staticmethod
    @ensure_ncclient
    def guess_network_os(obj):

        try:
            m = manager.connect(
                host=obj._play_context.remote_addr,
                port=obj._play_context.port or 830,
                username=obj._play_context.remote_user,
                password=obj._play_context.password,
                key_filename=obj._play_context.private_key_file,
                hostkey_verify=C.HOST_KEY_CHECKING,
                look_for_keys=C.PARAMIKO_LOOK_FOR_KEYS,
                allow_agent=obj._play_context.allow_agent,
                timeout=obj._play_context.timeout
            )
        except SSHUnknownHostError as exc:
            raise AnsibleConnectionFailure(str(exc))

        guessed_os = None
        for c in m.server_capabilities:
            if re.search('huawei', c):
                guessed_os = 'ne'

        m.close_session()
        return guessed_os

    # Due to issue in ncclient commit() method for Juniper (https://github.com/ncclient/ncclient/issues/238)
    # below commit() is a workaround which build's raw `commit-configuration` xml with required tags and uses
    # ncclient generic rpc() method to execute rpc on remote host.
    # Remove below method after the issue in ncclient is fixed.
    @ensure_ncclient
    def commit(self, confirmed=False, check=False, timeout=None, comment=None, synchronize=False, at_time=None):
        """Commit the candidate configuration as the device's new current configuration.
           Depends on the `:candidate` capability.
           A confirmed commit (i.e. if *confirmed* is `True`) is reverted if there is no
           followup commit within the *timeout* interval. If no timeout is specified the
           confirm timeout defaults to 600 seconds (10 minutes).
           A confirming commit may have the *confirmed* parameter but this is not required.
           Depends on the `:confirmed-commit` capability.
        :confirmed: whether this is a confirmed commit
        :timeout: specifies the confirm timeout in seconds
        """
        obj = new_ele('commit-configuration')
        if confirmed:
            sub_ele(obj, 'confirmed')
        if check:
            sub_ele(obj, 'check')
        if synchronize:
            sub_ele(obj, 'synchronize')
        if at_time:
            subele = sub_ele(obj, 'at-time')
            subele.text = str(at_time)
        if comment:
            subele = sub_ele(obj, 'log')
            subele.text = str(comment)
        if timeout:
            subele = sub_ele(obj, 'confirm-timeout')
            subele.text = str(timeout)
        return self.rpc(obj)
