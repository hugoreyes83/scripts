from ipaddress import IPv4Address,summarize_address_range
import argparse

def parse_args():
    #setting up argparser
    parser = argparse.ArgumentParser(description='subnetting tool')
    parser.add_argument('--start',required=True, help='enter ipv4 ip address')
    parser.add_argument('--end',required=True, help='enter ipv4 network')
    args = parser.parse_args()
    return args

def generate_subnets(start,end):
    return [ipaddr for ipaddr in summarize_address_range(IPv4Address(start),IPv4Address(end))]

def main():
    get_args = parse_args()
    for i in generate_subnets(get_args.start,get_args.end): print('{}'.format(i))


if __name__ == '__main__':
    main()
