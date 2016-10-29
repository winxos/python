#device manager
#winxos 2016-06-13
from fan import Fan
from device import Device
from IOManager import *
class DeviceManager:
	devices=[]
	def __init__(self):
		self.add_device(Fan(12))
	def add_device(self,d):
		d.set_id(len(self.devices))
		self.devices.append(d)
	def list_devices(self):
		ans=""
		for d in self.devices:
			ans+= str(d)+';'
		print ans
		return ans
	def run_device(self,args):
		print args
		if len(args)>2:
			return getattr(self.devices[int(args[0])],args[1])(args[2:])
		elif len(args)==2:
			return getattr(self.devices[int(args[0])],args[1])()
	def device_test(self):
		self.add_device(Fan(12))
		self.add_device(Fan(11))
		self.devices[0].test()
		self.list_devices()
if __name__=="__main__":
	dm=DeviceManager()
	dm.device_test()
