import argparse
from napalm import get_network_driver
from prettytable import PrettyTable
import getpass
parser = argparse.ArgumentParser(description='script for gathering interfaces data from a router')
parser.add_argument('--device')
parser.add_argument('--username')
args = parser.parse_args()

def get_password():
    password = getpass.getpass('Enter Password ')
    return password

def main():
    password = get_password()
    mx_router = get_network_driver('junos')
    router = mx_router(hostname=args.device,username=args.username,password=password)
    router.open()
    if not router.is_alive():
        print 'router is not alive'
    else:
        header = ['Interface', 'Description', 'Last Flapped', 'Status', 'MAC Address', 'Speed']
        table = PrettyTable(header)
        interfaces = router.get_interfaces()
        for i in interfaces:
            port = i
            desc =  interfaces[i]['description']
            flap = interfaces[i]['last_flapped']
            state =  interfaces[i]['is_up']
            mac =  interfaces[i]['mac_address']
            speed = interfaces[i]['speed']
            table.add_row([port,desc,flap,state,mac,speed])
        print table
if __name__ == '__main__':
    main()
