from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

yaml_data="""
---
junos_lldp_neighbors_detail_table:
  rpc: get-lldp-neighbors-information
  args:
    interface_name: '[afgx]e*'
  item: lldp-neighbor-information
  key: lldp-local-port-id
  view: junos_lldp_neighbors_detail_view

junos_lldp_neighbors_detail_view:
  fields:
    interface: lldp-local-port-id
    parent_interface: lldp-local-parent-interface-name
    remote_port: lldp-remote-port-id
    remote_chassis_id: lldp-remote-chassis-id
    remote_port: lldp-remote-port-id
    remote_port_description: lldp-remote-port-description
    remote_system_name: lldp-remote-system-name
    remote_system_description: lldp-system-description/lldp-remote-system-description
    remote_system_capab: lldp-remote-system-capabilities-supported
    remote_system_enable_capab: lldp-remote-system-capabilities-enabled
"""

dev = Device(host='111.111.111.111', user='root', password='Juniper')
dev.open()

globals().update(FactoryLoader().load(yaml.load(yaml_data)))

lldp = junos_lldp_neighbors_detail_table(dev)
lldp.get()

# Get list of interfaces
interfaces = lldp.get().keys()

lldp.GET_RPC = 'get-lldp-interface-neighbors'

# Get details of each interface
for interface in interfaces:
        lldp.get(interface)
        for item in lldp:
          print 'Remote system description: ', item.remote_system_description
          print "Remote system capabiltiy:", item.remote_system_capab
          print

dev.close()
