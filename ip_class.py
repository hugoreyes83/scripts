from geolite2 import geolite2
from iptools import IpRange
from ipaddress import ip_address
import socket

class IP():
    def __init__(self,ipaddress,mask):
        self.ipaddress = ipaddress
        self.mask = mask

    def __str__(self):
        return "this is an IP object for {}".format(self.ipaddress)

    def geoip(self):
        '''This method returns a dictionary of geoip data for the provided ip'''
        get_ip_data = geolite2.reader()
        ip_data = get_ip_data.get(self.ipaddress)
        return ip_data

    def hosts(self):
        '''This method returns a list of hosts within the provided subnet'''
        return IpRange(self.ipaddress+'/'+self.mask)

    def reverse_record(self):
        return ip_address(self.ipaddress).reverse_pointer

    def reachability(self):
        pass
