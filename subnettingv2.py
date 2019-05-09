from netaddr import IPNetwork
from iptools import IpRange
from iptools.ipv4 import validate_cidr
from prettytable import PrettyTable
import argparse
import logging

#setting up logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format = LOG_FORMAT)

def parse_args():
    #setting up argparser
    parser = argparse.ArgumentParser(description='subnetting tool')
    parser.add_argument('--prefix',required=True, help="enter ipv4 prefix in cidr notation")
    parser.add_argument('--display',required=False)
    parser.add_argument('--file', required=False)
    args = parser.parse_args()
    return args

def validate_prefix(ip):
    # validate both prefix and prefix length
    return validate_cidr(ip)

def user_input():
    # get user input
    user_input = input('Enter prefix length ')
    try:
        int(user_input)
        if int(user_input) <= 32 and int(user_input) >= 1:
            logging.info('{} is a valid prefix length'.format(user_input))
            return user_input
        else:
            logging.info('{} is not a valid prefix length'.format(user_input))
    except:
        logging.info('{} is not a valid prefix length'.format(user_input))

def netmask(n):
    return '{}{}'.format('0'*n,'1'*(32-n))

def main():
    get_args = parse_args()
    check_prefix = validate_cidr(get_args.prefix)
    assert(check_prefix), 'Prefix is NOT a valid ipv4 prefix, Exiting...'
    validate_prefix_length = user_input()
    logging.info('Generating number of /{} that could fit in {}'.format(validate_prefix_length,get_args.prefix))
    number_of_subnets = len(IpRange(get_args.prefix))//int(netmask(int(validate_prefix_length)),2)
    logging.info('There are up to {} in {}'.format(number_of_subnets,get_args.prefix))



if __name__ == '__main__':
    main()
