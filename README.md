# Developer Tutorial

## Prerequisites

- Python >= 3.6
- Ansible == 2.9.9
- ncclient

```
pip3 install ansible==2.9.9 ncclient
```

## Installation

Download code:

```
git clone https://github.com/icanlab/mediator-ne-plugin.git
```

Set shell variable `ansible_path` and `ncclient_path`, and run script:

```
cd mediator-ne-plugin
./install.sh
```

## Configuration

Some arguments should be given in the config file `.mediator/plugin.yml` or `~/.mediator/plugin.yml`.

The following is a example:

```yaml
---
mediator_host: 127.0.0.1
mediator_port: 8080
mediator_controller_host: 127.0.0.1
mediator_controller_port: 8089
```

All the four arguments are required.
