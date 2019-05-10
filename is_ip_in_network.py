from ipaddress import IPv4Address,IPv4Network
from iptools.ipv4 import validate_ip,validate_cidr
import argparse
import logging

#setting up logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format = LOG_FORMAT)

def parse_args():
    #setting up argparser
    parser = argparse.ArgumentParser(description='subnetting tool')
    parser.add_argument('--ip',required=True, help='enter ipv4 ip address')
    parser.add_argument('--network',required=True, help='enter ipv4 network')
    args = parser.parse_args()
    return args

def is_ip_in_network(ip,net):
    return IPv4Address(ip) in IPv4Network(net)

def validate_ipaddress(ip):
    return validate_ip(ip)

def validate_network(network):
    return validate_cidr(network)

def main():
    get_args = parse_args()
    validateip = validate_ipaddress(get_args.ip)
    validatenetwork = validate_network(get_args.network)
    assert(validateip), '{} is not valid'.format(get_args.ip)
    assert(validatenetwork), '{} is not valid'.format(get_args.network)
    ip_in_network = is_ip_in_network(get_args.ip,get_args.network)
    if ip_in_network:
        logging.info('{} is part of {}'.format(get_args.ip,get_args.network))
    else:
        logging.info('{} is NOT part of {}'.format(get_args.ip,get_args.network))


if __name__ == '__main__':
    main()
