from netaddr import IPNetwork
import argparse
import logging

#setting up logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format = LOG_FORMAT)

#setting up argparser
parser = argparse.ArgumentParser(description='subnetting tool')
parser.add_argument('--prefix',required=True)
args = parser.parse_args()

def figure_out_hosts(ip):
    '''Figure out hosts in subnet'''
    ip_network = IPNetwork(ip)
    ip_list = list(ip_network)
    mask = ip_network.netmask
    prefixlen = ip_network.prefixlen
    broadcast = ip_network.broadcast
    cidr = ip_network.cidr
    return ip_list,mask,broadcast,prefixlen,cidr

def main():
    try:
        ip = args.prefix
        hosts,mask,broadcast,prefixlen,cidr = figure_out_hosts(ip)
        logging.info('IP prefix is {}'.format(str(cidr)))
        logging.info('Subnet is {}'.format(str(mask)))
        if str(mask) == '255.255.255.255':
            print('This is a host address hence there are no other IPs available in this subnet')
        else: 
            print('There could be up to {} hosts in this subnet'.format((2**(32-int(prefixlen)))))
            print('{} >> First Host'.format(str(hosts[0])))
            print('{} >> Last Usable Host'.format(str(hosts[-2])))
            print('{} >> Broadcast'.format(str(broadcast)))
    except Exception as e:
        print(e.message, e.args)

if __name__ == '__main__':
    main()



