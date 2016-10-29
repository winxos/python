#raspberry pi states remote query service
#winxos 2016-6-10
import socket
import time
version="1.0"
port=9000
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
s.bind(('',port))
if __name__=='__main__':
    print("query service starting...")
    while True:
        data,addr=s.recvfrom(1024)
        print("%s:%s"%(addr,data))
        datas=data.split()
        if len(datas)==0:continue
        if datas[0]=="RPI":
            if len(datas)==1:
                s.sendto("IPR",addr)
            else:
                if datas[1]=="NAME":
                    s.sendto(socket.gethostname(),addr)
                elif datas[1]=="VERSION":
                    s.sendto(version,addr)
