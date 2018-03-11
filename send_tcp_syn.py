import random
from scapy.all import *
conf.verb = 0
sequence = random.randint(100,5000)
ports = random.randint(1025,60000)
print 'sending packet with sequence {}'.format(sequence)
p = IP(dst='1.1.1.1')/TCP(sport=ports,dport=22,flags='S',seq=sequence) 
r = sr1(p)
print r.summary()
print r.show()
ack = r.seq + 1
sequence_plus_two = int(sequence) + 1

print 'sending packet with ack {}'.format(ack)
packet = IP(dst='1.1.1.1')/TCP(sport=ports,dport=22,flags='A',seq=sequence_plus_two,ack=ack)
send_packet = send(packet)

print 'sequence plus two = {}'.format(sequence_plus_two)
my_payload="space for rent!"
TCP_PUSH=IP(dst='1.1.1.1')/TCP(sport=ports, dport=22, flags="PA", seq=sequence_plus_two, ack=ack)
send(TCP_PUSH/my_payload)
