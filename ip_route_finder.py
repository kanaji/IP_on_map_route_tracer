from scapy.all import *
from scapy.layers.inet import IP, TCP

from ipwhois import IPWhois
from pprint import pprint

#obj = IPWhois('8.8.8.8')
#results = obj.lookup_rdap(depth=1)
#pprint(results)

target = ["8.8.8.8"]

result, unans = sr(IP(dst=target, ttl=(1, 10)) / TCP(dport=53, flags="S"))

for snd, rcv in result:
  print(rcv.src)
  x = str(rcv.src).split('.')
  if x[0] != '192':
    obj = IPWhois(str(rcv.src))
    results = obj.lookup_rdap(depth=1)
    pprint(results)