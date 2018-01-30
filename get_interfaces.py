import argparse
import datetime
from napalm import get_network_driver
from prettytable import PrettyTable
import getpass
import re
from jnpr.junos.exception import ConnectAuthError
from jnpr.junos.exception import ConnectRefusedError
from jnpr.junos.exception import ConnectTimeoutError
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import PermissionError

parser = argparse.ArgumentParser(description='script for gathering interfaces data from a router')
parser.add_argument('--device',required=True)
parser.add_argument('--username',required=True)
args = parser.parse_args()

def get_password():
    password = getpass.getpass('Enter Password ')
    return password

def main():
    try:
        password = get_password()
        mx_router = get_network_driver('junos')
        router = mx_router(hostname=args.device,username=args.username,password=password)
        router.open()
        if not router.is_alive():
            print 'router is not alive'
        else:
            header = ['Interface', 'Description', 'Last Flapped', 'Status', 'MAC Address', 'Speed', 'LLDP Neighbor', 'Remote Interface']
            table = PrettyTable(header)
            interfaces = router.get_interfaces()
            lldp_neighbors = router.get_lldp_neighbors()
            list_of_lldp_interfaces = []
            for i in lldp_neighbors:
                list_of_lldp_interfaces.append(i)
            for i in interfaces:
                match_ge_interfaces = re.match(r'(^ge-*)', i)
                if match_ge_interfaces:
                    port = i
                    desc =  interfaces[i]['description']
                    flap = str(datetime.timedelta(seconds=interfaces[i]['last_flapped']))
                    if interfaces[i]['is_up'] == True:
                        state = 'UP'
                    else:
                        state = 'DOWN' 
                    mac =  interfaces[i]['mac_address']
                    speed = interfaces[i]['speed']
                    if i in list_of_lldp_interfaces:
                        lldp_neighbor =  lldp_neighbors[i][0]['hostname']
                        lldp_port = lldp_neighbors[i][0]['port']
                        table.add_row([port,desc,flap,state,mac,speed,lldp_neighbor,lldp_port])
                    else:
                        table.add_row([port,desc,flap,state,mac,speed,'No lldp neighbor','N/A'])
                else:
                    continue
            print table
    except ConnectAuthError as e:
        print e
    except ConnectRefusedError as e:
        print e
    except ConnectTimeoutError as e:
        print e
    except ConnectError as e:
        print e
    except PermissionError as e:
        print e
if __name__ == '__main__':
    main()

