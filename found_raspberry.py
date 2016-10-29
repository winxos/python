# broadcast discovery raspberry pi
# version 1.0
# winxos 2016-06-10
import socket
import sys
desc = ('<broadcast>', 9000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('',11000))
s.sendto("RPI NAME", desc)
while True:
    data,addr=s.recvfrom(1024)
    print("%s:%s"%(addr,data))
