#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


import sys
from collections import OrderedDict
from ansible.module_utils.network.ne.common_module.ne_base import ConfigBase, GetBase, InputBase
from ansible.module_utils.network.ne.ne import get_nc_config, set_nc_config, ne_argument_spec

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLE = """
---
- name: ietf-interfaces_config
  hosts: ne_test
  connection: netconf
  gather_facts: no
  vars:
    netconf:
      host: "{{ inventory_hostname }}"
      port: "{{ ansible_ssh_port }}"
      username: "{{ ansible_user }}"
      password: "{{ ansible_ssh_pass }}"
      transport: netconf

  tasks:

  - name: ietf-interfaces_full
    ietf-interfaces_config:
      operation_type: config
      interfaces:
        - interface:
            name: "GigabitEthernet 3/0/1"
            type: "ianaift:ethernetCsmacd"
            ipv4:
              - address:
                  ip: "192.0.2.2"
                  prefix-length: 32
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:ietf-interfaces_config
version_added: "2.6"
short_description: This module contains a collection of YANG definitions for
                   managing network interfaces.
                   Copyright (c) 2018 IETF Trust and the persons identified as
                   authors of the code.  All rights reserved.
                   Redistribution and use in source and binary forms, with or
                   without modification, is permitted pursuant to, and subject
                   to the license terms contained in, the Simplified BSD License
                   set forth in Section 4.c of the IETF Trust's Legal Provisions
                   Relating to IETF Documents
                   (http://trustee.ietf.org/license-info).
                   This version of this YANG module is part of RFC XXXX; see
                   the RFC itself for full legal notices.
description:
    - This module contains a collection of YANG definitions for
      managing network interfaces.
      Copyright (c) 2018 IETF Trust and the persons identified as
      authors of the code.  All rights reserved.
      Redistribution and use in source and binary forms, with or
      without modification, is permitted pursuant to, and subject
      to the license terms contained in, the Simplified BSD License
      set forth in Section 4.c of the IETF Trust's Legal Provisions
      Relating to IETF Documents
      (http://trustee.ietf.org/license-info).
      This version of this YANG module is part of RFC XXXX; see
      the RFC itself for full legal notices.
author:ansible_team@huawei
time:2020-10-14 16:47:35
options:
    opreation_type:config
        description:config
            - This is a helper node ,Choose from config, get
        type: str
        required:True
        chioces: ["config","get","get-config"]
    interfaces:
        description:
            - Interface parameters.
        required:False
        interface:
            description:
                - The list of interfaces on the device.
                  The status of an interface is available in this list in the
                  operational state.  If the configuration of a
                  system-controlled interface cannot be used by the system
                  (e.g., the interface hardware present does not match the
                  interface type), then the configuration is not applied to
                  the system-controlled interface shown in the operational
                  state.  If the configuration of a user-controlled interface
                  cannot be used by the system, the configured interface is
                  not instantiated in the operational state.
                  System-controlled interfaces created by the system are
                  always present in this list in the operational state,
                  whether they are configured or not.
            required:False
            name:
                description:
                    - The name of the interface.
                      A device MAY restrict the allowed values for this leaf,
                      possibly depending on the type of the interface.
                      For system-controlled interfaces, this leaf is the
                      device-specific name of the interface.
                      If a client tries to create configuration for a
                      system-controlled interface that is not present in the
                      operational state, the server MAY reject the request if
                      the implementation does not support pre-provisioning of
                      interfaces or if the name refers to an interface that can
                      never exist in the system.  A NETCONF server MUST reply
                      with an rpc-error with the error-tag 'invalid-value' in
                      this case.
                      If the device supports pre-provisioning of interface
                      configuration, the 'pre-provisioning' feature is
                      advertised.
                      If the device allows arbitrarily named user-controlled
                      interfaces, the 'arbitrary-names' feature is advertised.
                      When a configured user-controlled interface is created by
                      the system, it is instantiated with the same name in the
                      operational state.
                      A server implementation MAY map this leaf to the ifName
                      MIB object.  Such an implementation needs to use some
                      mechanism to handle the differences in size and characters
                      allowed between this leaf and ifName.  The definition of
                      such a mechanism is outside the scope of this document.
                required:True
                key:True
                type:str
            type:
                description:
                    - The type of the interface.
                      When an interface entry is created, a server MAY
                      initialize the type leaf with a valid value, e.g., if it
                      is possible to derive the type from the name of the
                      interface.
                      If a client tries to set the type of an interface to a
                      value that can never be used by the system, e.g., if the
                      type is not supported or if the type does not match the
                      name of the interface, the server MUST reject the request.
                      A NETCONF server MUST reply with an rpc-error with the
                      error-tag 'invalid-value' in this case.
                required:True
                mandatory:True
                type:str
                length:None
            ipv4:
                description:
                    - Parameters for the IPv4 address family.
                required:False
                address:
                    description:
                        - The list of IPv4 addresses on the interface.
                    required:False
                    ip:
                        description:
                            - The IPv4 address on the interface.
                        required:True
                        key:True
                        pattern:['[0-9\\.]*']
                        type:str
                    prefix-length:
                        description:
                            - The length of the subnet prefix.
                        required:True
                        type:int
                        range:[(0, 32)]

"""


xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/interfaces/interface/name',
            '/interfaces/interface/ipv4/address/ip']

namespaces = [{'/interfaces': ['',
                               '@xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"',
                               '/interfaces']},
              {'/interfaces/interface': ['',
                                         '',
                                         '/interfaces/interface']},
              {'/interfaces/interface/name': ['GigabitEthernet 3/0/1',
                                              '',
                                              '/interfaces/interface/name']},
              {'/interfaces/interface/type': ['ianaift:ethernetCsmacd',
                                              '@xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type"',
                                              '/interfaces/interface/type']},
              {'/interfaces/interface/ipv4': ['',
                                              '@xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"',
                                              '/interfaces/interface/ipv4']},
              {'/interfaces/interface/ipv4/address': ['',
                                                      '@xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"',
                                                      '/interfaces/interface/ipv4/address']},
              {'/interfaces/interface/ipv4/address/ip': ['192.0.2.2',
                                                         '',
                                                         '/interfaces/interface/ipv4/address/ip']},
              {'/interfaces/interface/ipv4/address/prefix-length': ['32',
                                                                    '',
                                                                    '/interfaces/interface/ipv4/address/prefix-length']}]

business_tag = ['interfaces']

# Passed to the ansible parameter
argument_spec = OrderedDict([('interfaces',
                              {'type': 'list',
                               'elements': 'dict',
                               'options': OrderedDict([('interface',
                                                        {'type': 'dict',
                                                         'options': OrderedDict([('name',
                                                                                  {'type': 'str',
                                                                                   'required': False}),
                                                                                 ('type',
                                                                                  {'type': 'str',
                                                                                   'required': False}),
                                                                                 ('ipv4',
                                                                                  {'type': 'list',
                                                                                   'elements': 'dict',
                                                                                   'options': OrderedDict([('address',
                                                                                                            {'type': 'dict',
                                                                                                             'options': OrderedDict([('ip',
                                                                                                                                      {'type': 'str',
                                                                                                                                       'required': False}),
                                                                                                                                     ('prefix-length',
                                                                                                                                      {'type': 'int',
                                                                                                                                       'required': False})])})])})])})])})])

# Operation type
operation_dict = {
    'operation_type': {
        'type': 'str',
        'required': True,
        'choices': [
            'config',
            'get',
            'get-config',
            'rpc']},
    'operation_specs': {
        'elements': 'dict',
        'type': 'list',
                'options': {
                    'path': {
                        'type': 'str'},
                    'operation': {
                        'choices': [
                            'merge',
                            'replace',
                            'create',
                            'delete',
                            'remove'],
                        'default': 'merge'}}}}

# Parameters passed to check params
leaf_info = OrderedDict([('interfaces',
                          OrderedDict([('interface',
                                        OrderedDict([('name',
                                                      {'default': None,
                                                       'key': True,
                                                       'length': [],
                                                          'pattern': [],
                                                          'type': 'string',
                                                          'required': False}),
                                                     ('type',
                                                      {'default': None,
                                                       'key': False,
                                                       'length': [],
                                                       'pattern': [],
                                                       'type': 'string',
                                                       'required': False}),
                                                     ('ipv4',
                                                      OrderedDict([('address',
                                                                    OrderedDict([('ip',
                                                                                  {'default': None,
                                                                                   'key': True,
                                                                                   'length': [],
                                                                                   'pattern': ['[0-9\\.]*'],
                                                                                   'type': 'string',
                                                                                   'required': False}),
                                                                                 ('prefix-length',
                                                                                  {'default': None,
                                                                                   'key': False,
                                                                                   'pattern': [],
                                                                                   'range': [(0,
                                                                                              32)],
                                                                                   'type': 'int',
                                                                                   'required': False})]))]))]))]))])


# User check params
class UserCheck(object):
    def __init__(self, params, infos):
        #  user configuration get from AnsibleModule().params
        self.params = params
        # leaf infos from yang files
        self.infos = infos

    # user defined check method need startswith "check_"
    # return 0 if not pass check logic, else 1
    def check_leaf_restrict(self):
        """
            if leaf_1 configured, leaf2 shouble be configured
            and range shouble be in [10, 20]
        """
        return 1


# Call the ConfigBase base class
def config_base(config_args):
    class_object = ConfigBase(*config_args)
    class_object.run()


# Call the GetBase base class
def get_base(get_args):
    class_object = GetBase(*get_args)
    class_object.run()


def input_base(input_args):
    class_object = InputBase(*input_args)
    class_object.run()


# According to the type of message
def operation(operation_type, args):
    if operation_type == 'config':
        config_base(args)
    elif operation_type == 'get' or operation_type == 'get-config':
        get_base(args)
    else:
        input_base(args)


def filter_check(user_check_obj):
    return (
        list(
            filter(
                lambda m: m.startswith("check_"), [
                    i + '()' for i in dir(user_check_obj)])))


def main():
    """Module main"""
    argument_spec.update(ne_argument_spec)
    argument_spec.update(operation_dict)
    args = (
        argument_spec,
        leaf_info,
        namespaces,
        business_tag,
        xml_head,
        xml_tail,
        key_list)
    module_params = ConfigBase(*args).get_operation_type()
    for check_func in filter_check(UserCheck):
        if not eval('UserCheck(module_params, leaf_info).' + check_func):
            ConfigBase(
                *
                args).init_module().fail_json(
                msg='UserCheck.' +
                check_func)
    operation(module_params['operation_type'], args)


if __name__ == '__main__':
    main()
