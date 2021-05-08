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
- name: ietf_l3vpn
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

  - name: l3vpn
    ietf_l3vpn:
      operation_type: config
      l3vpn-ntw: 
        vpn-services: 
          - vpn-service: 
              vpn-id: "4G"
              customer-name: "mycustomer"
              vpn-service-topology: "custom"
              vpn-nodes: 
                - vpn-node: 
                    vpn-node-id: "44"
                    ne-id: "10.0.0.1"
                    local-autonomous-system: 65500
                    rd: "0:65500:1"
                    vpn-targets: 
                      - vpn-target: 
                          id: 1
                          - route-targets: 
                              route-target: "0:65500:1"
                          route-target-type: both
                    vpn-network-accesses: 
                      - vpn-network-access: 
                          id: "1"
                          port-id: "GigabitEthernet 3/0/0"
                          description: "Interface DATA to eNODE-B"
                          status: ""
                          vpn-network-access-type: "vpn-common:point-to-point"
                          ip-connection: 
                            ipv4: 
                              address-allocation-type: "static-address"
                              primary-address: "1"
                              - address: 
                                  address-id: "1"
                                  s-provider-address: "192.0.2.1"
                                  s-customer-address: "192.0.2.2"
                                  s-prefix-length: 32
                          routing-protocols: 
                            - routing-protocol: 
                                id: "1"
                                type: "vpn-common:bgp"
                                bgp: 
                                  peer-autonomous-system: 200
                                  local-autonomous-system: 65500
                                  address-family: ipv4
                                  neighbor: "192.0.2.2"
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:ietf_l3vpn
version_added: "2.6"
short_description: 
description:
    - 
author:ansible_team@huawei
time:2021-05-07 17:26:00
options:
    opreation_type:config
        description:config
            - This is a helper node ,Choose from config, get
        type: str
        required:True
        chioces: ["config","get","get-config"]
    l3vpn-ntw:
        description:
            - Main container for L3VPN services management.
        required:False
        vpn-services:
            description:
                - Top-level container for the VPN services.
            required:False
            vpn-service:
                description:
                    - List of VPN services.
                required:False
                vpn-id:
                    description:
                        - VPN identifier.
                          This identifier has a local meaning.
                    required:False
                    type:str
                customer-name:
                    description:
                        - Name of the customer that actually uses the VPN service.
                    required:False
                    type:str
                vpn-service-topology:
                    description:
                        - VPN service topology.
                    required:False
                    default:vpn-common:any-to-any
                    type:str
                    length:None
                vpn-nodes:
                    description:
                        - Container for VPN nodes.
                    required:False
                    vpn-node:
                        description:
                            - List for VPN node.
                        required:False
                        vpn-node-id:
                            description:
                                - Type STRING or NUMBER Service-Id.
                            required:True
                            key:True
                            type:str
                            length:None
                        ne-id:
                            description:
                                - Unique identifier of the network element
                                  where the VPN node is deployed.
                            required:False
                            type:str
                        local-autonomous-system:
                            description:
                                - Provider's AS number in case the customer
                                  requests BGP routing.
                            required:False
                            type:int
                            range:[(0, 4294967295)]
                        rd:
                            description:
                                - Route distinguisher value. If this leaf has not been
                                  configured, the server will auto-assign a route
                                  distinguisher value and use that value operationally.
                                  This calculated value is available in the operational
                                  state.
                                  Use the empty type to indicate RD has no value and
                                  is not to be aouto-assigned.
                            required:False
                            type:str
                            length:None
                        vpn-targets:
                            description:
                                - Set of route-targets to match for import and export routes
                                  to/from VRF
                            required:False
                            vpn-target:
                                description:
                                    - L3VPN route targets. AND/OR Operations are available
                                      based on the RTs assigment.
                                required:False
                                id:
                                    description:
                                        - Identifies each VPN Target
                                    required:True
                                    key:True
                                    type:int
                                    range:[(-128, 127)]
                                route-targets:
                                    description:
                                        - List of Route Targets.
                                    required:False
                                    route-target:
                                        description:
                                            - Route Target value
                                        required:True
                                        key:True
                                        pattern:['(0:(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|0):(429496729[0-5]|42949672[0-8][0-9]|4294967[01][0-9]{2}|429496[0-6][0-9]{3}|42949[0-5][0-9]{4}|4294[0-8][0-9]{5}|429[0-3][0-9]{6}|42[0-8][0-9]{7}|4[01][0-9]{8}|[1-3][0-9]{9}|[1-9][0-9]{0,8}|0))|(1:((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])):(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|0))|(2:(429496729[0-5]|42949672[0-8][0-9]|4294967[01][0-9]{2}|429496[0-6][0-9]{3}|42949[0-5][0-9]{4}|4294[0-8][0-9]{5}|429[0-3][0-9]{6}|42[0-8][0-9]{7}|4[01][0-9]{8}|[1-3][0-9]{9}|[1-9][0-9]{0,8}|0):(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|0))|(6(:[a-fA-F0-9]{2}){6})|(([3-57-9a-fA-F]|[1-9a-fA-F][0-9a-fA-F]{1,3}):[0-9a-fA-F]{1,12})']
                                        type:str
                                route-target-type:
                                    description:
                                        - Import/export type of the Route Target.
                                    required:True
                                    mandatory:True
                                    type:enum
                                    choices:['import', 'export', 'both']
                        vpn-network-accesses:
                            description:
                                - List of accesses for a site.
                            required:False
                            vpn-network-access:
                                description:
                                    - List of accesses for a site.
                                required:False
                                id:
                                    description:
                                        - Identifier for the access.
                                    required:True
                                    key:True
                                    type:str
                                port-id:
                                    description:
                                        - Identifier for the network access.
                                    required:False
                                    type:str
                                description:
                                    description:
                                        - Textual description of a network access.
                                    required:False
                                    type:str
                                status:
                                    description:
                                        - Service status.
                                    required:False
                                    pattern:None
                                    type:None
                                vpn-network-access-type:
                                    description:
                                        - Describes the type of connection, e.g.,
                                          point-to-point or multipoint.
                                    required:False
                                    default:vpn-common:point-to-point
                                    type:str
                                    length:None
                                ip-connection:
                                    description:
                                        - Defines connection parameters.
                                    required:False
                                    ipv4:
                                        description:
                                            - IPv4-specific parameters.
                                        required:False
                                        address-allocation-type:
                                            description:
                                                - Defines how addresses are allocated.
                                                  If there is no value for the address
                                                  allocation type, then IPv4 is not enabled.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            type:str
                                            length:None
                                        primary-address:
                                            description:
                                                - Principal address of the connection.
                                            required:False
                                            type:str
                                        address:
                                            description:
                                                - Describes IPv4 addresses used.
                                            required:False
                                            address-id:
                                                description:
                                                    - IPv4 Address
                                                required:True
                                                key:True
                                                type:str
                                            s-provider-address:
                                                description:
                                                    - IPv4 Address List of the provider side.
                                                      When the protocol allocation type is
                                                      static, the provider address must be
                                                      configured.
                                                required:False
                                                pattern:['(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\\p{N}\\p{L}]+)?']
                                                type:str
                                            s-customer-address:
                                                description:
                                                    - IPv4 Address of customer side.
                                                required:False
                                                pattern:['(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\\p{N}\\p{L}]+)?']
                                                type:str
                                            s-prefix-length:
                                                description:
                                                    - Subnet prefix length expressed
                                                      in bits. It is applied to both
                                                      provider-address and customer-address.
                                                required:False
                                                type:int
                                                range:[(0, 32)]
                                routing-protocols:
                                    description:
                                        - Defines routing protocols.
                                    required:False
                                    routing-protocol:
                                        description:
                                            - List of routing protocols used on
                                              the site.  This list can be augmented.
                                        required:False
                                        id:
                                            description:
                                                - Unique identifier for routing protocol.
                                            required:True
                                            key:True
                                            type:str
                                        type:
                                            description:
                                                - Type of routing protocol.
                                            required:False
                                            type:str
                                            length:None
                                        bgp:
                                            description:
                                                - BGP-specific configuration.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            peer-autonomous-system:
                                                description:
                                                    - Indicates the Customer's AS Number (ASN) in
                                                      case the Customer requests BGP routing.
                                                required:True
                                                mandatory:True
                                                type:int
                                                range:[(0, 4294967295)]
                                            local-autonomous-system:
                                                description:
                                                    - Is set to the ASN to override a peers' ASN
                                                      if such feature is requested by the
                                                      Customer.
                                                required:False
                                                type:int
                                                range:[(0, 4294967295)]
                                            address-family:
                                                description:
                                                    - This node contains at least one
                                                      address-family to be activated.
                                                required:False
                                                type:enum
                                                choices:['ipv4', 'ipv6']
                                            neighbor:
                                                description:
                                                    - IP address(es) of the BGP neighbor. IPv4
                                                      and IPv6 neighbors may be indicated if
                                                      two sessions will be used for IPv4 and
                                                      IPv6.
                                                required:False
                                                type:str
                                                length:None

"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/l3vpn-ntw/vpn-services/vpn-service/vpn-id', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-node-id', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/id', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/route-targets/route-target', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/id', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/address-id', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/id']

namespaces = [{'/l3vpn-ntw': ['', '@xmlns="urn:ietf:params:xml:ns:yang:ietf-l3vpn-ntw"', '/l3vpn-ntw']}, {'/l3vpn-ntw/vpn-services': ['', '', '/l3vpn-ntw/vpn-services']}, {'/l3vpn-ntw/vpn-services/vpn-service': ['', '', '/l3vpn-ntw/vpn-services/vpn-service']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-id': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-id']}, {'/l3vpn-ntw/vpn-services/vpn-service/customer-name': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/customer-name']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-service-topology': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-service-topology']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-node-id': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-node-id']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/ne-id': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/ne-id']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/local-autonomous-system': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/local-autonomous-system']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/rd': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/rd']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/id': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/id']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/route-targets': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/route-targets']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/route-target-type': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/route-target-type']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/id': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/id']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/port-id': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/port-id']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/description': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/description']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/status': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/status']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/vpn-network-access-type': ['', '@xmlns:vpn-common="urn:ietf:params:xml:ns:yang:ietf-vpn-common"', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/vpn-network-access-type']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/route-targets/route-target': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-targets/vpn-target/route-targets/route-target']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address-allocation-type': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address-allocation-type']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/primary-address': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/primary-address']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/id': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/id']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/type': ['', '@xmlns:vpn-common="urn:ietf:params:xml:ns:yang:ietf-vpn-common"', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/type']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/address-id': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/address-id']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/s-provider-address': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/s-provider-address']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/s-customer-address': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/s-customer-address']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/s-prefix-length': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/ip-connection/ipv4/address/s-prefix-length']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp/peer-autonomous-system': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp/peer-autonomous-system']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp/local-autonomous-system': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp/local-autonomous-system']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp/address-family': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp/address-family']}, {'/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp/neighbor': ['', '', '/l3vpn-ntw/vpn-services/vpn-service/vpn-nodes/vpn-node/vpn-network-accesses/vpn-network-access/routing-protocols/routing-protocol/bgp/neighbor']}]

business_tag = ['l3vpn-ntw']

# Passed to the ansible parameter
argument_spec = OrderedDict([('l3vpn-ntw', {'type': 'dict', 'options': OrderedDict([('vpn-services', {'elements': 'dict', 'type': 'list', 'options': OrderedDict([('vpn-service', {'type': 'dict', 'options': OrderedDict([('vpn-id', {'type': 'str', 'required': False}), ('customer-name', {'type': 'str', 'required': False}), ('vpn-service-topology', {'type': 'str', 'required': False}), ('vpn-nodes', {'elements': 'dict', 'type': 'list', 'options': OrderedDict([('vpn-node', {'type': 'dict', 'options': OrderedDict([('vpn-node-id', {'type': 'str', 'required': False}), ('ne-id', {'type': 'str', 'required': False}), ('local-autonomous-system', {'type': 'int', 'required': False}), ('rd', {'type': 'str', 'required': False}), ('vpn-targets', {'elements': 'dict', 'type': 'list', 'options': OrderedDict([('vpn-target', {'elements': 'dict', 'type': 'list', 'options': OrderedDict([('id', {'type': 'int', 'required': False}), ('route-targets', {'type': 'dict', 'options': OrderedDict([('route-target', {'type': 'str', 'required': False})])}), ('route-target-type', {'required': False, 'choices': ['import', 'export', 'both']})])})])}), ('vpn-network-accesses', {'elements': 'dict', 'type': 'list', 'options': OrderedDict([('vpn-network-access', {'type': 'dict', 'options': OrderedDict([('id', {'type': 'str', 'required': False}), ('port-id', {'type': 'str', 'required': False}), ('description', {'type': 'str', 'required': False}), ('status', {'type': None, 'required': False}), ('vpn-network-access-type', {'type': 'str', 'required': False}), ('ip-connection', {'type': 'dict', 'options': OrderedDict([('ipv4', {'elements': 'dict', 'type': 'list', 'options': OrderedDict([('address-allocation-type', {'type': 'str', 'required': False}), ('primary-address', {'type': 'str', 'required': False}), ('address', {'type': 'dict', 'options': OrderedDict([('address-id', {'type': 'str', 'required': False}), ('s-provider-address', {'type': 'str', 'required': False}), ('s-customer-address', {'type': 'str', 'required': False}), ('s-prefix-length', {'type': 'int', 'required': False})])})])})])}), ('routing-protocols', {'elements': 'dict', 'type': 'list', 'options': OrderedDict([('routing-protocol', {'type': 'dict', 'options': OrderedDict([('id', {'type': 'str', 'required': False}), ('type', {'type': 'str', 'required': False}), ('bgp', {'type': 'dict', 'options': OrderedDict([('peer-autonomous-system', {'type': 'int', 'required': False}), ('local-autonomous-system', {'type': 'int', 'required': False}), ('address-family', {'required': False, 'choices': ['ipv4', 'ipv6']}), ('neighbor', {'type': 'str', 'required': False})])})])})])})])})])})])})])})])})])})])})])

# Operation type
operation_dict = {'operation_type':{'type': 'str', 'required':True, 'choices': ['config','get','get-config','rpc']},
                  'operation_specs': {
                      'elements': 'dict', 'type': 'list','options': {
                          'path': {
                              'type': 'str'}, 'operation': {
                              'choices': ['merge', 'replace', 'create', 'delete', 'remove'],'default':'merge'}}}}

# Parameters passed to check params
leaf_info =  OrderedDict([('l3vpn-ntw', OrderedDict([('vpn-services', OrderedDict([('vpn-service', OrderedDict([('vpn-id', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('customer-name', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('vpn-service-topology', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('vpn-nodes', OrderedDict([('vpn-node', OrderedDict([('vpn-node-id', {
                'key': True, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('ne-id', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('local-autonomous-system', {
                'key': False, 'type': 'int', 'required': False, 
                'pattern': [], 
                'range': [(0, 4294967295)], 
                'default': None}), 
            ('rd', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('vpn-targets', OrderedDict([('vpn-target', OrderedDict([('id', {
                'key': True, 'type': 'int', 'required': False, 
                'pattern': [], 
                'range': [(-128, 127)], 
                'default': None}), 
            ('route-targets', OrderedDict([('route-target', {
                'key': True, 'type': 'string', 'required': False, 
                'pattern': ['(0:(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|0):(429496729[0-5]|42949672[0-8][0-9]|4294967[01][0-9]{2}|429496[0-6][0-9]{3}|42949[0-5][0-9]{4}|4294[0-8][0-9]{5}|429[0-3][0-9]{6}|42[0-8][0-9]{7}|4[01][0-9]{8}|[1-3][0-9]{9}|[1-9][0-9]{0,8}|0))|(1:((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])):(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|0))|(2:(429496729[0-5]|42949672[0-8][0-9]|4294967[01][0-9]{2}|429496[0-6][0-9]{3}|42949[0-5][0-9]{4}|4294[0-8][0-9]{5}|429[0-3][0-9]{6}|42[0-8][0-9]{7}|4[01][0-9]{8}|[1-3][0-9]{9}|[1-9][0-9]{0,8}|0):(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|0))|(6(:[a-fA-F0-9]{2}){6})|(([3-57-9a-fA-F]|[1-9a-fA-F][0-9a-fA-F]{1,3}):[0-9a-fA-F]{1,12})'], 
                'length': [], 
                'default': None})])), 
            ('route-target-type', {
                'key': False, 'type': 'enumeration', 'required': False, 
                'pattern': [], 
                'default': None, 'choices': ['import', 'export', 'both']})]))])), 
            ('vpn-network-accesses', OrderedDict([('vpn-network-access', OrderedDict([('id', {
                'key': True, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('port-id', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('description', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('status', {
                'key': False, 'type': None, 'required': False, 
                'pattern': None, 'default': None}), 
            ('vpn-network-access-type', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('ip-connection', OrderedDict([('ipv4', OrderedDict([('address-allocation-type', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('primary-address', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('address', OrderedDict([('address-id', {
                'key': True, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('s-provider-address', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': ['(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\\p{N}\\p{L}]+)?'], 
                'length': [], 
                'default': None}), 
            ('s-customer-address', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': ['(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\\p{N}\\p{L}]+)?'], 
                'length': [], 
                'default': None}), 
            ('s-prefix-length', {
                'key': False, 'type': 'int', 'required': False, 
                'pattern': [], 
                'range': [(0, 32)], 
                'default': None})]))]))])), 
            ('routing-protocols', OrderedDict([('routing-protocol', OrderedDict([('id', {
                'key': True, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('type', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None}), 
            ('bgp', OrderedDict([('peer-autonomous-system', {
                'key': False, 'type': 'int', 'required': False, 
                'pattern': [], 
                'range': [(0, 4294967295)], 
                'default': None}), 
            ('local-autonomous-system', {
                'key': False, 'type': 'int', 'required': False, 
                'pattern': [], 
                'range': [(0, 4294967295)], 
                'default': None}), 
            ('address-family', {
                'key': False, 'type': 'enumeration', 'required': False, 
                'pattern': [], 
                'default': None, 'choices': ['ipv4', 'ipv6']}), 
            ('neighbor', {
                'key': False, 'type': 'string', 'required': False, 
                'pattern': [], 
                'length': [], 
                'default': None})]))]))]))]))]))]))]))]))]))]))])


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
