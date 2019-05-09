from ipaddress import ip_network
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

def user_input(p):
    # get user input
    user_input = input('Enter prefix length: ')
    try:
        int(user_input)
        if int(user_input) <= 32 and int(user_input) >= 1 and int(user_input) > int(p):
            logging.info('{} is a valid prefix length'.format(user_input))
            return user_input
        else:
            logging.info('{} is not a valid prefix length'.format(user_input))
            return False
    except ValueError as e:
        logging.info(e)

def generate_subnets(s,p):
    return list(ip_network(s).subnets(new_prefix=p))

def generate_table(d):
    table = PrettyTable()
    table.field_names = ["Prefixes"]
    for i in d:
        table.add_row([i])
    return table


def main():
    #grab arguments
    get_args = parse_args()
    check_prefix = validate_cidr(get_args.prefix)
    #check if prefix is valid, if it is not then do not proceed
    assert(check_prefix), 'Prefix is NOT a valid ipv4 prefix, Exiting...'
    #ask user for prefix length
    prefix_length = user_input(get_args.prefix.split('/')[1])
    logging.info('Generating number of /{} that could fit in {}'.format(prefix_length,get_args.prefix))
    # do not proceed further if user provided prefix is larger than prefix
    assert(prefix_length), 'Provided prefix length cannot be larger than {}'.format(get_args.prefix.split('/')[1])
    #generate subnets
    generatesubnets = generate_subnets(get_args.prefix,int(prefix_length))
    #generate table
    generatetable = generate_table(generatesubnets)
    print(generatetable)


if __name__ == '__main__':
    main()
