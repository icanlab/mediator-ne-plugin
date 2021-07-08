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
from ansible.module_utils.network.ne.common_module.ne_base import ConfigBase,GetBase, InputBase
from ansible.module_utils.network.ne.ne import get_nc_config, set_nc_config, ne_argument_spec

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLE = """
---
- name: ietf_isis
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

  - name: IETF_105_isis_full
    ietf_isis:
      operation_type: config
      routing: 
        control-plane-protocols: 
          - control-plane-protocol: 
              type: "isis"
              name: "is-is-1"
              isis: 
                enable: true
                level-type: level-2
                system-id: "1111.1111.1111"
                area-address: "00"
                srv6-cfg: 
                  enable: true
                  default-locator: false
                  locator-name: "test"
                  persistent-end-x-sid: true
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:ietf_isis
version_added: "2.6"
short_description: This YANG module defines essential components for the management
                   of a routing subsystem.  The model fully conforms to the Network
                   Management Datastore Architecture (NMDA).
                   Copyright (c) 2018 IETF Trust and the persons
                   identified as authors of the code.  All rights reserved.
                   Redistribution and use in source and binary forms, with or
                   without modification, is permitted pursuant to, and subject
                   to the license terms contained in, the Simplified BSD License
                   set forth in Section 4.c of the IETF Trust's Legal Provisions
                   Relating to IETF Documents
                   (https://trustee.ietf.org/license-info).
                   This version of this YANG module is part of RFC 8349; see
                   the RFC itself for full legal notices.
description:
    - This YANG module defines essential components for the management
      of a routing subsystem.  The model fully conforms to the Network
      Management Datastore Architecture (NMDA).
      Copyright (c) 2018 IETF Trust and the persons
      identified as authors of the code.  All rights reserved.
      Redistribution and use in source and binary forms, with or
      without modification, is permitted pursuant to, and subject
      to the license terms contained in, the Simplified BSD License
      set forth in Section 4.c of the IETF Trust's Legal Provisions
      Relating to IETF Documents
      (https://trustee.ietf.org/license-info).
      This version of this YANG module is part of RFC 8349; see
      the RFC itself for full legal notices.
author:ansible_team@huawei
time:2021-07-08 10:08:26
options:
    opreation_type:config
        description:config
            - This is a helper node ,Choose from config, get
        type: str
        required:True
        chioces: ["config","get","get-config"]
    routing:
        description:
            - Configuration parameters for the routing subsystem.
        required:False
        control-plane-protocols:
            description:
                - Support for control-plane protocol instances.
            required:False
            control-plane-protocol:
                description:
                    - Each entry contains a control-plane protocol instance.
                required:False
                type:
                    description:
                        - Type of the control-plane protocol -- an identity
                          derived from the 'control-plane-protocol'
                          base identity.
                    required:True
                    key:True
                    type:str
                    length:None
                name:
                    description:
                        - An arbitrary name of the control-plane protocol
                          instance.
                    required:True
                    key:True
                    type:str
                isis:
                    description:
                        - IS-IS configuration/state top-level container
                    must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                    required:False
                    enable:
                        description:
                            - Enable/Disable the protocol.
                        required:False
                        default:True
                        type:bool
                        choices:['true', 'false']
                    level-type:
                        description:
                            - Level of an IS-IS node - can be level-1,
                              level-2 or level-all.
                        required:False
                        default:level-all
                        type:enum
                        choices:['level-1', 'level-2', 'level-all']
                    system-id:
                        description:
                            - system-id of the node.
                        required:False
                        pattern:['[0-9A-Fa-f]{4}\\.[0-9A-Fa-f]{4}\\.[0-9A-Fa-f]{4}']
                        type:str
                    area-address:
                        description:
                            - List of areas supported by the protocol instance.
                        required:False
                        pattern:['[0-9A-Fa-f]{2}(\\.[0-9A-Fa-f]{4}){0,6}']
                        type:str
                    srv6-cfg:
                        description:
                            - Configuration about ISIS segment-routing IPv6.
                        required:False
                        enable:
                            description:
                                - Enables SRv6
                                  protocol extensions.
                            required:False
                            default:False
                            type:bool
                            choices:['true', 'false']
                        default-locator:
                            description:
                                - Enable ISIS segment-routing IPv6 with default Locator.
                            required:False
                            default:False
                            type:bool
                            choices:['true', 'false']
                        locator-name:
                            description:
                                - Enable ISIS segment-routing IPv6 with specified Locator.
                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                            required:False
                            type:str
                        persistent-end-x-sid:
                            description:
                                - Enable the persistent nature of End.X sid
                            required:False
                            default:False
                            type:bool
                            choices:['true', 'false']

"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/routing/control-plane-protocols/control-plane-protocol/type', '/routing/control-plane-protocols/control-plane-protocol/name']

namespaces = [{'/routing': ['', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"', '/routing']}, {'/routing/control-plane-protocols': ['', '', '/routing/control-plane-protocols']}, {'/routing/control-plane-protocols/control-plane-protocol': ['', '', '/routing/control-plane-protocols/control-plane-protocol']}, {'/routing/control-plane-protocols/control-plane-protocol/type': ['isis', '', '/routing/control-plane-protocols/control-plane-protocol/type']}, {'/routing/control-plane-protocols/control-plane-protocol/name': ['is-is-1', '', '/routing/control-plane-protocols/control-plane-protocol/name']}, {'/routing/control-plane-protocols/control-plane-protocol/isis': ['', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-isis"', '/routing/control-plane-protocols/control-plane-protocol/isis']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/enable': ['true', '', '/routing/control-plane-protocols/control-plane-protocol/isis/enable']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/level-type': ['level-2', '', '/routing/control-plane-protocols/control-plane-protocol/isis/level-type']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/system-id': ['1111.1111.1111', '', '/routing/control-plane-protocols/control-plane-protocol/isis/system-id']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/area-address': ['00', '', '/routing/control-plane-protocols/control-plane-protocol/isis/area-address']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg': ['', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-isis-srv6"', '/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg/enable': ['true', '', '/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg/enable']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg/default-locator': ['false', '', '/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg/default-locator']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg/locator-name': ['test', '', '/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg/locator-name']}, {'/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg/persistent-end-x-sid': ['true', '', '/routing/control-plane-protocols/control-plane-protocol/isis/srv6-cfg/persistent-end-x-sid']}]

business_tag = ['routing']

# Passed to the ansible parameter
argument_spec = OrderedDict([('routing', {'type': 'dict', 'options': OrderedDict([('control-plane-protocols', {'type': 'list', 'options': OrderedDict([('control-plane-protocol', {'type': 'dict', 'options': OrderedDict([('type', {'type': 'str', 'required': False}), ('name', {'type': 'str', 'required': False}), ('isis', {'type': 'dict', 'options': OrderedDict([('enable', {'type': 'bool', 'required': False}), ('level-type', {'required': False, 'choices': ['level-1', 'level-2', 'level-all']}), ('system-id', {'type': 'str', 'required': False}), ('area-address', {'type': 'str', 'required': False}), ('srv6-cfg', {'type': 'dict', 'options': OrderedDict([('enable', {'type': 'bool', 'required': False}), ('default-locator', {'type': 'bool', 'required': False}), ('locator-name', {'type': 'str', 'required': False}), ('persistent-end-x-sid', {'type': 'bool', 'required': False})])})])})])})]), 'elements': 'dict'})])})])

# Operation type
operation_dict = {'operation_type':{'type': 'str', 'required':True, 'choices': ['config','get','get-config','rpc']},
                  'operation_specs': {
                      'elements': 'dict', 'type': 'list','options': {
                          'path': {
                              'type': 'str'}, 'operation': {
                              'choices': ['merge', 'replace', 'create', 'delete', 'remove'],'default':'merge'}}}}

# Parameters passed to check params
leaf_info =  OrderedDict([('routing', OrderedDict([('control-plane-protocols', OrderedDict([('control-plane-protocol', OrderedDict([('type', {
                'default': None, 
                'pattern': [], 
                'type': 'string', 'required': False, 'length': [], 
                'key': True}), 
            ('name', {
                'default': None, 
                'pattern': [], 
                'type': 'string', 'required': False, 'length': [], 
                'key': True}), 
            ('isis', OrderedDict([('enable', {
                'default': None, 'required': False, 'key': False, 
                'pattern': [], 
                'type': 'boolean'}), 
            ('level-type', {
                'default': None, 
                'pattern': [], 
                'type': 'enumeration', 'required': False, 'choices': ['level-1', 'level-2', 'level-all'], 
                'key': False}), 
            ('system-id', {
                'default': None, 
                'pattern': ['[0-9A-Fa-f]{4}\\.[0-9A-Fa-f]{4}\\.[0-9A-Fa-f]{4}'], 
                'type': 'string', 'required': False, 'length': [], 
                'key': False}), 
            ('area-address', {
                'default': None, 
                'pattern': ['[0-9A-Fa-f]{2}(\\.[0-9A-Fa-f]{4}){0,6}'], 
                'type': 'string', 'required': False, 'length': [], 
                'key': False}), 
            ('srv6-cfg', OrderedDict([('enable', {
                'default': None, 'required': False, 'key': False, 
                'pattern': [], 
                'type': 'boolean'}), 
            ('default-locator', {
                'default': None, 'required': False, 'key': False, 
                'pattern': [], 
                'type': 'boolean'}), 
            ('locator-name', {
                'default': None, 
                'pattern': [], 
                'type': 'string', 'required': False, 'length': [], 
                'key': False}), 
            ('persistent-end-x-sid', {
                'default': None, 'required': False, 'key': False, 
                'pattern': [], 
                'type': 'boolean'})]))]))]))]))]))])


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
def operation(operation_type,args):
    if operation_type == 'config':
        config_base(args)
    elif operation_type == 'get' or operation_type == 'get-config':
        get_base(args)
    else:
        input_base(args)


def filter_check(user_check_obj):
    return (list(
        filter(lambda m: m.startswith("check_"), [i + '()' for i in dir(user_check_obj)])))


def main():
    """Module main"""
    argument_spec.update(ne_argument_spec)
    argument_spec.update(operation_dict)
    args = (argument_spec, leaf_info, namespaces, business_tag, xml_head,xml_tail,key_list)
    module_params = ConfigBase(*args).get_operation_type()
    for check_func in filter_check(UserCheck):
        if not eval('UserCheck(module_params, leaf_info).' + check_func):
            ConfigBase(*args).init_module().fail_json(msg='UserCheck.'+ check_func)
    operation(module_params['operation_type'], args)


if __name__ == '__main__':
    main()
