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
- name: ietf-routing_config
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

  - name: ietf-routing_full
    ietf-routing_config:
      operation_type: config
      routing:
        control-plane-protocols:
          - control-plane-protocol:
              type: "bgp:bgp"
              name: "bgp200"
              bgp:
                global:
                  as: 200
                  afi-safis:
                    - afi-safi:
                        afi-safi-name: "bt:ipv4-unicast"
                        enabled: true
                neighbors:
                  - neighbor:
                      remote-address: "192.0.2.1"
                      enabled: true
                      remote-as: 65550
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:ietf-routing_config
version_added: "2.6"
short_description: This YANG module defines essential components for the management
                   of a routing subsystem. The model fully conforms to the Network
                   Management Datastore Architecture (NMDA).
                   Copyright (c) 2017 IETF Trust and the persons
                   identified as authors of the code.  All rights reserved.
                   Redistribution and use in source and binary forms, with or
                   without modification, is permitted pursuant to, and subject
                   to the license terms contained in, the Simplified BSD License
                   set forth in Section 4.c of the IETF Trust's Legal Provisions
                   Relating to IETF Documents
                   (http://trustee.ietf.org/license-info).
                   This version of this YANG module is part of RFC XXXX; see
                   the RFC itself for full legal notices.
description:
    - This YANG module defines essential components for the management
      of a routing subsystem. The model fully conforms to the Network
      Management Datastore Architecture (NMDA).
      Copyright (c) 2017 IETF Trust and the persons
      identified as authors of the code.  All rights reserved.
      Redistribution and use in source and binary forms, with or
      without modification, is permitted pursuant to, and subject
      to the license terms contained in, the Simplified BSD License
      set forth in Section 4.c of the IETF Trust's Legal Provisions
      Relating to IETF Documents
      (http://trustee.ietf.org/license-info).
      This version of this YANG module is part of RFC XXXX; see
      the RFC itself for full legal notices.
author:ansible_team@huawei
time:2020-10-14 16:47:57
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
                        - Type of the control-plane protocol - an identity derived
                          from the 'control-plane-protocol' base identity.
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
                bgp:
                    description:
                        - Top-level configuration for the BGP router
                    required:False
                    global:
                        description:
                            - Global configuration for the BGP router
                        required:False
                        as:
                            description:
                                - Local autonomous system number of the router.  Uses
                                  the 32-bit as-number type from the model in RFC 6991.
                            required:True
                            mandatory:True
                            type:int
                            range:[(0, 4294967295)]
                        afi-safis:
                            description:
                                - List of address-families associated with the BGP
                                  instance
                            required:False
                            afi-safi:
                                description:
                                    - AFI,SAFI configuration available for the
                                      neighbour or group
                                required:False
                                afi-safi-name:
                                    description:
                                        - AFI,SAFI
                                    required:True
                                    key:True
                                    type:str
                                    length:None
                                enabled:
                                    description:
                                        - This leaf indicates whether the IPv4 Unicast AFI,SAFI is
                                          enabled for the neighbour or group
                                    required:False
                                    default:False
                                    type:bool
                                    choices:['true', 'false']
                    neighbors:
                        description:
                            - Configuration for BGP neighbors
                        required:False
                        neighbor:
                            description:
                                - List of BGP neighbors configured on the local system,
                                  uniquely identified by remote IPv[46] address
                            required:False
                            remote-address:
                                description:
                                    - The remote IP address of this entry's BGP peer.
                                required:True
                                key:True
                                type:str
                                length:None
                            enabled:
                                description:
                                    - Whether the BGP peer is enabled. In cases where the
                                      enabled leaf is set to false, the local system should
                                      not initiate connections to the neighbor, and should
                                      not respond to TCP connections attempts from the
                                      neighbor. If the state of the BGP session is
                                      ESTABLISHED at the time that this leaf is set to false,
                                      the BGP session should be ceased.
                                      A transition from 'false' to 'true' will cause
                                      the BGP Manual Start Event to be generated.
                                      A transition from 'true' to 'false' will cause
                                      the BGP Manual Stop Event to be generated.
                                      This parameter can be used to restart BGP peer
                                      connections. Care should be used in providing
                                      write access to this object without adequate
                                      authentication.
                                required:False
                                default:True
                                type:bool
                                choices:['true', 'false']
                            remote-as:
                                description:
                                    - The remote autonomous system number received in
                                      the BGP OPEN message.
                                required:False
                                type:int
                                range:[(0, 4294967295)]

"""


xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = [
    '/routing/control-plane-protocols/control-plane-protocol/type',
    '/routing/control-plane-protocols/control-plane-protocol/name',
    '/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis/afi-safi/afi-safi-name',
    '/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor/remote-address']

namespaces = [{'/routing': ['',
                            '@xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"',
                            '/routing']},
              {'/routing/control-plane-protocols': ['',
                                                    '',
                                                    '/routing/control-plane-protocols']},
              {'/routing/control-plane-protocols/control-plane-protocol': ['',
                                                                           '',
                                                                           '/routing/control-plane-protocols/control-plane-protocol']},
              {'/routing/control-plane-protocols/control-plane-protocol/type': ['bgp:bgp',
                                                                                '@xmlns:bgp="urn:ietf:params:xml:ns:yang:ietf-bgp"',
                                                                                '/routing/control-plane-protocols/control-plane-protocol/type']},
              {'/routing/control-plane-protocols/control-plane-protocol/name': ['bgp200',
                                                                                '',
                                                                                '/routing/control-plane-protocols/control-plane-protocol/name']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp': ['',
                                                                               '@xmlns="urn:ietf:params:xml:ns:yang:ietf-bgp"',
                                                                               '/routing/control-plane-protocols/control-plane-protocol/bgp']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/global': ['',
                                                                                      '',
                                                                                      '/routing/control-plane-protocols/control-plane-protocol/bgp/global']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors': ['',
                                                                                         '',
                                                                                         '/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/global/as': ['200',
                                                                                         '',
                                                                                         '/routing/control-plane-protocols/control-plane-protocol/bgp/global/as']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis': ['',
                                                                                                '',
                                                                                                '/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor': ['',
                                                                                                  '',
                                                                                                  '/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis/afi-safi': ['',
                                                                                                         '',
                                                                                                         '/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis/afi-safi']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor/remote-address': ['192.0.2.1',
                                                                                                                 '',
                                                                                                                 '/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor/remote-address']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor/enabled': ['true',
                                                                                                          '',
                                                                                                          '/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor/enabled']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor/remote-as': ['65550',
                                                                                                            '',
                                                                                                            '/routing/control-plane-protocols/control-plane-protocol/bgp/neighbors/neighbor/remote-as']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis/afi-safi/afi-safi-name': ['bt:ipv4-unicast',
                                                                                                                       '@xmlns:bt="urn:ietf:params:xml:ns:yang:ietf-bgp-types"',
                                                                                                                       '/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis/afi-safi/afi-safi-name']},
              {'/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis/afi-safi/enabled': ['true',
                                                                                                                 '',
                                                                                                                 '/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis/afi-safi/enabled']}]

business_tag = ['routing']

# Passed to the ansible parameter
argument_spec = OrderedDict([('routing',
                              {'type': 'dict',
                               'options': OrderedDict([('control-plane-protocols',
                                                        {'type': 'list',
                                                         'elements': 'dict',
                                                         'options': OrderedDict([('control-plane-protocol',
                                                                                  {'type': 'dict',
                                                                                   'options': OrderedDict([('type',
                                                                                                            {'type': 'str',
                                                                                                             'required': False}),
                                                                                                           ('name',
                                                                                                            {'type': 'str',
                                                                                                             'required': False}),
                                                                                                           ('bgp',
                                                                                                            {'type': 'dict',
                                                                                                             'options': OrderedDict([('global',
                                                                                                                                      {'type': 'dict',
                                                                                                                                       'options': OrderedDict([('as',
                                                                                                                                                                {'type': 'int',
                                                                                                                                                                 'required': False}),
                                                                                                                                                               ('afi-safis',
                                                                                                                                                                {'type': 'list',
                                                                                                                                                                 'elements': 'dict',
                                                                                                                                                                 'options': OrderedDict([('afi-safi',
                                                                                                                                                                                          {'type': 'dict',
                                                                                                                                                                                           'options': OrderedDict([('afi-safi-name',
                                                                                                                                                                                                                    {'type': 'str',
                                                                                                                                                                                                                     'required': False}),
                                                                                                                                                                                                                   ('enabled',
                                                                                                                                                                                                                    {'type': 'bool',
                                                                                                                                                                                                                     'required': False})])})])})])}),
                                                                                                                                     ('neighbors',
                                                                                                                                      {'type': 'list',
                                                                                                                                       'elements': 'dict',
                                                                                                                                       'options': OrderedDict([('neighbor',
                                                                                                                                                                {'type': 'dict',
                                                                                                                                                                 'options': OrderedDict([('remote-address',
                                                                                                                                                                                          {'type': 'str',
                                                                                                                                                                                           'required': False}),
                                                                                                                                                                                         ('enabled',
                                                                                                                                                                                          {'type': 'bool',
                                                                                                                                                                                           'required': False}),
                                                                                                                                                                                         ('remote-as',
                                                                                                                                                                                          {'type': 'int',
                                                                                                                                                                                           'required': False})])})])})])})])})])})])})])

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
leaf_info = OrderedDict([('routing',
                          OrderedDict([('control-plane-protocols',
                                        OrderedDict([('control-plane-protocol',
                                                      OrderedDict([('type',
                                                                    {'default': None,
                                                                     'key': True,
                                                                     'length': [],
                                                                        'pattern': [],
                                                                        'type': 'string',
                                                                        'required': False}),
                                                                   ('name',
                                                                    {'default': None,
                                                                     'key': True,
                                                                     'length': [],
                                                                     'pattern': [],
                                                                     'type': 'string',
                                                                     'required': False}),
                                                                   ('bgp',
                                                                    OrderedDict([('global',
                                                                                  OrderedDict([('as',
                                                                                                {'default': None,
                                                                                                 'key': False,
                                                                                                 'pattern': [],
                                                                                                 'range': [(0,
                                                                                                            4294967295)],
                                                                                                 'type': 'int',
                                                                                                 'required': False}),
                                                                                               ('afi-safis',
                                                                                                OrderedDict([('afi-safi',
                                                                                                              OrderedDict([('afi-safi-name',
                                                                                                                            {'default': None,
                                                                                                                             'key': True,
                                                                                                                             'length': [],
                                                                                                                             'pattern': [],
                                                                                                                             'type': 'string',
                                                                                                                             'required': False}),
                                                                                                                           ('enabled',
                                                                                                                            {'default': None,
                                                                                                                             'key': False,
                                                                                                                             'type': 'boolean',
                                                                                                                             'pattern': [],
                                                                                                                             'required': False})]))]))])),
                                                                                 ('neighbors',
                                                                                  OrderedDict([('neighbor',
                                                                                                OrderedDict([('remote-address',
                                                                                                              {'default': None,
                                                                                                               'key': True,
                                                                                                               'length': [],
                                                                                                               'pattern': [],
                                                                                                               'type': 'string',
                                                                                                               'required': False}),
                                                                                                             ('enabled',
                                                                                                              {'default': None,
                                                                                                               'key': False,
                                                                                                               'type': 'boolean',
                                                                                                               'pattern': [],
                                                                                                               'required': False}),
                                                                                                             ('remote-as',
                                                                                                              {'default': None,
                                                                                                               'key': False,
                                                                                                               'pattern': [],
                                                                                                               'range': [(0,
                                                                                                                          4294967295)],
                                                                                                               'type': 'int',
                                                                                                               'required': False})]))]))]))]))]))]))])


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
