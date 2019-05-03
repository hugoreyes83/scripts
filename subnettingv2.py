from netaddr import IPNetwork
from iptools import IpRange
from iptools.ipv4 import validate_cidr
from prettytable import PrettyTable
import argparse
import logging

#setting up logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format = LOG_FORMAT)

#setting up argparser
parser = argparse.ArgumentParser(description='subnetting tool')
parser.add_argument('--prefix',required=True, help="enter ipv4 prefix in cidr notation")
parser.add_argument('--display',required=False)
parser.add_argument('--file', required=False)
args = parser.parse_args()

def validate_prefix(ip):
    return validate_cidr(ip)


def main():
    check_prefix = validate_cidr(args.prefix)
    assert(check_prefix), "Prefix is NOT a valid ipv4 prefix, Exitting..."

if __name__ == '__main__':
    main()
