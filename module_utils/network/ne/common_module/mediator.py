import os

import requests
import yaml
from lxml import etree

NSMAP = {
    None: 'urn:ietf:params:xml:ns:netconf:base:1.0'
}
NSMAPX = {
    'def': 'urn:ietf:params:xml:ns:netconf:base:1.0'
}
PARSER = etree.XMLParser(remove_blank_text=True)
CONFIG_XPATH = etree.XPath('/def:rpc/def:edit-config/def:config', namespaces=NSMAPX)


def pack_edit_config(xml_str, target='running', default_operation='merge'):
    rpc_node = etree.Element('rpc', {"message-id": '101'}, nsmap=NSMAP)
    edit_config_node = etree.Element('edit-config')
    rpc_node.append(edit_config_node)

    target_node = etree.Element('target')
    etree.SubElement(target_node, target)
    edit_config_node.append(target_node)

    default_operation_node = etree.Element('default-operation')
    default_operation_node.text = default_operation
    edit_config_node.append(default_operation_node)

    config_node = etree.fromstring(xml_str, parser=PARSER)
    edit_config_node.append(config_node)

    return etree.tostring(rpc_node, encoding='unicode', pretty_print=True)


def pack(type, xml_str, target='running', default_operation='merge'):
    if type == 'edit-config':
        return pack_edit_config(xml_str, target, default_operation)
    return xml_str


def unpack_edit_config(xml_str):
    rpc_node = etree.fromstring(xml_str, parser=PARSER)
    config_node = CONFIG_XPATH(rpc_node)[0]
    return etree.tostring(config_node, encoding='unicode', pretty_print=True)


def unpack(type, xml_str):
    if type == 'edit-config':
        return unpack_edit_config(xml_str)
    return xml_str


def get_mediator_address():
    candidate_list = [
        '.mediator/plugin.yaml',
        os.path.expanduser('~/.mediator/plugin.yaml'),
        '/etc/mediator/plugin.yaml',
    ]
    for fn in candidate_list:
        if os.path.exists(fn):
            with open(fn) as f:
                data = yaml.safe_load(f)
            break
    else:
        raise RuntimeError('missing mediator config file')

    host = data['mediator_host']
    port = data['mediator_port']
    return host, port


def call_mediator(protocol, type, params, message):
    neid = params['host']
    if neid is None:
        neid = params['provider']['host']

    packed_message = pack(type, message)
    data = {
        'protocol': protocol,
        'neid': neid,
        'message': packed_message,
    }
    host, port = get_mediator_address()
    url = 'http://{}:{}/v1/adaptor/translateMsg'.format(host, port)
    r = requests.post(url, json=data)

    if r.status_code == 200:
        return unpack(type, r.text)
    return message
