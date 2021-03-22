import os
from datetime import datetime
from pathlib import Path

import requests
import yaml
from lxml import etree

NSMAP = {
    'a': 'urn:ietf:params:xml:ns:netconf:base:1.0'
}
PARSER = etree.XMLParser(remove_blank_text=True)
CONFIG_XPATH = etree.XPath('/a:rpc/a:edit-config/a:config', namespaces=NSMAP)
FILTER_XPATH = etree.XPath('/a:rpc/a:get-config/a:filter', namespaces=NSMAP)
DATA_XPATH = etree.XPath('/a:rpc-reply/a:data', namespaces=NSMAP)


def pack_edit_config(xml_str):
    return '''<?xml version="1.0" encoding="UTF-8"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <edit-config>
        <target>
            <running/>
        </target>
        {}
    </edit-config>
</rpc>'''.format(xml_str)


def pack_get_config(xml_str):
    return '''<?xml version="1.0" encoding="UTF-8"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <get-config>
        <source>
            <running/>
        </source>
        {}
    </get-config>
</rpc>'''.format(xml_str)


def pack_rpc_reply(xml_str):
    xml_str = xml_str.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
    return '''<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    {}
</rpc-reply>'''.format(xml_str)


def pack(type, xml_str):
    if type == 'edit-config':
        return pack_edit_config(xml_str)
    if type == 'get-config':
        return pack_get_config(xml_str)
    if type == 'rpc-reply':
        return pack_rpc_reply(xml_str)
    raise ValueError('unsupported type {}'.format(type))


def unpack_edit_config(xml_str):
    rpc_node = etree.fromstring(xml_str, parser=PARSER)
    config_node = CONFIG_XPATH(rpc_node)[0]
    foo = etree.tostring(config_node, encoding='unicode', pretty_print=True)
    return foo.replace(' xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '')


def unpack_get_config(xml_str):
    rpc_node = etree.fromstring(xml_str, parser=PARSER)
    filter_node = FILTER_XPATH(rpc_node)[0]
    foo = etree.tostring(filter_node, encoding='unicode', pretty_print=True)
    return foo.replace(' xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '')


def unpack_rpc_reply(xml_str):
    rpc_node = etree.fromstring(xml_str, parser=PARSER)
    data_node = DATA_XPATH(rpc_node)[0]
    foo = etree.tostring(data_node, encoding='unicode', pretty_print=True)
    return foo.replace(' xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '')


def unpack(type, xml_str):
    if type == 'edit-config':
        return unpack_edit_config(xml_str)
    if type == 'get-config':
        return unpack_get_config(xml_str)
    if type == 'rpc-reply':
        return unpack_rpc_reply(xml_str)
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


def get_neid(params):
    neid = params.get('host')
    if neid is None:
        neid = params['provider']['host']
    return neid


def call_mediator(protocol, type, params, message):
    # 目前只翻译部分报文
    if type not in {'edit-config', 'get-config', 'rpc-reply'}:
        return message

    dt = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    logdir = Path(os.path.expanduser('~/test'))

    if type == 'rpc-reply' and '<data' not in message:
        (logdir / (dt + '-' + type + '-raw_msg.xml')).write_text(message)
        return message

    packed_message = pack(type, message)
    (logdir / (dt + '-' + type + '-packed_msg.xml')).write_text(packed_message)

    neid = get_neid(params)
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
        (logdir / (dt + '-' + type + '-translated_msg.xml')).write_text(translated_message)
        return translated_message
    return message
