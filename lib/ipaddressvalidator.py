import netaddr

def ip_address(ip):
    if netaddr.valid_ipv4(ip):
        return True
    else:
        return False

