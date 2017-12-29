from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import argparse
import getpass

parser = argparse.ArgumentParser(description='script for commiting config on juniper routers')
parser.add_argument('--device', '-d', help='device name')
parser.add_argument('--username', '-u', help='enter username')
parser.add_argument('--config', '-c', help='enter config file')
args=parser.parse_args()

getpasswd= getpass.getpass('Enter password: ')
dev = Device(host=args.device, user=args.username, password=getpasswd, gather_facts=False)
dev.open()

cu = Config(dev)

with open(args.config, 'r') as f:
    data = f.read()

cu.load(data, format='text')
cu.pdiff()
commit_config = raw_input('Would you like to commit? ')

if cu.commit_check() and commit_config.lower() == 'y':
    cu.commit()
else:
    cu.rollback()
