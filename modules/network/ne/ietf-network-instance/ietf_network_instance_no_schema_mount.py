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

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

EXAMPLE = """
---
- name: ietf_network_instance_no_schema_mount
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

  - name: ietf-network-instance-no_schema_mount_full
    ietf_network_instance_no_schema_mount:
      operation_type: config
      routing: 
        router-id: "192.0.2.1"
        control-plane-protocols: 
          - control-plane-protocol: 
              type: "ospf"
              name: "1"
              ospf: 
                areas: 
                  - area: 
                      area-id: "203.0.113.1"
                      interfaces: 
                        - interface: 
                            name: "eth1"
                            cost: 10
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
None
"""

xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = [
    '/routing/control-plane-protocols/control-plane-protocol/type',
    '/routing/control-plane-protocols/control-plane-protocol/name',
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/area-id',
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces/interface/name'
]

namespaces = [{
    '/routing':
    ['', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"', '/routing']
}, {
    '/routing/router-id': ['192.0.2.1', '', '/routing/router-id']
}, {
    '/routing/control-plane-protocols':
    ['', '', '/routing/control-plane-protocols']
}, {
    '/routing/control-plane-protocols/control-plane-protocol':
    ['', '', '/routing/control-plane-protocols/control-plane-protocol']
}, {
    '/routing/control-plane-protocols/control-plane-protocol/type': [
        'ospf', '',
        '/routing/control-plane-protocols/control-plane-protocol/type'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/name':
    ['1', '', '/routing/control-plane-protocols/control-plane-protocol/name']
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf': [
        '', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-ospf"',
        '/routing/control-plane-protocols/control-plane-protocol/ospf'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf/address_family':
    [
        'ipv4', '',
        '/routing/control-plane-protocols/control-plane-protocol/ospf/address_family'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas': [
        '', '',
        '/routing/control-plane-protocols/control-plane-protocol/ospf/areas'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area':
    [
        '', '',
        '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/area-id':
    [
        '203.0.113.1', '',
        '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/area-id'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces':
    [
        '', '',
        '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces/interface':
    [
        '', '',
        '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces/interface'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces/interface/name':
    [
        'eth1', '',
        '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces/interface/name'
    ]
}, {
    '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces/interface/cost':
    [
        '10', '',
        '/routing/control-plane-protocols/control-plane-protocol/ospf/areas/area/interfaces/interface/cost'
    ]
}]

business_tag = ['routing']

# Passed to the ansible parameter
argument_spec = OrderedDict([('routing', {
    'options':
    OrderedDict([('router-id', {
        'required': False,
        'type': 'str'
    }),
                 ('control-plane-protocols', {
                     'elements':
                     'dict',
                     'options':
                     OrderedDict([('control-plane-protocol', {
                         'options':
                         OrderedDict([
                             ('type', {
                                 'required': False,
                                 'type': 'str'
                             }), ('name', {
                                 'required': False,
                                 'type': 'str'
                             }),
                             ('ospf', {
                                 'options':
                                 OrderedDict([('areas', {
                                     'elements':
                                     'dict',
                                     'options':
                                     OrderedDict([('area', {
                                         'options':
                                         OrderedDict([
                                             ('area-id', {
                                                 'required': False,
                                                 'type': 'str'
                                             }),
                                             ('interfaces', {
                                                 'elements':
                                                 'dict',
                                                 'options':
                                                 OrderedDict([('interface', {
                                                     'options':
                                                     OrderedDict([
                                                         ('name', {
                                                             'required': False,
                                                             'type': 'str'
                                                         }),
                                                         ('cost', {
                                                             'required': False,
                                                             'type': 'int'
                                                         })
                                                     ]),
                                                     'type':
                                                     'dict'
                                                 })]),
                                                 'type':
                                                 'list'
                                             })
                                         ]),
                                         'type':
                                         'dict'
                                     })]),
                                     'type':
                                     'list'
                                 })]),
                                 'type':
                                 'dict'
                             })
                         ]),
                         'type':
                         'dict'
                     })]),
                     'type':
                     'list'
                 })]),
    'type':
    'dict'
})])

# Operation type
operation_dict = {
    'operation_type': {
        'type': 'str',
        'required': True,
        'choices': ['config', 'get', 'get-config', 'rpc']
    },
    'operation_specs': {
        'elements': 'dict',
        'type': 'list',
        'options': {
            'path': {
                'type': 'str'
            },
            'operation': {
                'choices': ['merge', 'replace', 'create', 'delete', 'remove'],
                'default': 'merge'
            }
        }
    }
}

# Parameters passed to check params
leaf_info = OrderedDict([(
    'routing',
    OrderedDict([
        ('router-id', {
            'required':
            False,
            'pattern': [
                '(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'
            ],
            'length': [],
            'default':
            None,
            'type':
            'string',
            'key':
            False
        }),
        ('control-plane-protocols',
         OrderedDict([(
             'control-plane-protocol',
             OrderedDict([
                 ('type', {
                     'required':
                     False,
                     'pattern':
                     [],
                     'length':
                     [],
                     'default':
                     None,
                     'type':
                     'string',
                     'key':
                     True
                 }),
                 ('name', {
                     'required':
                     False,
                     'pattern':
                     [],
                     'length':
                     [],
                     'default':
                     None,
                     'type': 'string',
                     'key': True
                 }),
                 ('ospf',
                  OrderedDict([(
                      'areas',
                      OrderedDict([(
                          'area',
                          OrderedDict([('area-id', {
                              'required':
                              False,
                              'pattern':
                              [
                                  '(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'
                              ],
                              'length': [],
                              'default':
                              None,
                              'type':
                              'string',
                              'key':
                              True
                          }),
                                       ('interfaces',
                                        OrderedDict([
                                            ('interface',
                                             OrderedDict([('name', {
                                                 'required': False,
                                                 'pattern': [],
                                                 'length': [],
                                                 'default': None,
                                                 'type': 'string',
                                                 'key': True
                                             }),
                                                          ('cost', {
                                                              'required':
                                                              False,
                                                              'pattern': [],
                                                              'default':
                                                              None,
                                                              'type':
                                                              'int',
                                                              'key':
                                                              False,
                                                              'range':
                                                              [(0, 65535)]
                                                          })]))
                                        ]))]))]))]))
             ]))]))
    ]))])


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
    return (list(
        filter(lambda m: m.startswith("check_"),
               [i + '()' for i in dir(user_check_obj)])))


def main():
    """Module main"""
    argument_spec.update(ne_argument_spec)
    argument_spec.update(operation_dict)
    args = (argument_spec, leaf_info, namespaces, business_tag, xml_head,
            xml_tail, key_list)
    module_params = ConfigBase(*args).get_operation_type()
    for check_func in filter_check(UserCheck):
        if not eval('UserCheck(module_params, leaf_info).' + check_func):
            ConfigBase(*args).init_module().fail_json(msg='UserCheck.' +
                                                      check_func)
    operation(module_params['operation_type'], args)


if __name__ == '__main__':
    main()
