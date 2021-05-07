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
    if type == 'get-config' or type == 'get':
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
    if type == 'get-config' or type == 'get':
        return unpack_get_config(xml_str)
    if type == 'rpc-reply':
        return unpack_rpc_reply(xml_str)
    raise ValueError('unsupported type {}'.format(type))


def get_configdata():
    candidate_list = [
        '.mediator/plugin.yml',
        '.mediator/plugin.yaml',
        os.path.expanduser('~/.mediator/plugin.yml'),
        os.path.expanduser('~/.mediator/plugin.yaml'),
        '/etc/mediator/plugin.yml',
        '/etc/mediator/plugin.yaml',
    ]
    for fn in candidate_list:
        if os.path.exists(fn):
            with open(fn) as f:
                data = yaml.safe_load(f)
            break
    else:
        raise RuntimeError('missing mediator config file')

    return data


def get_neid(params):
    neid = params.get('host')
    if neid is None:
        neid = params['provider']['host']
    return neid


def call_mediator(protocol, type, params, message, *, do_log=True):
    # 目前只翻译部分报文
    if type not in {'edit-config', 'get', 'get-config', 'rpc-reply'}:
        return message

    dt = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    logdir = Path(os.path.expanduser('~/test'))

    if type == 'rpc-reply' and '<data' not in message:
        if do_log:
            (logdir / (dt + '-' + type + '-raw_msg.xml')).write_text(message)
        return message

    packed_message = pack(type, message)
    if do_log:
        (logdir / (dt + '-' + type + '-packed_msg.xml')).write_text(packed_message)

    neid = get_neid(params)
    data = {
        'protocol': protocol,
        'neid': neid,
        'message': packed_message,
    }
    configdata = get_configdata()
    host = configdata['mediator_host']
    port = configdata['mediator_port']
    url = 'http://{}:{}/v1/adaptor/translateMsg'.format(host, port)
    r = requests.post(url, json=data)

    if r.status_code == 200:
        translated_message = unpack(type, r.content)
        if do_log:
            (logdir / (dt + '-' + type + '-translated_msg.xml')).write_text(translated_message)
        return translated_message
    return message


class Datastore:
    api_list = [
        'set_controller_config',
        'set_device_config',
        'update_controller_config',
        'update_device_config',
    ]

    def __init__(self):
        config = get_configdata()
        host = config['mediator_controller_host']
        port = config['mediator_controller_port']
        self.base_url = 'http://{}:{}/v1/datastore/'.format(host, port)

    def _make_url(self, api):
        return self.base_url + api

    def set_controller_config(self, params, module, message):
        neid = get_neid(params)
        data = {
            'neid': neid,
            'source': 'running',
            'module': module,
            'data': message,
        }
        url = self._make_url('set_controller_config')
        r = requests.post(url, json=data)

        if r.status_code == 200:
            pass

    def set_device_config(self, params, module, message):
        neid = get_neid(params)
        data = {
            'neid': neid,
            'source': 'running',
            'module': module,
            'data': message,
        }
        url = self._make_url('set_device_config')
        r = requests.post(url, json=data)

        if r.status_code == 200:
            pass

    def update_controller_config(self, params, module, message):
        neid = get_neid(params)
        data = {
            'neid': neid,
            'source': 'running',
            'module': module,
            'data': message,
        }
        url = self._make_url('update_controller_config')
        r = requests.post(url, json=data)

        if r.status_code == 200:
            pass

    def update_device_config(self, params, module, message):
        neid = get_neid(params)
        data = {
            'neid': neid,
            'source': 'running',
            'module': module,
            'data': message,
        }
        url = self._make_url('update_device_config')
        r = requests.post(url, json=data)

        if r.status_code == 200:
            pass


datastore = Datastore()
