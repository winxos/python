#coding:utf8
'''
raspberry pi camera using picamera and cv2
for the catching tank.
winxos 2015-11-22 @aistlab
added dist, angle modify 2015-11-23
'''
import io
import time
import picamera
import cv2
import numpy as np
from Queue import Queue
from threading import Thread
import math
npic=1
images=Queue(npic)

W=160
H=160
hsv=None
mask=None
ball_min=np.array((28,70,90))
ball_max=np.array((52,220,240))
class Viewer(Thread):
    _selection=None
    _drag_start=None
    def on_mouse(self,event,x,y,flags,param):
        global ball_min,ball_max
        try:
            if event==cv2.EVENT_LBUTTONDOWN:
                self._drag_start=(x,y)
            if event==cv2.EVENT_LBUTTONUP:
                self._drag_start=None
                x,y,w,h=self._selection
                cm=hsv[y:y+h,x:x+w]
                ball_min=np.array((np.min(cm[:,:,0])*0.9,np.min(cm[:,:,1])*0.75,np.min(cm[:,:,2])*0.8))
                ball_max=np.array((np.max(cm[:,:,0])*1.1,np.max(cm[:,:,1])*1.45,np.max(cm[:,:,2])*1.2))
                print ball_min,ball_max
                
            if self._drag_start:
                xmin=min(x,self._drag_start[0])
                ymin=min(y,self._drag_start[1])
                xmax=max(x,self._drag_start[0])
                ymax=max(y,self._drag_start[1])
                self._selection=(xmin,ymin,xmax-xmin,ymax-ymin)
        except Exception,e:
            print e
            
    def run(self):
        global images,hsv,mask

        cv2.setMouseCallback("hsv",self.on_mouse)
        while True:
            try:
                if hsv!=None:
                    cv2.imshow("hsv",hsv)
                if mask!=None:
                    cv2.imshow("mask",mask)
                if images.qsize()>0:
                    tmp=images.get()
                    cv2.imshow("cam",tmp)
                    #print images.qsize()
            except Exception,e:
                print e
            time.sleep(0.025);
            ch=0xFF & cv2.waitKey(5)
            if ch==27:
                break
        exit(0)
                    
    def __init__(self):
        Thread.__init__(self)
        cv2.namedWindow("hsv")
        cv2.namedWindow("cam")
        cv2.namedWindow("mask")
        
class Catcher(Thread):
    def __init__(self):
        Thread.__init__(self)
    def outputs(self):
        global hsv,mask
        stream=io.BytesIO()
        for i in range(npic):
            yield stream
            start_time=time.time()
            stream.seek(0)
            try:
                tmp=np.fromstring(stream.getvalue(),dtype=np.uint8)
                tmp=tmp.reshape((W,H,3))
                hsv=cv2.cvtColor(tmp,cv2.COLOR_BGR2HSV)
                mask=cv2.inRange(hsv,ball_min,ball_max)
                cmask=mask.copy()
                contours,hierarchy=cv2.findContours(cmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                maxarea=0
                cnt=None
                for h,tcnt in enumerate(contours):
                    area=cv2.contourArea(tcnt)
                    if area>maxarea:
                        maxarea=area
                        cnt=tcnt
                (x,y),r=(0,0),0
                if cnt != None:
                    (x,y),r=cv2.minEnclosingCircle(cnt)
                    cv2.circle(tmp,((int)(x),(int)(y)),(int)(r),(0,0,255),1)
                    cv2.putText(tmp,"%.1f %.1f %.1f"%(x,y,r),(1,20),cv2.FONT_HERSHEY_PLAIN,1.0,(255,0,255))
                finish=time.time()
                cv2.putText(tmp,"dist:%.1f, ang:%.1f"%self.calc_loc(x,y),(0,40),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,255))
                cv2.putText(tmp,"fps:%.1f"%(1/(finish-start_time)),(0,60),cv2.FONT_HERSHEY_PLAIN,1.0,(255,255,0))
                images.put(tmp)
            except Exception,e:
                print e
            stream.truncate()
    def calc_loc(self,x,y):
        camera_height=110.0
        camera_mid_ground=820.0
        camera_near_ground=50.0
        camera_mid_angle=math.atan(camera_height/camera_mid_ground)
        camera_near_angle=math.atan(camera_height/camera_near_ground)
        camera_half_viewangle=camera_near_angle-camera_mid_angle
        half_image_height=H/2
        part_angle=(y-half_image_height)/half_image_height*camera_half_viewangle
        real_angle=part_angle+camera_mid_angle
        dist=camera_height/math.tan(real_angle)
        if dist<0:
            dist=0
            
        half_image_weight=W/2
        real_xangle=(x-half_image_weight)/half_image_weight*camera_half_viewangle*57.3
        return (dist/10.0,real_xangle)

        
    def run(self):
        with picamera.PiCamera() as cam:
            cam.resolution=(H,W)
            cam.framerate=40
            while True:
                #time.sleep(5)
                try:
                    cam.capture_sequence(self.outputs(),'bgr',use_video_port=True)
                except Exception,e:
                    print e

if __name__=="__main__":
    print( "running...")
    v=Viewer()
    c=Catcher()
    c.start()
    v.start()
    while True:
        time.sleep(1)
    



    
