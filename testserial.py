# python serial hex test
# winxos 2016-09-23
import time
import math
import serial

t = serial.Serial('com4', 115200)
cmd = ['63', '02', '61', '40', '33']
cmd_out = []
for i in cmd:
    cmd_out.append(i.decode('hex'))
i=0
while True:
    cmd_out[3] = int(math.sin(i)*90)+90
    i=i+0.01
    t.write(cmd_out)
    time.sleep(0.1)
t.close()
