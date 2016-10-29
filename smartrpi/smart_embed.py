#raspberry pi states remote query service
#winxos 2016-6-10
import socket
import time
from DeviceManager import DeviceManager
version="1.0"
port=9000
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
s.bind(('',port))
if __name__=='__main__':
    print("query service starting...")
    dm=DeviceManager()
    while True:
        data,addr=s.recvfrom(1024)
        print("%s:%s"%(addr,data))
        datas=data.split()
        if len(datas)==0:continue
        if datas[0]=="RPI":
            if len(datas)==1:
                s.sendto("IPR",addr)
            else:
                t=datas[1]
                if t=="NAME":
                    s.sendto(socket.gethostname(),addr)
                elif t=="VERSION":
                    s.sendto(version,addr)
                elif t=="DEVICES":
                    s.sendto(dm.list_devices(),addr)
                elif t=="DEVICE":
                    if len(datas)>2:
                        msg=dm.run_device(datas[2:])
                        if isinstance(msg,str):
                            s.sendto("IPR DEVICE %s %s"%(datas[2],msg),addr)
                    
                
