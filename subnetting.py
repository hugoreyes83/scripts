import netaddr
import argparse
import logging

#setting up logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format = LOG_FORMAT)

#setting up argparser
parser = argparse.ArgumentParser(description='subnetting tool')
parser.add_argument('--prefix',required=True)
args = parser.parse_args()

ip = args.prefix.split('/')[0]

def validate_ip(ip):
    '''Validate IP before moving forward'''
    output = True if netaddr.valid_ipv4(ip) else False
    return output

def main():
    try:
        logging.info("Checking if {} is valid".format(ip))
        is_ip_valid = validate_ip(ip)
        if not is_ip_valid:
            print "{} is not a valid IP".format(ip)
            raise ValueError('oops!')
        else:
            print "{} is a valid IP".format(ip)

    except ValueError,e:
        print e.args[0]

if __name__ == '__main__':
    main()



