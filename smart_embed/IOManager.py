#gpio manager
#winxos 2016-06-13
import RPi.GPIO as g
import time
pwm={}
cpwm={}
class IOManager:
	def __init__(self):
		g.setmode(g.BOARD)
	def gpio_setmode(self,p,m):
		if m=="OUTPUT":
			g.setup(p,g.OUT)
		elif m=="INPUT":
			g.setup(p,g.INPUT)
	def gpio_pwm_init(self,p,c):
		pwm[p]=g.PWM(p,c)
		pwm[p].start(0)
		cpwm[p]=0
	def gpio_pwm_set(self,p,c):
		pwm[p].ChangeDutyCycle(c)
		cpwm[p]=c
	def gpio_pwm_get(self,p):
		return cpwm[p]
	def gpio_write(self,n,v): #v 0 -> low
		g.output(n,v)
	def gpio_read(self,n):
		return g.input(n)
	def gpio_test(self):
		'''
		gpio_setmode(12,"OUTPUT")
		gpio_pwm_init(12,1000)
		gpio_pwm_set(12,2)
		time.sleep(10)
		gpio_pwm_set(12,100)
		time.sleep(10)
		gpio_write(12,1)
		print gpio_read(12)
		gpio_write(12,0)
		print gpio_read(12)
		'''
		pass

if __name__=="__main__":
	im=IOManager()
