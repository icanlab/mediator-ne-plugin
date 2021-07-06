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
- name: IETF_105
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

  - name: IETF_105_full
    IETF_105:
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
              bgp:
                global:
                  as: 100
                  afi-safis:
                    - afi-safi:
                        afi-safi-name: "ipv4-unicast"
                        enabled: true
                        ipv4-unicast:
                          segment-routing:
        srv6:
          enable: true
          encapsulation:
            source-address: "A1::123"
          locators:
            - locator:
                name: "test1"
                enable: true
                prefix:
                  address: "A2::123"
                  length: 64
                static:
                  local-sids:
                    - sid:
                        end-behavior-type: "End.DT4"
                        end-dt4:
                          lookup-table-ipv4: 100
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
    '/routing/control-plane-protocols/control-plane-protocol/bgp/global/afi-safis/afi-safi/afi-safi-name',
    '/routing/srv6/locators/locator/name']

namespaces = [{'/rt:routing': ['',
                               '@xmlns:rt="urn:ietf:params:xml:ns:yang:ietf-routing"',
                               '/rt:routing']},
              {'/rt:routing/rt:control-plane-protocols': ['',
                                                          '',
                                                          '/rt:routing/rt:control-plane-protocols']},
              {'/rt:routing/srv6:srv6': ['',
                                         '@xmlns:srv6="urn:ietf:params:xml:ns:yang:ietf-srv6-base"',
                                         '/rt:routing/srv6:srv6']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol': ['',
                                                                                    '',
                                                                                    '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol']},
              {'/rt:routing/srv6:srv6/srv6:enable': ['true',
                                                     '',
                                                     '/rt:routing/srv6:srv6/srv6:enable']},
              {'/rt:routing/srv6:srv6/srv6:encapsulation': ['',
                                                            '',
                                                            '/rt:routing/srv6:srv6/srv6:encapsulation']},
              {'/rt:routing/srv6:srv6/srv6:locators': ['',
                                                       '',
                                                       '/rt:routing/srv6:srv6/srv6:locators']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/rt:type': ['isis',
                                                                                            '',
                                                                                            '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/rt:type']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/rt:name': ['is-is-1',
                                                                                            '',
                                                                                            '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/rt:name']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis': ['',
                                                                                              '@xmlns:isis="urn:ietf:params:xml:ns:yang:ietf-isis"',
                                                                                              '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp': ['',
                                                                                            '@xmlns:bgp="urn:ietf:params:xml:ns:yang:ietf-bgp"',
                                                                                            '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp']},
              {'/rt:routing/srv6:srv6/srv6:encapsulation/srv6:source-address': ['A1::123',
                                                                                '',
                                                                                '/rt:routing/srv6:srv6/srv6:encapsulation/srv6:source-address']},
              {'/rt:routing/srv6:srv6/srv6:encapsulation/srv6:ip-ttl-propagation': ['1',
                                                                                    '',
                                                                                    '/rt:routing/srv6:srv6/srv6:encapsulation/srv6:ip-ttl-propagation']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator': ['',
                                                                    '',
                                                                    '/rt:routing/srv6:srv6/srv6:locators/srv6:locator']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis:enable': ['true',
                                                                                                          '',
                                                                                                          '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis:enable']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis:level-type': ['level-2',
                                                                                                              '',
                                                                                                              '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis:level-type']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis:system-id': ['1111.1111.1111',
                                                                                                             '',
                                                                                                             '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis:system-id']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis:area-address': ['00',
                                                                                                                '',
                                                                                                                '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis:area-address']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg': ['',
                                                                                                                 '@xmlns:isis-srv6="urn:ietf:params:xml:ns:yang:ietf-isis-srv6"',
                                                                                                                 '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global': ['',
                                                                                                       '',
                                                                                                       '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:name': ['test1',
                                                                              '',
                                                                              '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:name']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:enable': ['true',
                                                                                '',
                                                                                '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:enable']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:is-default': ['true',
                                                                                    '',
                                                                                    '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:is-default']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:prefix': ['',
                                                                                '',
                                                                                '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:prefix']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static': ['',
                                                                                       '@xmlns:srv6-static="urn:ietf:params:xml:ns:yang:ietf-srv6-static"',
                                                                                       '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg/isis-srv6:enable': ['true',
                                                                                                                                  '',
                                                                                                                                  '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg/isis-srv6:enable']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg/isis-srv6:default-locator': ['false',
                                                                                                                                           '',
                                                                                                                                           '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg/isis-srv6:default-locator']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg/isis-srv6:locator-name': ['test',
                                                                                                                                        '',
                                                                                                                                        '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg/isis-srv6:locator-name']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg/isis-srv6:persistent-end-x-sid': ['true',
                                                                                                                                                '',
                                                                                                                                                '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/isis:isis/isis-srv6:srv6-cfg/isis-srv6:persistent-end-x-sid']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:as': ['100',
                                                                                                              '',
                                                                                                              '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:as']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis': ['',
                                                                                                                     '',
                                                                                                                     '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:prefix/srv6:address': ['A2::123',
                                                                                             '',
                                                                                             '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:prefix/srv6:address']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:prefix/srv6:length': ['64',
                                                                                            '',
                                                                                            '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6:prefix/srv6:length']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids': ['',
                                                                                                              '',
                                                                                                              '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi': ['',
                                                                                                                                  '',
                                                                                                                                  '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid': ['',
                                                                                                                              '',
                                                                                                                              '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:afi-safi-name': ['ipv4-unicast',
                                                                                                                                                    '',
                                                                                                                                                    '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:afi-safi-name']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:enabled': ['true',
                                                                                                                                              '',
                                                                                                                                              '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:enabled']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:ipv4-unicast': ['',
                                                                                                                                                   '',
                                                                                                                                                   '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:ipv4-unicast']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid/srv6-static:opcode': ['66',
                                                                                                                                                 '',
                                                                                                                                                 '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid/srv6-static:opcode']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid/srv6-static:end-behavior-type': ['End.DT4',
                                                                                                                                                            '',
                                                                                                                                                            '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid/srv6-static:end-behavior-type']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid/srv6-static:end-dt4': ['',
                                                                                                                                                  '',
                                                                                                                                                  '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid/srv6-static:end-dt4']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:ipv4-unicast/bgp-sr:segment-routing': ['',
                                                                                                                                                                          '@xmlns:bgp-sr="urn:ietf:params:xml:ns:yang:ietf-bgp-sr"',
                                                                                                                                                                          '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:ipv4-unicast/bgp-sr:segment-routing']},
              {'/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid/srv6-static:end-dt4/srv6-static:lookup-table-ipv4': ['100',
                                                                                                                                                                                '',
                                                                                                                                                                                '/rt:routing/srv6:srv6/srv6:locators/srv6:locator/srv6-static:static/srv6-static:local-sids/srv6-static:sid/srv6-static:end-dt4/srv6-static:lookup-table-ipv4']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:ipv4-unicast/bgp-sr:segment-routing/bgp-sr:srv6': ['',
                                                                                                                                                                                      '',
                                                                                                                                                                                      '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:ipv4-unicast/bgp-sr:segment-routing/bgp-sr:srv6']},
              {'/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:ipv4-unicast/bgp-sr:segment-routing/bgp-sr:srv6/bgp-sr:sid-alloc-mode': ['per-vpn',
                                                                                                                                                                                                            '',
                                                                                                                                                                                                            '/rt:routing/rt:control-plane-protocols/rt:control-plane-protocol/bgp:bgp/bgp:global/bgp:afi-safis/bgp:afi-safi/bgp:ipv4-unicast/bgp-sr:segment-routing/bgp-sr:srv6/bgp-sr:sid-alloc-mode']}]

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
                                                                                                           ('isis',
                                                                                                            {'type': 'dict',
                                                                                                             'options': OrderedDict([('enable',
                                                                                                                                      {'type': 'bool',
                                                                                                                                       'required': False}),
                                                                                                                                     ('level-type',
                                                                                                                                      {'choices': ['level-1',
                                                                                                                                                   'level-2',
                                                                                                                                                   'level-all'],
                                                                                                                                       'required': False}),
                                                                                                                                     ('system-id',
                                                                                                                                      {'type': 'str',
                                                                                                                                       'required': False}),
                                                                                                                                     ('area-address',
                                                                                                                                      {'type': 'str',
                                                                                                                                       'required': False}),
                                                                                                                                     ('srv6-cfg',
                                                                                                                                      {'type': 'dict',
                                                                                                                                       'options': OrderedDict([('enable',
                                                                                                                                                                {'type': 'bool',
                                                                                                                                                                 'required': False}),
                                                                                                                                                               ('default-locator',
                                                                                                                                                                {'type': 'bool',
                                                                                                                                                                 'required': False}),
                                                                                                                                                               ('locator-name',
                                                                                                                                                                {'type': 'str',
                                                                                                                                                                 'required': False}),
                                                                                                                                                               ('persistent-end-x-sid',
                                                                                                                                                                {'type': 'bool',
                                                                                                                                                                 'required': False})])})])}),
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
                                                                                                                                                                                                                     'required': False}),
                                                                                                                                                                                                                   ('ipv4-unicast',
                                                                                                                                                                                                                    {'type': 'dict',
                                                                                                                                                                                                                     'options': OrderedDict([('segment-routing',
                                                                                                                                                                                                                                              {'type': 'dict',
                                                                                                                                                                                                                                               'options': OrderedDict()})])})])})])})])})])})])})])}),
                                                       ('srv6',
                                                        {'type': 'dict',
                                                         'options': OrderedDict([('enable',
                                                                                  {'type': 'bool',
                                                                                   'required': False}),
                                                                                 ('encapsulation',
                                                                                  {'type': 'dict',
                                                                                   'options': OrderedDict([('source-address',
                                                                                                            {'type': 'str',
                                                                                                             'required': False})])}),
                                                                                 ('locators',
                                                                                  {'type': 'list',
                                                                                   'elements': 'dict',
                                                                                   'options': OrderedDict([('locator',
                                                                                                            {'type': 'dict',
                                                                                                             'options': OrderedDict([('name',
                                                                                                                                      {'type': 'str',
                                                                                                                                       'required': False}),
                                                                                                                                     ('enable',
                                                                                                                                      {'type': 'bool',
                                                                                                                                       'required': False}),
                                                                                                                                     ('prefix',
                                                                                                                                      {'type': 'dict',
                                                                                                                                       'options': OrderedDict([('address',
                                                                                                                                                                {'type': 'str',
                                                                                                                                                                 'required': False}),
                                                                                                                                                               ('length',
                                                                                                                                                                {'type': 'int',
                                                                                                                                                                 'required': False})])}),
                                                                                                                                     ('static',
                                                                                                                                      {'type': 'dict',
                                                                                                                                       'options': OrderedDict([('local-sids',
                                                                                                                                                                {'type': 'list',
                                                                                                                                                                 'elements': 'dict',
                                                                                                                                                                 'options': OrderedDict([('sid',
                                                                                                                                                                                          {'type': 'dict',
                                                                                                                                                                                           'options': OrderedDict([('end-behavior-type',
                                                                                                                                                                                                                    {'type': 'str',
                                                                                                                                                                                                                     'required': False}),
                                                                                                                                                                                                                   ('end-dt4',
                                                                                                                                                                                                                    {'type': 'dict',
                                                                                                                                                                                                                     'options': OrderedDict([('lookup-table-ipv4',
                                                                                                                                                                                                                                              {'type': 'int',
                                                                                                                                                                                                                                               'required': False})])})])})])})])})])})])})])})])})])

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
                                                                    {'required': False,
                                                                     'type': 'string',
                                                                     'default': None,
                                                                     'pattern': [],
                                                                        'key': True,
                                                                        'length': []}),
                                                                   ('name',
                                                                    {'required': False,
                                                                     'type': 'string',
                                                                     'default': None,
                                                                     'pattern': [],
                                                                     'key': True,
                                                                     'length': []}),
                                                                   ('isis',
                                                                    OrderedDict([('enable',
                                                                                  {'required': False,
                                                                                   'type': 'boolean',
                                                                                   'default': None,
                                                                                   'pattern': [],
                                                                                   'key': False}),
                                                                                 ('level-type',
                                                                                  {'required': False,
                                                                                   'type': 'enumeration',
                                                                                   'default': None,
                                                                                   'pattern': [],
                                                                                   'key': False,
                                                                                   'choices': ['level-1',
                                                                                               'level-2',
                                                                                               'level-all']}),
                                                                                 ('system-id',
                                                                                  {'required': False,
                                                                                   'type': 'string',
                                                                                   'default': None,
                                                                                   'pattern': ['[0-9A-Fa-f]{4}\\.[0-9A-Fa-f]{4}\\.[0-9A-Fa-f]{4}'],
                                                                                   'key': False,
                                                                                   'length': []}),
                                                                                 ('area-address',
                                                                                  {'required': False,
                                                                                   'type': 'string',
                                                                                   'default': None,
                                                                                   'pattern': ['[0-9A-Fa-f]{2}(\\.[0-9A-Fa-f]{4}){0,6}'],
                                                                                   'key': False,
                                                                                   'length': []}),
                                                                                 ('srv6-cfg',
                                                                                  OrderedDict([('enable',
                                                                                                {'required': False,
                                                                                                 'type': 'boolean',
                                                                                                 'default': None,
                                                                                                 'pattern': [],
                                                                                                 'key': False}),
                                                                                               ('default-locator',
                                                                                                {'required': False,
                                                                                                 'type': 'boolean',
                                                                                                 'default': None,
                                                                                                 'pattern': [],
                                                                                                 'key': False}),
                                                                                               ('locator-name',
                                                                                                {'required': False,
                                                                                                 'type': 'string',
                                                                                                 'default': None,
                                                                                                 'pattern': [],
                                                                                                 'key': False,
                                                                                                 'length': []}),
                                                                                               ('persistent-end-x-sid',
                                                                                                {'required': False,
                                                                                                 'type': 'boolean',
                                                                                                 'default': None,
                                                                                                 'pattern': [],
                                                                                                 'key': False})]))])),
                                                                   ('bgp',
                                                                    OrderedDict([('global',
                                                                                  OrderedDict([('as',
                                                                                                {'required': False,
                                                                                                 'type': 'int',
                                                                                                 'default': None,
                                                                                                 'pattern': [],
                                                                                                 'key': False,
                                                                                                 'range': [(0,
                                                                                                            4294967295)]}),
                                                                                               ('afi-safis',
                                                                                                OrderedDict([('afi-safi',
                                                                                                              OrderedDict([('afi-safi-name',
                                                                                                                            {'required': False,
                                                                                                                             'type': 'string',
                                                                                                                             'default': None,
                                                                                                                             'pattern': [],
                                                                                                                             'key': True,
                                                                                                                             'length': []}),
                                                                                                                           ('enabled',
                                                                                                                            {'required': False,
                                                                                                                             'type': 'boolean',
                                                                                                                             'default': None,
                                                                                                                             'pattern': [],
                                                                                                                             'key': False}),
                                                                                                                           ('ipv4-unicast',
                                                                                                                            OrderedDict([('segment-routing',
                                                                                                                                          OrderedDict([('srv6',
                                                                                                                                                        OrderedDict())]))]))]))]))]))]))]))])),
                                       ('srv6',
                                        OrderedDict([('enable',
                                                      {'required': False,
                                                       'type': 'boolean',
                                                       'default': None,
                                                       'pattern': [],
                                                       'key': False}),
                                                     ('encapsulation',
                                                      OrderedDict([('source-address',
                                                                    {'required': False,
                                                                     'type': 'string',
                                                                     'default': None,
                                                                     'pattern': ['((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\p{N}\\p{L}]+)?',
                                                                                 '(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?'],
                                                                     'key': False,
                                                                     'length': []})])),
                                                     ('locators',
                                                      OrderedDict([('locator',
                                                                    OrderedDict([('name',
                                                                                  {'required': False,
                                                                                   'type': 'string',
                                                                                   'default': None,
                                                                                   'pattern': [],
                                                                                   'key': True,
                                                                                   'length': []}),
                                                                                 ('enable',
                                                                                  {'required': False,
                                                                                   'type': 'boolean',
                                                                                   'default': None,
                                                                                   'pattern': [],
                                                                                   'key': False}),
                                                                                 ('prefix',
                                                                                  OrderedDict([('address',
                                                                                                {'required': False,
                                                                                                 'type': 'string',
                                                                                                 'default': None,
                                                                                                 'pattern': ['((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[\\p{N}\\p{L}]+)?',
                                                                                                             '(([^:]+:){6}(([^:]+:[^:]+)|(.*\\..*)))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?'],
                                                                                                 'key': False,
                                                                                                 'length': []}),
                                                                                               ('length',
                                                                                                {'required': False,
                                                                                                 'type': 'int',
                                                                                                 'default': None,
                                                                                                 'pattern': [],
                                                                                                 'key': False,
                                                                                                 'range': [(32,
                                                                                                            96)]})])),
                                                                                 ('static',
                                                                                  OrderedDict([('local-sids',
                                                                                                OrderedDict([('sid',
                                                                                                              OrderedDict([('end-behavior-type',
                                                                                                                            {'required': False,
                                                                                                                             'type': 'string',
                                                                                                                             'default': None,
                                                                                                                             'pattern': [],
                                                                                                                             'key': False,
                                                                                                                             'length': []}),
                                                                                                                           ('end-dt4',
                                                                                                                            OrderedDict([('lookup-table-ipv4',
                                                                                                                                          {'required': False,
                                                                                                                                           'type': 'int',
                                                                                                                                           'default': None,
                                                                                                                                           'pattern': [],
                                                                                                                                           'key': False,
                                                                                                                                           'range': [(0,
                                                                                                                                                      4294967295)]})]))]))]))]))]))]))]))]))])


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
