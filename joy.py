import pygame as p

p.init()
stick = p.joystick.Joystick(0)
stick.init()
print("initialized:",bool(stick.get_init()))
print(stick.get_name())

while stick.get_axis(0)*100 < 99:
   print(round(stick.get_axis(0)*100))
   #need for right detection otherwise stick.get_axis always returns 0
   for event in p.event.get(): 
      None
p.quit()
