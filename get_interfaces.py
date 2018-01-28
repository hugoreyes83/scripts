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
        for i in router.get_interfaces():
            table.add_row([router.get_interfaces()[i],router.get_interfaces()[i]['description'],router.get_interfaces()[i]['last_flapped'],router.get_interfaces()[i]['is_up'],router.get_interfaces()[i]['mac_address'],router.get_interfaces()[i]['speed']])
        print table
if __name__ == '__main__':
    main()
