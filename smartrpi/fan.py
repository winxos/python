#fan driver
#winxos 2016-06-13
from device import *
from IOManager import *
class Fan(Device):
	im=IOManager()
	def __init__(self,p):
		self.name="FAN"
		self.device_id=0
		self.sdk_version=1
		self.author="winxos"
		self.device_type="IO"
		self.io_binded=[p]	
		self.im.gpio_setmode(p,"OUTPUT")
		self.im.gpio_pwm_init(p,1000)
	def set_id(self,n):
		self.device_id=n
	def set_speed(self,s):
		try:
			self.im.gpio_pwm_set(self.io_binded[0],int(s[0]))
		except Exception,e:
			print e
	def stop(self):
		self.im.gpio_write(self.io_binded[0],0)
	def get_speed(self):
		return str(self.im.gpio_pwm_get(self.io_binded[0]))
	def test(self):
		import time
		self.set_speed(5)
		time.sleep(5)
		self.set_speed(90)
		time.sleep(5)
	def __str__(self):
		return "%s@%s"%(self.name,self.device_id)
