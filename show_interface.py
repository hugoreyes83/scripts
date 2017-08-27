from pprint import pprint
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.exception import ConnectError
import argparse

parser = argparse.ArgumentParser(description='Simple show interfaces script')
parser.add_argument('--device', '-d', help='Specify device name')
parser.add_argument('--user', '-u', help="Specify username")
parser.add_argument('--password', '-p', help="Specify password")
parser.add_argument('--interface', '-i', help="interface")
args = parser.parse_args()

try:
    dev = Device(host=args.device, user=args.user, password=args.password, normalize=True)
    dev.open()
    rsp = dev.rpc.get_interface_information(interface_name=args.interface, extensive=True)
#print(etree.tostring(rsp, encoding='unicode'))
    print 'Operational Status: ',
    print (rsp.xpath(".//oper-status")[0].text)
    print 'IP Address: ',
    print (rsp.xpath(".//address-family[address-family-name='inet']/ interface-address/ifa-local")[0].text)
    print 'Description: ',
    print (rsp.xpath(".//description")[0].text)
    print 'Input Errors: ',
    print (rsp.xpath(".//input-error-list/input-errors")[0].text)
    print 'Input Bytes: ',
    print (rsp.xpath(".//input-bps")[0].text)
    print 'Output Bytes: ',
    print (rsp.xpath(".//output-bps")[0].text)
    print 'Last Flapped: ',
    print (rsp.xpath(".//interface-flapped")[0].text)
except ConnectError as e:
    print e
except:
    print "This is a generic error message"
finally:
    dev.close()
