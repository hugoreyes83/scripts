from jnpr.junos import Device
from jnpr.junos.op.lldp import LLDPNeighborTable
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectAuthError
from jnpr.junos.exception import ConnectRefusedError
from jnpr.junos.exception import ConnectTimeoutError
import argparse
import getpass
import json

parser = argparse.ArgumentParser(description='lldp script')
parser.add_argument('--router', '-d', help='device name', required=True)
parser.add_argument('--username', '-u', help='enter username', required=True)
args=parser.parse_args()


def get_password():
    getpasswd= getpass.getpass('Enter password: ')
    return getpasswd


def connect_to_router(host,user,password):
    dev = Device(host=host, user=user, password=password, gather_facts=False)
    dev.open()
    return dev

def main():
    try:
        password = get_password()
        router = connect_to_router(args.router,args.username,password)
        router.open()
        neighbors = LLDPNeighborTable(router)
        neighbors.get()
        output_json = json.loads(neighbors.to_json())
        for i in output_json:
            print 'local interface is ' + str(i) + ' and remote interface is ' + output_json[i]['remote_port_id']
    except ConnectAuthError as e:
        print e
    except ConnectRefusedError as e:
        print e
    except ConnectTimeoutError as e:
        print e
    except ConnectError as e:
        print e



if __name__ == '__main__':
    main()
