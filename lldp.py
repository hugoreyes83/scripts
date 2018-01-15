from jnpr.junos import Device
from jnpr.junos.op.lldp import LLDPNeighborTable
import json

device = Device(host='111.111.111.111', user='root', password='Juniper')
device.open()
neighbors = LLDPNeighborTable(device)
neighbors.get()
output_json = json.loads(neighbors.to_json())
for i in output_json:
    print 'local interface is ' + str(i) + ' and remote interface is ' + output_json[i]['remote_port_id']
