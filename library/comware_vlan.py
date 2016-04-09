#!/usr/bin/python


DOCUMENTATION = """
---

module: comware_vlan
short_description: Manage VLAN attributes for Comware 7 devices
description:
    - Manage VLAN attributes for Comware 7 devices
version_added: 1.8
category: Feature (RW)
options:
    vlanid:
        description:
            - VLAN ID to configure
        required: true
        default: null
        choices: []
        aliases: []
    name:
        description:
            - Name to configure for the specified VLAN ID
        required: false
        default: null
        choices: []
        aliases: []
    descr:
        description:
            - Description for the VLAN
        required: false
        default: null
        choices: []
        aliases: []
    port:
        description:
            - NETCONF port number
        required: false
        default: 830
        choices: []
        aliases: []
    hostname:
        description:
            - IP Address or hostname of the Comware v7 device that has
              NETCONF enabled
        required: true
        default: null
        choices: []
        aliases: []
    username:
        description:
            - Username used to login to the switch
        required: true
        default: null
        choices: []
        aliases: []
    password:
        description:
            - Password used to login to the switch
        required: true
        default: null
        choices: []
        aliases: []
    state:
        description:
            - Desired state of the vlan
        required: false
        default: present
        choices: ['present', 'absent']
        aliases: []

"""
EXAMPLES = """

# ensure VLAN 10 exists
- comware_vlan: vlanid=10 name=VLAN10_WEB descr=LOCALSEGMENT state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# update name and descr
- comware_vlan: vlanid=10 name=WEB10 descr=WEBDESCR state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure VLAN 10 does not exist
- comware_vlan: vlanid=10 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

"""

import socket
try:
    HAS_PYHP = True
    from pyhpecw7.features.vlan import Vlan
    from pyhpecw7.comware import HPCOM7
    from pyhpecw7.features.errors import *
    from pyhpecw7.errors import *
except ImportError as ie:
    HAS_PYHP = False


def safe_fail(module, device=None, **kwargs):
    if device:
        device.close()
    module.fail_json(**kwargs)


def safe_exit(module, device=None, **kwargs):
    if device:
        device.close()
    module.exit_json(**kwargs)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlanid=dict(required=True, type='str'),
            name=dict(required=False),
            descr=dict(required=False),
            state=dict(choices=['present', 'absent'], default='present'),
            port=dict(default=830, type='int'),
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=True),
        ),
        supports_check_mode=True
    )
    if not HAS_PYHP:
        module.fail_json(msg='There was a problem loading from the pyhpecw7 '
                         + 'module.', error=str(ie))

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    hostname = socket.gethostbyname(module.params['hostname'])

    device_args = dict(host=hostname, username=username,
                       password=password, port=port)

    device = HPCOM7(**device_args)

    vlanid = module.params['vlanid']
    name = module.params['name']
    descr = module.params['descr']

    state = module.params['state']

    changed = False

    args = dict(vlanid=vlanid, name=name, descr=descr)
    proposed = dict((k, v) for k, v in args.iteritems() if v is not None)

    try:
        device.open()
    except ConnectionError as e:
        safe_fail(module, device, msg=str(e))

    try:
        vlan = Vlan(device, vlanid)
        vlan.param_check(**proposed)
    except LengthOfStringError as lose:
        safe_fail(module, device, msg=str(lose))
    except VlanIDError as vie:
        safe_fail(module, device, msg=str(vie))
    except PYHPError as e:
        safe_fail(module, device, msg=str(e))

    try:
        existing = vlan.get_config()
    except PYHPError as e:
        safe_fail(module, device, msg=str(e),
                  descr='error getting vlan config')

    if state == 'present':
        delta = dict(set(proposed.iteritems()).difference(
            existing.iteritems()))
        if delta:
            vlan.build(stage=True, **delta)
    elif state == 'absent':
        if existing:
            vlan.remove(stage=True)

    commands = None
    end_state = existing

    if device.staged:
        commands = device.staged_to_string()
        if module.check_mode:
            device.close()
            safe_exit(module, device, changed=True,
                      commands=commands)
        else:
            try:
                device.execute_staged()
                end_state = vlan.get_config()
            except PYHPError as e:
                safe_fail(module, device, msg=str(e),
                          descr='error during execution')
            changed = True

    results = {}
    results['proposed'] = proposed
    results['existing'] = existing
    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state

    safe_exit(module, device, **results)

from ansible.module_utils.basic import *
main()
