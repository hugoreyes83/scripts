from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectAuthError
from jnpr.junos.exception import ConnectRefusedError
from jnpr.junos.exception import ConnectTimeoutError
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import PermissionError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import CommitError
from jnpr.junos.exception import ConfigLoadError
import argparse
import getpass

parser = argparse.ArgumentParser(description='script for commiting config on juniper routers')
parser.add_argument('--device', '-d', help='device name')
parser.add_argument('--routers', '-r', help='file containing routers')
parser.add_argument('--username', '-u', help='enter username', required=True)
parser.add_argument('--config', '-c', help='enter config file', required=True)
args=parser.parse_args()

def get_password():
    getpasswd= getpass.getpass('Enter password: ')
    return getpasswd

def connect_to_router(host,user,password):
    dev = Device(host=host, user=user, password=password, gather_facts=False)
    return dev

def read_config_file(config_file):
    try:
        with open(config_file, 'r') as f:
            data = f.read()
            return data
    except IOError:
        print 'Error: file does not exist'
        return 0

def read_file_multiple_routers(filename):
    try:
        with open(filename, 'r') as f:
            routers_to_apply_config = f.readlines()
            routers = []
            for i in routers_to_apply_config:
                routers.append(i)
            return routers
    except IOError:
            print 'Error: File does not exist.'
            return 0

def commitconfig(commitcheck,device,username,password):
    commit_config = raw_input('Would you like to commit? ')
    if commitcheck == True and commit_config.lower() == 'y':
        connect_to_devices = connect_to_router(device,username,password) 
        cu = Config(connect_to_devices)
        cu.commit()
        print 'config has been successfully commited'
    else:
        connect_to_devices = connect_to_router(device,username,password) 
        cu = Config(connect_to_devices)
        cu.rollback()
        print 'config had to be rolledback'

def main():
    try:
        enable_password = get_password()
        config_file_data = read_config_file(args.config)
        if args.routers != None:
            multiple_routers_to_apply_config = read_file_multiple_routers(args.routers)
            print multiple_routers_to_apply_config
            for i in multiple_routers_to_apply_config:
                connect_to_devices = connect_to_router(i,args.username,enable_password) 
                cu = Config(connect_to_devices)
                cu.load(config_file_data, format='text')
                print 'pushing config to {}'.format(i)
                cu.pdiff()
                connect_to_devices.open()
                commit_check_config = cu.commit_check()
                commitconfig(commit_check_config,i,args.username,enable_password)
                
        else:
            connect_to_devices = connect_to_router(args.device,args.username,enable_password) 
            cu = Config(connect_to_devices)
            cu.load(config_file_data, format='text')
            cu.pdiff()
            connect_to_devices.open()
            commit_check_config = cu.commit_check()
            commitconfig(commit_check_config,args.device,args.username,enable_password)
    except ConnectAuthError as e:
        print e
    except ConnectRefusedError as e:
        print e
    except ConnectTimeoutError as e:
        print e
    except ConnectError as e:
        print e
    except LockError as e :
        print e
    except PermissionError as e:
        print e
    except UnlockError as e:
        print e
    except CommitError as e:
        print e
    except ConfigLoadError as e:
        print e

if __name__ == '__main__':
    main()
