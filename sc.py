#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scapy.all import srp,Ether,ARP,conf
ipscan='192.168.1.1/24'
try:
    ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ipscan),timeout=2,verbose=False)
except Exception,e:
    print str(e)
else:
    for snd,rcv in ans:
        list_mac=rcv.sprintf("%Ether.src% - %ARP.psrc%")
        print list_mac