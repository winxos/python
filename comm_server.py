#-------------------------------------------------------------------------------
# Name:        broadcast connect client module
# Purpose:
#
# Author:      lw
#
# Created:     10/09/2014
# Copyright:   (c) lw 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import socket,threading,time
import ctypes
login=False
port=10400
addr=None

class recv_broadcast(threading.Thread):
    motion=None
    def __init__(self,s):
        self.s=s
        threading.Thread.__init__(self)

        self.motion=ctypes.WinDLL('e:/XhuMobot.dll')
        self.motion.create()
        print ( "loading finished")
    def run(self):
        global login,addr
        print ("listening")
        while True:
            data,addrs=self.s.recvfrom(1<<8)
            print(data,addrs)
            self.run_cmd(data)
    def run_cmd(self,data):
        if data[0]=='c' and data[6]=='e':
            if data[1]=='w':
                l=((ord(data[2])<<8) + ord(data[3])) &0xFFFF
                if(l>2**15):l=l-2**16
                r=((ord(data[4])<<8) + ord(data[5])) &0xFFFF
                if(r>2**15):r=r-2**16
                self.motion.set_speed(l,r)

def main():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,True)
    s.bind(('0.0.0.0',port))
    try:
        recv_broadcast(s).start()
    except Exception, e:
        print "err",e



if __name__ == '__main__':
     main()
