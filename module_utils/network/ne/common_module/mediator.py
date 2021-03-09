import os

import requests
import yaml
from lxml import etree

NSMAP = {
    'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0'
}
PARSER = etree.XMLParser(remove_blank_text=True)
CONFIG_XPATH = etree.XPath('/nc:rpc/nc:edit-config/nc:config', namespaces=NSMAP)
FILTER_XPATH = etree.XPath('/nc:rpc/nc:get-config/nc:filter', namespaces=NSMAP)


def pack_edit_config(xml_str):
    return '''<?xml version="1.0" encoding="UTF-8"?>
    <rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <edit-config>
            <target>
                <running/>
            </target>
            {}
        </edit-config>
    </rpc>
    '''.format(xml_str)


def pack_get_config(xml_str):
    return '''<?xml version="1.0" encoding="UTF-8"?>
    <rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <get-config>
            <target>
                <running/>
            </target>
            {}
        </get-config>
    </rpc>
    '''.format(xml_str)


def pack(type, xml_str):
    if type == 'edit-config':
        return pack_edit_config(xml_str)
    if type == 'get-config':
        return pack_get_config(xml_str)
    raise ValueError('unsupported type {}'.format(type))


def unpack_edit_config(xml_str):
    rpc_node = etree.fromstring(xml_str, parser=PARSER)
    config_node = CONFIG_XPATH(rpc_node)[0]
    return etree.tostring(config_node, encoding='unicode', pretty_print=True)


def unpack_get_config(xml_str):
    rpc_node = etree.fromstring(xml_str, parser=PARSER)
    filter_node = FILTER_XPATH(rpc_node)[0]
    return etree.tostring(filter_node, encoding='unicode', pretty_print=True)


def unpack(type, xml_str):
    if type == 'edit-config':
        return unpack_edit_config(xml_str)
    if type == 'get-config':
        return unpack_get_config(xml_str)
    raise ValueError('unsupported type {}'.format(type))


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
    # 目前只翻译 edit-config
    if type in {'get', 'get-config'}:
        return message

    neid = params.get('host')
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
        translated_message = unpack(type, r.content)
        return translated_message
    return message
