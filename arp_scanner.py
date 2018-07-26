from scapy.all import srp,Ether,ARP,conf 
import sys
from datetime import datetime


try:
    interface = raw_input('[*] Please enter interface ')
    ips = raw_input('[*] Please enter IPs ')
        
    print '\n[*]Scanning'
    start_time = datetime.now()
    conf.verb = 0
    ans,unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ips), timeout = 20, iface = interface, inter = 0.1)
    print 'MAC  -  IP\n'
    for snd,rcv in ans:
        print rcv.sprintf(r'%Ether.src%  - %ARP.psrc%')
    stop_time = datetime.now()
    total_time = stop_time - start_time
    print '\n[*]Scan Complete'
    print '[*]Scan Duration: {}'.format(total_time)

except KeyboardInterrupt:
        print 'Quitting'
        sys.exit(1)
