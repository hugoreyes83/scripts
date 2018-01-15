from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectAuthError
from jnpr.junos.exception import ConnectRefusedError
from jnpr.junos.exception import ConnectTimeoutError
import argparse
import getpass

parser = argparse.ArgumentParser(description='script for commiting config on juniper routers')
parser.add_argument('--router', '-d', help='device name', required=True)
parser.add_argument('--username', '-u', help='enter username', required=True)
args=parser.parse_args()


def get_password():
    getpasswd= getpass.getpass('Enter password: ')
    return getpasswd


def connect_to_router(host,user,password):
    try:
        dev = Device(host=host, user=user, password=password, gather_facts=False)
        dev.open()
        return dev
    except ConnectAuthError as e:
        print e
    except ConnectRefusedError as e:
        print e
    except ConnectTimeoutError as e:
        print e
    except ConnectError as e:
        print e

def main():
    try:
        password = get_password()
        connect_to_router(args.router,args.username,password)
    except Exception as e:
        print e



if __name__ == '__main__':
    main()
