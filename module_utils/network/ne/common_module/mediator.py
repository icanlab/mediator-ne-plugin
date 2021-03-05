import os

import requests
import yaml


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


def call_mediator(protocol, params, message):
    neid = params['host']
    if neid is None:
        neid = params['provider']['host']

    data = {
        'protocol': protocol,
        'neid': neid,
        'message': message,
    }
    host, port = get_mediator_address()
    url = 'http://{}:{}/v1/adaptor/translateMsg'.format(host, port)
    r = requests.post(url, json=data)

    if r.status_code == 200:
        return r.text
    return message
