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
- name: ietf_srv6
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

  - name: IETF_105_srv6_full
    ietf_srv6:
      operation_type: config
      routing: 
        srv6: 
          enable: true
          encapsulation: 
            source-address: "A1::123"
            ip-ttl-propagation: 1
          locators: 
            - locator: 
                name: "test1"
                enable: true
                is-default: true
                prefix: 
                  address: "A2::123"
                  length: 64
                static: 
                  local-sids: 
                    - sid: 
                        opcode: 65
                        end-behavior-type: "End"
                        end-dt4: 
                          lookup-table-ipv4: 100
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:ietf_srv6
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
time:2021-07-08 10:08:25
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
        srv6:
            description:
                - Segment Routing with IPv6 dataplane
            required:False
            enable:
                description:
                    - Enable SRv6
                required:False
                default:False
                type:bool
                choices:['true', 'false']
            encapsulation:
                description:
                    - Configure encapsulation related parameters
                required:False
                source-address:
                    description:
                        - Specify a source address (for T.Encap). The address must locally exists
                          and be routable
                    required:False
                    pattern:['((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\p{N}\\p{L}]+)?', '(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?']
                    type:str
                ip-ttl-propagation:
                    description:
                        - IP TTL propagation from encapsulated packet to encapsulating outer
                          IPv6 header. When configured on decapsulation side, this refers to
                          propagating IP TTL from outer IPv6 header to inner header after decap
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
            locators:
                description:
                    - SRv6 locators
                required:False
                locator:
                    description:
                        - Configure a SRv6 locator
                    required:False
                    name:
                        description:
                            - Locator name
                        required:True
                        key:True
                        type:str
                    enable:
                        description:
                            - Enable a SRv6 locator
                        required:False
                        default:False
                        type:bool
                        choices:['true', 'false']
                    is-default:
                        description:
                            - Indicates if the locator is a default locator
                        required:True
                        mandatory:True
                        type:bool
                        choices:['true', 'false']
                    prefix:
                        description:
                            - Specify locator prefix value
                        required:False
                        address:
                            description:
                                - IPv6 address
                            required:True
                            mandatory:True
                            pattern:['((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\p{N}\\p{L}]+)?', '(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?']
                            type:str
                        length:
                            description:
                                - Locator (prefix) length
                            required:True
                            mandatory:True
                            type:int
                            range:[(32, 96)]
                    static:
                        description:
                            - Static SRv6
                        required:False
                        local-sids:
                            description:
                                - SRv6-static local-SIDs
                            required:False
                            sid:
                                description:
                                    - Local SID list
                                required:False
                                opcode:
                                    description:
                                        - SRv6 function opcode.
                                    required:True
                                    key:True
                                    type:int
                                    range:[(64, 4294967295)]
                                end-behavior-type:
                                    description:
                                        - Type of SRv6 end behavior.
                                    required:True
                                    mandatory:True
                                    type:str
                                    length:None
                                end-dt4:
                                    description:
                                        - Endpoint with decapsulation and specific
                                          IPv4 table lookup.
                                          Pop the (outer) IPv6 header and its extension
                                          headers.
                                          Lookup the exposed inner IPv4 DA in IPv4
                                          table T and forward via the matched table entry.
                                          This would be equivalent to the per-VRF VPN label
                                          in MPLS.
                                    when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                    required:False
                                    lookup-table-ipv4:
                                        description:
                                            - IPv4 table
                                        required:True
                                        mandatory:True
                                        type:int
                                        range:[(0, 4294967295)]

"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/routing/srv6/locators/locator/name', '/routing/srv6/locators/locator/static/local-sids/sid/opcode']

namespaces = [{'/routing': ['', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"', '/routing']}, {'/routing/srv6': ['', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-srv6-base"', '/routing/srv6']}, {'/routing/srv6/enable': ['true', '', '/routing/srv6/enable']}, {'/routing/srv6/encapsulation': ['', '', '/routing/srv6/encapsulation']}, {'/routing/srv6/locators': ['', '', '/routing/srv6/locators']}, {'/routing/srv6/encapsulation/source-address': ['A1::123', '', '/routing/srv6/encapsulation/source-address']}, {'/routing/srv6/encapsulation/ip-ttl-propagation': ['1', '', '/routing/srv6/encapsulation/ip-ttl-propagation']}, {'/routing/srv6/locators/locator': ['', '', '/routing/srv6/locators/locator']}, {'/routing/srv6/locators/locator/name': ['test1', '', '/routing/srv6/locators/locator/name']}, {'/routing/srv6/locators/locator/enable': ['true', '', '/routing/srv6/locators/locator/enable']}, {'/routing/srv6/locators/locator/is-default': ['true', '', '/routing/srv6/locators/locator/is-default']}, {'/routing/srv6/locators/locator/prefix': ['', '', '/routing/srv6/locators/locator/prefix']}, {'/routing/srv6/locators/locator/static': ['', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-srv6-static"', '/routing/srv6/locators/locator/static']}, {'/routing/srv6/locators/locator/prefix/address': ['A2::123', '', '/routing/srv6/locators/locator/prefix/address']}, {'/routing/srv6/locators/locator/prefix/length': ['64', '', '/routing/srv6/locators/locator/prefix/length']}, {'/routing/srv6/locators/locator/static/local-sids': ['', '', '/routing/srv6/locators/locator/static/local-sids']}, {'/routing/srv6/locators/locator/static/local-sids/sid': ['', '', '/routing/srv6/locators/locator/static/local-sids/sid']}, {'/routing/srv6/locators/locator/static/local-sids/sid/opcode': ['65', '', '/routing/srv6/locators/locator/static/local-sids/sid/opcode']}, {'/routing/srv6/locators/locator/static/local-sids/sid/end-behavior-type': ['End', '', '/routing/srv6/locators/locator/static/local-sids/sid/end-behavior-type']}, {'/routing/srv6/locators/locator/static/local-sids/sid/end-dt4': ['', '', '/routing/srv6/locators/locator/static/local-sids/sid/end-dt4']}, {'/routing/srv6/locators/locator/static/local-sids/sid/end-dt4/lookup-table-ipv4': ['100', '', '/routing/srv6/locators/locator/static/local-sids/sid/end-dt4/lookup-table-ipv4']}]

business_tag = ['routing']

# Passed to the ansible parameter
argument_spec = OrderedDict([('routing', {'type': 'dict', 'options': OrderedDict([('srv6', {'type': 'dict', 'options': OrderedDict([('enable', {'type': 'bool', 'required': False}), ('encapsulation', {'type': 'dict', 'options': OrderedDict([('source-address', {'type': 'str', 'required': False}), ('ip-ttl-propagation', {'type': 'bool', 'required': False})])}), ('locators', {'type': 'list', 'options': OrderedDict([('locator', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': False}), ('enable', {'type': 'bool', 'required': False}), ('is-default', {'type': 'bool', 'required': False}), ('prefix', {'type': 'dict', 'options': OrderedDict([('address', {'type': 'str', 'required': False}), ('length', {'type': 'int', 'required': False})])}), ('static', {'type': 'dict', 'options': OrderedDict([('local-sids', {'type': 'list', 'options': OrderedDict([('sid', {'type': 'dict', 'options': OrderedDict([('opcode', {'type': 'int', 'required': False}), ('end-behavior-type', {'type': 'str', 'required': False}), ('end-dt4', {'type': 'dict', 'options': OrderedDict([('lookup-table-ipv4', {'type': 'int', 'required': False})])})])})]), 'elements': 'dict'})])})])})]), 'elements': 'dict'})])})])})])

# Operation type
operation_dict = {'operation_type':{'type': 'str', 'required':True, 'choices': ['config','get','get-config','rpc']},
                  'operation_specs': {
                      'elements': 'dict', 'type': 'list','options': {
                          'path': {
                              'type': 'str'}, 'operation': {
                              'choices': ['merge', 'replace', 'create', 'delete', 'remove'],'default':'merge'}}}}

# Parameters passed to check params
leaf_info =  OrderedDict([('routing', OrderedDict([('srv6', OrderedDict([('enable', {
                'default': None, 'required': False, 'key': False, 
                'pattern': [], 
                'type': 'boolean'}), 
            ('encapsulation', OrderedDict([('source-address', {
                'default': None, 
                'pattern': ['((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\p{N}\\p{L}]+)?', '(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?'], 
                'type': 'string', 'required': False, 'length': [], 
                'key': False}), 
            ('ip-ttl-propagation', {
                'default': None, 'required': False, 'key': False, 
                'pattern': [], 
                'type': 'boolean'})])), 
            ('locators', OrderedDict([('locator', OrderedDict([('name', {
                'default': None, 
                'pattern': [], 
                'type': 'string', 'required': False, 'length': [], 
                'key': True}), 
            ('enable', {
                'default': None, 'required': False, 'key': False, 
                'pattern': [], 
                'type': 'boolean'}), 
            ('is-default', {
                'default': None, 'required': False, 'key': False, 
                'pattern': [], 
                'type': 'boolean'}), 
            ('prefix', OrderedDict([('address', {
                'default': None, 
                'pattern': ['((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\p{N}\\p{L}]+)?', '(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?'], 
                'type': 'string', 'required': False, 'length': [], 
                'key': False}), 
            ('length', {
                'default': None, 
                'pattern': [], 
                'type': 'int', 'range': [(32, 96)], 
                'required': False, 'key': False})])), 
            ('static', OrderedDict([('local-sids', OrderedDict([('sid', OrderedDict([('opcode', {
                'default': None, 
                'pattern': [], 
                'type': 'int', 'range': [(64, 4294967295)], 
                'required': False, 'key': True}), 
            ('end-behavior-type', {
                'default': None, 
                'pattern': [], 
                'type': 'string', 'required': False, 'length': [], 
                'key': False}), 
            ('end-dt4', OrderedDict([('lookup-table-ipv4', {
                'default': None, 
                'pattern': [], 
                'type': 'int', 'range': [(0, 4294967295)], 
                'required': False, 'key': False})]))]))]))]))]))]))]))]))])


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
