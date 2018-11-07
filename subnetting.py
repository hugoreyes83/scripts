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
mask = int(args.prefix.split('/')[1])

def validate_ip(ip):
    '''Validate IP before moving forward'''
    return True if netaddr.valid_ipv4(ip) else False

def validate_mask(mask):
    '''Validate Mask if valid before moving forward'''
    return True if mask > 0 and mask <= 32 else False

def figure_out_hosts(ip,mask):
    '''Figure out hosts per subnet'''
    subnet = 32 - mask
    if subnet == 0:
        '''This is a host address'''
        return 0
    else:
        return 2**subnet
def figure_out_subnet(ip,mask):
    '''Figure out subnets'''
        
def main():
    try:
        logging.info('Checking if both {} and {} are valid'.format(ip,mask))
        is_ip_valid = validate_ip(ip)
        is_mask_valid = validate_mask(mask)
        if not is_ip_valid:
            print '{} is not a valid IP'.format(ip)
            raise ValueError('oops! {} is not a valid IP'.format(ip))
        else:
            print '{} is a valid IP'.format(ip)
        if not is_mask_valid:
            print '{} is not a valid mask'.format(mask)
            raise ValueError('Opps! {} is not a valid mask'.format(mask))
        else:
            print '{} is a valid mask'.format(mask)
        hosts_per_subnet = figure_out_hosts(ip,mask)
        print 'There can be up to {} hosts in this subnet'.format(hosts_per_subnet)       




    except ValueError,e:
        print e.args[0]

if __name__ == '__main__':
    main()



