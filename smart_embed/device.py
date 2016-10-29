#device class info
#winxos 2016-06-13
class Device:
	def __init__(self):
		self.name=""
		self.device_id=0
		self.sdk_version=0
		self.author=""
		self.device_type=""
		self.io_binded=[]
	def get_name(self):
		return self.name	
