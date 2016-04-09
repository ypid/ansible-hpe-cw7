# HP Networking Comware 7 Ansible Docs
### *Network Automation with HPN and Ansible*

---
### Requirements
* Comware 7 and NETCONF support
* Testing performed on HP 5930s
* pyhpecw7

---
### Modules

  * [comware_ping - ping remote destinations *from* the comware 7 switch](#comware_ping)
  * [comware_vrrp - manages vrrp configurations on a comware v7 device](#comware_vrrp)
  * [comware_file_copy - copy local file to remote comware v7 device](#comware_file_copy)
  * [comware_install_os - copy (if necessary) and install a new operating system on comware v7 device](#comware_install_os)
  * [comware_irf_ports - manages irf port creation and removal for comware v7 devices](#comware_irf_ports)
  * [comware_vxlan - manages vxlan to vsi mappings and tunnel mappings to vxlan](#comware_vxlan)
  * [comware_vlan - manage vlan attributes for comware 7 devices](#comware_vlan)
  * [comware_reboot - perform a reboot of a comware 7 device](#comware_reboot)
  * [comware_irf_members - manages irf membership configuration](#comware_irf_members)
  * [comware_l2vpn_global - manage global config state for l2vpn](#comware_l2vpn_global)
  * [comware_neighbors - retrieves active lldp neighbors (read-only)](#comware_neighbors)
  * [comware_ipinterface - manages ipv4/ipv6 addresses on interfaces](#comware_ipinterface)
  * [comware_switchport - manages layer 2 parameters on switchport interfaces](#comware_switchport)
  * [comware_install_config - activate a new current-running config in realtime](#comware_install_config)
  * [comware_vxlan_tunnel - manages vxlan tunnels on comware 7 devices](#comware_vxlan_tunnel)
  * [comware_command - execute cli commands on comware 7 devices](#comware_command)
  * [comware_interface - manages physical interface attributes](#comware_interface)
  * [comware_facts - gathers facts of comware 7 devices](#comware_facts)
  * [comware_save - save the running configuration](#comware_save)
  * [comware_portchannel - manages port-channel (lag) on comware 7 devices](#comware_portchannel)
  * [comware_vrrp_global - manages vrrp global configuration mode](#comware_vrrp_global)
  * [comware_vxlan_vsi - manages mapping of an ethernet service to a vsi (vxlan id)](#comware_vxlan_vsi)
  * [comware_clean_erase - factory default hp comware 7 device](#comware_clean_erase)

---

## comware_ping
Ping remote destinations *from* the Comware 7 switch

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Ping remote destinations *from* the Comware 7 device.  Really helpful for reachability testing.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   no  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| host  |   yes  |  | <ul></ul> |  IP or name (resolvable by the switch) that you want to ping  |
| vrf  |   no  |  | <ul></ul> |  VRF instance pings should be sourced from  |
| password  |   no  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# test reachability to 8.8.8.8
- comware_ping: host=8.8.8.8 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_vrrp
Manages VRRP configurations on a Comware v7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages VRRP configurations on a Comware v7 device

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| key_type  |   no  |  | <ul> <li>cipher</li>  <li>plain</li> </ul> |  Type of key, i.e. cipher or clear text  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li>  <li>shutdown</li>  <li>undoshutdown</li> </ul> |  Desired state for the interface configuration  |
| vrid  |   yes  |  | <ul></ul> |  VRRP group ID number  |
| preempt  |   no  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Determine preempt mode for the device  |
| auth_mode  |   no  |  | <ul> <li>simple</li>  <li>md5</li> </ul> |  authentication mode for vrrp  |
| priority  |   no  |  | <ul></ul> |  VRRP priority for the device  |
| vip  |   no  |  | <ul></ul> |  Virtual IP to assign within the group  |
| key  |   no  |  | <ul></ul> |  cipher or clear text string  |
| interface  |   yes  |  | <ul></ul> |  Full name of the Layer 3 interface  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# ensure vrid and vrip are configured
- comware_vrrp: vrid=100 vip=100.100.100.1 interface=vlan100 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure vrid 100 is shutdown
- comware_vrrp: vrid=100 interface=vlan100 state=shutdown username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# simple auth w/  plain text key
- comware_vrrp: vrid=100 interface=vlan100 auth_mode=simple key_type=plain key=testkey username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# md5 auth w/ cipher
- comware_vrrp: vrid=100 interface=vlan100 auth_mode=md5 key_type=cipher key='$c$3$d+Pc2DO3clxSA2tC6pe3UBzDEDl1dkE+voI=' username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure vrid 100 on vlan 100 is removed
- comware_vrrp: vrid=100 interface=vlan100 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- When state is set to absent, the vrrp group for a specific interface will be removed (if it exists)

- When state is set to shutdown, the vrrp group for a specific interface will be shutdown. undoshutdown reverses this operation

- When sending a text password, the module is not idempotent because a hash is calculated on the switch. sending a cipher that matches the one configured is idempotent.


---


## comware_file_copy
Copy local file to remote Comware v7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Copy local file to remote Comware v7 device

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| remote_path  |   no  |  flash:/<file>  | <ul></ul> |  Full file path on remote Comware v7 device, e.g. flash:/myfile. If no directory is included, flash will be prepended.  |
| file  |   yes  |  | <ul></ul> |  File (including absolute path of local file) that will be sent to the device  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# copy file
- comware_file_copy: file=/usr/smallfile remote_path=flash:/otherfile username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- If the remote directory doesn't exist, it will be automatically created.


---


## comware_install_os
Copy (if necessary) and install a new operating system on Comware v7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Offers ability to copy and install a new operating system on Comware v7 devices.  Supports using .ipe or .bin system and boot packages.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| delete_ipe  |   no  |  | <ul> <li>true</li>  <li>false</li>  <li>yes</li>  <li>no</li> </ul> |  If ipe_package is used, this specifies whether the .ipe file is deleted from the device after it is unpacked.  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| boot  |   no  |  | <ul></ul> |  File (including abs path) of the boot package (.bin)  |
| system  |   no  |  | <ul></ul> |  File (including abs path) of the system package (.bin)  |
| reboot  |   yes  |  | <ul> <li>true</li>  <li>false</li>  <li>yes</li>  <li>no</li> </ul> |  Determine if the reboot should take place after device startup software image is configured  |
| delay  |   no  |  | <ul></ul> |  If reboot is set to yes, this is the delay in minutes to wait before rebooting.  |
| remote_dir  |   no  |  flash:/  | <ul></ul> |  The remote directory into which the file(s) would be copied. See default.  |
| ipe_package  |   no  |  | <ul></ul> |  File (including abs path path) of the ipe package.  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 

#### Notes

- The parameters ipe_package and boot/system are mutually exclusive.

- If the files are not currently on the device, the will be transfered to the device.


---


## comware_irf_ports
Manages IRF port creation and removal for Comware v7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages IRF port creation and removal for Comware v7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| activate  |   no  |  True  | <ul> <li>true</li>  <li>false</li>  <li>yes</li>  <li>no</li> </ul> |  activate the IRF after the configuration is initially performed  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| irf_p2  |   yes  |  | <ul></ul> |  Physical Interface or List of Physical Interfaces that will be bound to IRF port 2. Any physical interfaces not in the list will be removed from the IRF port. An empty list removes all interfaces.  |
| irf_p1  |   yes  |  | <ul></ul> |  Physical Interface or List of Physical Interfaces that will be bound to IRF port 1. Any physical interfaces not in the list will be removed from the IRF port. An empty list removes all interfaces.  |
| member_id  |   yes  |  | <ul></ul> |  IRF member id for switch (must be unique). IRF member ids can be configured with the comware_irf_members module.  |
| filename  |   no  |  startup.cfg  | <ul></ul> |  Where to save the current configuration. Default is startup.cfg.  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| removal_override  |   no  |  False  | <ul> <li>true</li>  <li>false</li>  <li>yes</li>  <li>no</li> </ul> |  When set to true, allows the removal of physical ports from IRF port(s). Removing physical ports may have adverse effects and be disallowed by the switch. Disconnecting all IRF ports could lead to a split-brain scenario.  |


 
#### Examples

```

   # irf ports
   - comware_irf_ports:
      member_id: 1
      irf_p1:
        - FortyGigE1/0/1
        - FortyGigE1/0/3
      irf_p2: FortyGigE1/0/2
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      removal_override: yes


```


#### Notes

- This module is meant to be run after the comware_irf_members module.

- Any physical interfaces not in an interface list (irf_p1 or irf_p2) will be removed from the IRF port. An empty list removes all interfaces.

- If an IRF is succesfully created, the non-master members will no longer be accessible through their management interfaces.

- The process is as follows 1) Use comware_irf_members to change the IRF member identity of the device. 2) Use the reboot=true flag or reboot the device through some other means. 3) Use the comware_irf_ports module to create IRF port to physical port bindings. 4) In that module set activate=true to activate the IRF. If IRF neighbors are already configured, the IRF will be formed, some devices may reboot.


---


## comware_vxlan
Manages VXLAN to VSI mappings and Tunnel mappings to VXLAN

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages VXLAN to VSI mappings and Tunnel mappings to VXLAN

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| descr  |   yes  |  | <ul></ul> |  description of the VSI  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| tunnels  |   no  |  | <ul></ul> |  Desired Tunnel interface ID or a list of IDs. Any tunnel not in the list will be removed if it exists  |
| vsi  |   yes  |  | <ul></ul> |  Name of the VSI  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| vxlan  |   yes  |  | <ul></ul> |  VXLAN that will be mapped to the VSI  |


 
#### Examples

```

# ensure VXLAN and VSI do not exist
- comware_vxlan: vxlan=100 vsi=VSI_VXLAN_100 tunnels=20 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


# ensure VXLAN 100 exists and is mapped to VSI VSI_VXLAN_100 with only tunnel interface 20
- comware_vxlan: vxlan=100 vsi=VSI_VXLAN_100 tunnels=20 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure 3 tunnels mapped to the vxlan
- comware_vxlan:
    vxlan: 100
    vsi: VSI_VXLAN_100
    tunnels: ['20', '21', '22']
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"


```


#### Notes

- VXLAN tunnels should be created before using this module.

- state=absent removes the vsi and associated vxlan mapping if they both exist.

- Remember that is a 1 to 1 mapping between vxlan IDs and VSIs


---


## comware_vlan
Manage VLAN attributes for Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manage VLAN attributes for Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| name  |   no  |  | <ul></ul> |  Name to configure for the specified VLAN ID  |
| descr  |   no  |  | <ul></ul> |  Description for the VLAN  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| vlanid  |   yes  |  | <ul></ul> |  VLAN ID to configure  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# ensure VLAN 10 exists
- comware_vlan: vlanid=10 name=VLAN10_WEB descr=LOCALSEGMENT state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# update name and descr
- comware_vlan: vlanid=10 name=WEB10 descr=WEBDESCR state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure VLAN 10 does not exist
- comware_vlan: vlanid=10 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_reboot
Perform a reboot of a Comware 7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Offers ability to reboot Comware 7 devices instantly at a scheduled time, or after a given period of time

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   no  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| reboot  |   yes  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Needs to be set to true to reboot the device  |
| delay  |   no  |  | <ul></ul> |  Delay (in minutes) to wait to reboot the device  |
| time  |   no  |  | <ul></ul> |  Specify the time at which the reboot will take place. Format should be HH:MM enclosed in quotes.  |
| date  |   no  |  | <ul></ul> |  Specify the date at which the reboot will take place. The time parameter is required to use this parameter. Format should be MM/DD/YYYY in quotes.  |
| password  |   no  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# name: reboot immedidately
- comware_reboot: reboot=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot at 5:00
- comware_reboot: reboot=true time="05:00" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot in 5 minutes
- comware_reboot: reboot=true delay="05:00" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# name: reboot at 22:00 on July 30 2015
- comware_reboot: reboot=true time="22:00" date="07/10/2015" username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- Time/date and delay are mutually exclusive parameters

- Time is required when specifying date

- Reboot must be set to true to reboot the device

- This module is not idempotent


---


## comware_irf_members
Manages IRF membership configuration

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages IRF member configuration.
 This module should be used before the comware_irf_ports module.
 The process is as follows 1) Use comware_irf_members to change the IRF member identity of the device. 2) Use the reboot=true flag or reboot the device through some other means. 3) Use the comware_irf_ports module to create IRF port to physical port bindings. 4) In that module set activate=true to activate the IRF. If IRF neighbors are already configured, the IRF will be formed, some devices may reboot.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| priority  |   no  |  | <ul></ul> |  The desired IRF priority for the switch.  |
| descr  |   no  |  False  | <ul></ul> |  The text description of the IRF member switch.  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state of the interfaces listed in mad_exclude  |
| auto_update  |   no  |  | <ul> <li>enable</li>  <li>disable</li> </ul> |  Whether software autoupdate should be enabled for the fabric.  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| reboot  |   yes  |  False  | <ul></ul> |  Whether to reboot the switch after member changes are made.  |
| new_member_id  |   no  |  | <ul></ul> |  The desired IRF member ID for the switch. The new member ID takes effect after a reboot.  |
| mad_exclude  |   no  |  | <ul></ul> |  Interface or list of interfaces that should be excluded from shutting down in a recovery event.  |
| member_id  |   yes  |  | <ul></ul> |  Current IRF member ID of the switch. If the switch has not been configured for IRF yet, this should be 1.  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

  # irf members
  - comware_irf_members:
      member_id: 9
      state: present
      auto_update: disable
      mad_exclude:
        - FortyGigE9/0/30
        - FortyGigE9/0/23
        - FortyGigE9/0/24
      priority: 4
      descr: My description
      reboot: no
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"


```


#### Notes

- When state=absent, the interfaces in mad_exclude will be removed if present. Other parameters will be ignored.


---


## comware_l2vpn_global
Manage global config state for L2VPN

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Enable or Disable L2VPN on a HP Comware 7 device

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| state  |   yes  |  | <ul> <li>enabled</li>  <li>disabled</li> </ul> |  Desired state for l2vpn global configuration  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# enable l2vpn globally
- comware_l2vpn_global: state=enabled username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_neighbors
Retrieves active LLDP neighbors (read-only)

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Retrieves active LLDP neighbors (read-only)

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| neigh_type  |   no  |  lldp  | <ul> <li>lldp</li>  <li>cdp</li> </ul> |  type of neighbors  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# get lldp neighbors
- comware_neighbors: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_ipinterface
Manages IPv4/IPv6 addresses on interfaces

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages IPv4/IPv6 addresses on interfaces

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| name  |   yes  |  | <ul></ul> |  Full name of the interface  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| mask  |   yes  |  | <ul></ul> |  The network mask, in dotted decimal or prefix length notation. If using IPv6, only prefix length is supported.  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state of the switchport  |
| version  |   yes  |  v4  | <ul> <li>v4</li>  <li>v6</li> </ul> |  v4 for IPv4, v6 for IPv6  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| addr  |   yes  |  | <ul></ul> |  The IPv4 or IPv6 address of the interface  |


 
#### Examples

```

# Basic IPv4 config
- comware_ipinterface: name=FortyGigE1/0/3 addr=192.168.3.5 mask=255.255.255.0 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Basic IPv6 config
- comware_ipinterface: version=v6 name=FortyGigE1/0/3 addr=2001:DB8::1 mask=10 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- If the interface is not configured to be a layer 3 port, the module will fail and the user should use the interface module to convert the interface with type=routed

- If state=absent, the specified IP address will be removed from the interface. If the existing IP address doesn't match the specified, the existing will not be removed.


---


## comware_switchport
Manages Layer 2 parameters on switchport interfaces

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages Layer 2 parameters on switchport interfaces

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| name  |   yes  |  | <ul></ul> |  Full name of the interface  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| pvid  |   no  |  | <ul></ul> |  If link_type is set to trunk this will be used as the native native VLAN ID for that trunk. If link_type is set to access then this is the VLAN ID of the interface.  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state of the switchport  |
| permitted_vlans  |   no  |  | <ul></ul> |  If mode is set to trunk this will be the complete list/range of VLANs allowed on that trunk interface. Any VLAN not in the list will be removed from the interface.  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| link_type  |   yes  |  | <ul> <li>access</li>  <li>trunk</li> </ul> |  Layer 2 mode of the interface  |


 
#### Examples

```

# Basic access config
- comware_switchport: name=FortyGigE1/0/2 link_type=access username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# Basic trunk config
- comware_switchport: name=FortyGigE1/0/2 link_type=trunk username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- If the interface is configured to be a Layer 3 port, the module will fail and ask the user to use the comware_interface module to convert it to be a Layer 2 port first.

- If the interface is a member in a LAG, the module will fail telling the user changes hould be made to the LAG interface

- If VLANs are trying to be assigned that are not yet created on the switch, the module will fail asking the user to create them first.

- If state=default, the switchport settings will be defaulted. That means it will be set as an access port in VLAN 1.


---


## comware_install_config
Activate a new current-running config in realtime

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Activate a new current-running config in realtime

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| config_file  |   yes  |  | <ul></ul> |  File that will be sent to the device.  Relative path is location of Ansible playbook.  Recommended to use absolute path.  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| diff_file  |   no  |  | <ul></ul> |  File that will be used to store the diffs.  Relative path is location of ansible playbook. If not set, no diffs are saved.  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| commit_changes  |   yes  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Used to determine the action to take after transferring the config to the switch.  Either activate using the rollback feature or load on next-reboot.  |


 
#### Examples

```

# install config file that will be the new running config
- comware_install_config:
    config_file='/home/ansible/projects/pyhpecw7comware/newconfig.cfg'
    diff_file='/home/ansible/projects/pyhpecw7comware/diffs.diff'
    commit_changes=true
    username={{ username }}
    password={{ password }}
    hostname={{ inventory_hostname }}


```


#### Notes

- Check mode copies config file to device and still generates diffs

- diff_file must be specified to write diffs to a file, otherwise, only summarized diffs are returned from the module

- commit_changes must be true to apply changes

- this module does an automatic backup of the existing config to the filename flash:/safety_file.cfg

- this module does an auto save to flash:/startup.cfg upon completion

- config_file MUST be a valid FULL config file for a given device.


---


## comware_vxlan_tunnel
Manages VXLAN tunnels on Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages VXLAN tunnels on Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| global_src  |   no  |  | <ul></ul> |  Global source address for VXLAN tunnels  |
| src  |   no  |  | <ul></ul> |  Source address or interface for the tunnel  |
| tunnel  |   yes  |  | <ul></ul> |  Tunnel interface identifier  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| dest  |   no  |  | <ul></ul> |  Destination address for the tunnel  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# ensure tunnel interface 20 exists for vxlan and configures a global source address (although it's not used here)
- comware_vxlan_tunnel: tunnel=20 global_src=10.10.10.10 src=10.1.1.1 dest=10.1.1.2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure tunnel interface 21
- comware_vxlan_tunnel: tunnel=21 src=10.1.1.1 dest=10.1.1.2 username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure tunnel interface 21 does not exist (does not have to be a vxlan tunnel)
- comware_vxlan_tunnel: tunnel=21 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- state=absent removes the tunnel interface if it exists

- state=absent can also remove non-vxlan tunnel interfaces


---


## comware_command
Execute CLI commands on Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Execute CLI commands on Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   no  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| command  |   yes  |  | <ul></ul> |  String (single command) or list of commands to be executed on the device.  Sending a list requires YAML format to be used in the playbook.  |
| password  |   no  |  | <ul></ul> |  Password used to login to the switch  |
| type  |   yes  |  | <ul> <li>display</li>  <li>config</li>  <li>show</li> </ul> |  State whether the commands are display (user view) or configure (system view) commands.  Display and show are the same thing.  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# display vlan 10 passing in a string
- comware_command: command='display vlan 5' type=display username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# display vlans passing in a list
- comware_command:
    command:
      - display vlan 10
      - display vlan 5
    type: display
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"

# passing in config commands as a list
- comware_command:
    command:
      - vlan 5
      - name web_vlan
    type: config
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"


```


#### Notes

- This module is not idempotent


---


## comware_interface
Manages physical interface attributes

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages administrative state and physical attributes of the interface

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| name  |   yes  |  | <ul></ul> |  Full name of the interface  |
| admin  |   no  |  up  | <ul> <li>up</li>  <li>down</li> </ul> |  Admin state of the interface  |
| speed  |   no  |  | <ul></ul> |  Speed of the interface in Mbps  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| duplex  |   no  |  | <ul> <li>auto</li>  <li>full</li> </ul> |  Duplex of the interface  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li>  <li>default</li> </ul> |  Desired state for the interface configuration  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| type  |   no  |  | <ul> <li>bridged</li>  <li>routed</li> </ul> |  Type of interface, i.e. L2 or L3  |
| port  |   no  |  830  | <ul></ul> |  The Comware port used to connect to the switch  |
| description  |   no  |  | <ul></ul> |  Single line description for the interface  |


 

#### Notes

- Only logical interfaces can be removed with state=absent.

- If you want to configure type, run this module first with no other interface parameters. Then, remove the type parameter and include the other desired parameters. The type parameter defaults the other parameters.

- When state is set to default, the interface will be "defaulted" regardless of what other parameters are entered.

- When state is set to default, the interface must already exist.

- When state is set to absent, logical interfaces will be removed from the switch, while physical interfaces will be "defaulted"

- Tunnel interface creation and removal is not currently supported.


---


## comware_facts
Gathers facts of Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Gathers fact data (characteristics) of Comware 7 devices

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   no  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   no  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# get facts
- comware_facts: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_save
Save the running configuration

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Save the running configuration

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| filename  |   no  |  startup.cfg  | <ul></ul> |  Name of file that will be used when saving the current running conifg to flash.  |


 
#### Examples

```

# save as myfile.cfg (in flash)
- comware_save: filename=myfile.cfg username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# save as startup.cfg (in flash)
- comware_save: username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- This modules saves the running config as startup.cfg in flash. or YOUR_FILENAME, which will also be saved to flash.  It is not changing the config file to load on next-boot.


---


## comware_portchannel
Manages port-channel (LAG) on Comware 7 devices

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages routed and bridged aggregation configurations on Comware 7 devices.  This includes physical interface configs for LACP.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| min_ports  |   no  |  | <ul></ul> |  Minimum number of selected ports for the agg group  |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| group  |   yes  |  | <ul></ul> |  Group number to identify the Aggregate interface  |
| max_ports  |   no  |  | <ul></ul> |  Maximum number of selected ports for the agg group  |
| lacp_mode  |   no  |  active  | <ul> <li>active</li>  <li>passive</li> </ul> |  If mode is set to LACP, the type operating mode can be selected. This  mode will then be set for all members in the group.  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| mode  |   no  |  dynamic  | <ul> <li>static</li>  <li>dynamic</li> </ul> |  Mode of the Aggregate interface  |
| members  |   no  |  | <ul></ul> |  COMPLETE Interface List that should be in the agg group. Full names should be used AND Interface names ARE case sensitive. For example, FortyGigE1/0/1 should NOT be written as fortygige1/0/1.  This is for safety.  |
| lacp_edge  |   no  |  | <ul> <li>enabled</li>  <li>disabled</li> </ul> |  Determine if an LACP agg group should be an edge aggregate interface  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| type  |   yes  |  | <ul> <li>bridged</li>  <li>routed</li> </ul> |  Type of the Aggregate interface (L2 or L3)  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

  # Portchannel config
  - comware_portchannel:
      group: 100
      members:
        - FortyGigE1/0/27
        - FortyGigE1/0/28
        - FortyGigE1/0/29
        - FortyGigE1/0/30
      type: routed
      mode: static
      min_ports: 2
      max_ports: 4
      username: "{{ username }}"
      password: "{{ password }}"
      hostname: "{{ inventory_hostname }}"
      state: present


```


#### Notes

- When configuring a LAGG, the members param must be included

- Members is ALL members - it is ensuring that the members sent is the full list of all members.  This means to remove a member it just needs to be removed from the members list.

- When removing a LAGG, members is not required

- If mode is set to static, lacp_edge and lacp_mode are disregarded if those params are set


---


## comware_vrrp_global
Manages VRRP global configuration mode

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages VRRP global configuration mode

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| mode  |   yes  |  | <ul> <li>standard</li>  <li>load-balance</li> </ul> |  vrrp config mode for the switch  |


 
#### Examples

```

# configure load-balance mode
- comware_vrrp_global: mode=load-balance username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


## comware_vxlan_vsi
Manages mapping of an Ethernet Service to a VSI (VXLAN ID)

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Manages the mapping of an Ethernet Service to a VSI (VXLAN ID)

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware v7 device that has NETCONF enabled  |
| vlanid  |   no  |  | <ul></ul> |  If encap is set to only-tagged or s-vid, vlanid must be set.  |
| instance  |   yes  |  | <ul></ul> |  Service instance id  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  Desired state for the interface configuration  |
| encap  |   no  |  default  | <ul> <li>default</li>  <li>tagged</li>  <li>untagged</li>  <li>only-tagged</li>  <li>s-vid</li> </ul> |  only-tagged also ensures s-vid  |
| interface  |   yes  |  | <ul></ul> |  Layer 2 interface or bridged-interface  |
| vsi  |   no  |  | <ul></ul> |  Name of the VSI  |
| access_mode  |   no  |  vlan  | <ul> <li>ethernet</li>  <li>vlan</li> </ul> |  Mapping Ethernet service instance to a VSI using Ethernet or VLAN mode (options for xconnect command)  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# ensure the vsi is not mapped to the instance
- comware_vxlan_vsi: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_vsi: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=default access_mode=vlan username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_vsi: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=tagged access_mode=ethernet username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

# ensure instance and vsi and configured with encap and access mode as specified
- comware_vxlan_vsi: interface=Fo1/0/32 vsi=VSI_VXLAN_100 instance=100 encap=only-tagged vlanid=10 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```


#### Notes

- VSI needs to be created before using this module (comware_vxlan)

- encap and xconnect access_mode cannot be altered once set to change, use state=absent and re-configure

- state=absent removes the service instance for specified interface if if it exists

- This should be the last VXLAN module used after comware_vxlan_tunnel, and comware_vxlan.


---


## comware_clean_erase
Factory default HP Comware 7 device

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Reset system to factory default settings.  You will lose connectivity to the switch.  This module deletes all configuration files (.cfg files) in the root directories of the storage media. It Deletes all log files (.log files in the folder /logfile). Clears all log information (in the log buffer), trap information, and debugging information. Restores the parameters for the Boot ROM options to the factory-default settings. Deletes all files on an installed hot-swappable storage medium, such as a USB disk

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | <ul></ul> |  Username used to login to the switch  |
| password  |   yes  |  | <ul></ul> |  Password used to login to the switch  |
| factory_default  |   yes  |  | <ul> <li>true</li>  <li>false</li> </ul> |  Set to true if all logs and user-created files should be deleted and removed from the system and the device should be set to factory default settings  |
| hostname  |   yes  |  | <ul></ul> |  IP Address or hostname of the Comware 7 device that has NETCONF enabled  |
| port  |   yes  |  830  | <ul></ul> |  NETCONF port number  |


 
#### Examples

```

# factory default and reboot immediately
- comware_clean_erase: factory_default=true username={{ username }} password={{ password }} hostname={{ inventory_hostname }}


```



---


---
Created by Network to Code, LLC
For:
2015
