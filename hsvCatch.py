# -*- coding: utf-8 -*-
#全新的cv2版本框架
#wsNaoVisionMT.py 采用多线程框架进行数据处理
#winxos 2012-07-12

import numpy as np
import cv2
import math,time
from threading import Thread

TennisSize=65 #网球实际尺寸
GolfSize=43 #高尔夫球实际尺寸

class wsNaoVision(Thread):
  _robotip=""
  _baseSize=TennisSize
  _ball_min = np.array((37,93,126))
  _ball_max = np.array((42,216,248))
  _gate_min=np.array((106,31,195))
  _gate_max=np.array((119,59,232))
  _selection=None
  _ldrag_start = None
  _rdrag_start = None
  _raw=None
  _hsv=None
  _threshBall=None
  _threshGate=None
  hou=None
  _showWindows=False
  _startMonitor=False
  _ballImageInfo=(0,0,0) #图片上最小包裹圆信息
  _ballSpaceDistance=0 #空间球距离
  _gateBounding=(0,0,0,0)
  _nearstObstacleBounding=(0,0,0,0)
  _line=[(0,0),(0,0)]
  def setWindowsOn(self):
    self._showWindows=True

  def startMonitor(self):
    self._startMonitor=True
    self.start()
  def stopMonitor(self):
    self._startMonitor=False
  def run(self):
    if self._showWindows:
      cv2.namedWindow("raw")
      cv2.namedWindow("hsv")
      cv2.setMouseCallback("hsv",self.on_mouse)
    else:
      cv2.destroyAllWindows()
    while self._startMonitor:
      self.getRawImage()
      key = cv2.waitKey(20)
      if(key == 27):
          break  #
      cv2.imshow("raw",self._raw)
      cv2.imshow("hsv",self._hsv)
      
  def on_mouse(self,event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      self._ldrag_start = (x, y)
    if event == cv2.EVENT_RBUTTONDOWN:
      self._rdrag_start = (x, y)
    if event == cv2.EVENT_LBUTTONUP:
      self._ldrag_start = None
      self._ball_min,self._ball_max=self.getThresh(self._hsv,self._selection)
      print "ball:",self._ball_min,self._ball_max
    if event == cv2.EVENT_RBUTTONUP:
      self._rdrag_start = None
      self._gate_min,self._gate_max=self.getThresh(self._hsv,self._selection)
      print "gate:",self._gate_min,self._gate_max
    if self._ldrag_start:
      xmin = min(x, self._ldrag_start[0])
      ymin = min(y, self._ldrag_start[1])
      xmax = max(x, self._ldrag_start[0])
      ymax = max(y, self._ldrag_start[1])
      self._selection = (xmin, ymin, xmax - xmin, ymax - ymin)
    if self._rdrag_start:
      xmin = min(x, self._rdrag_start[0])
      ymin = min(y, self._rdrag_start[1])
      xmax = max(x, self._rdrag_start[0])
      ymax = max(y, self._rdrag_start[1])
      self._selection = (xmin, ymin, xmax - xmin, ymax - ymin)
  def __init__(self):
    Thread.__init__(self)
    self.cam = cv2.VideoCapture(0)

  def getThresh(self,img,selection): 
    x,y,w,h = selection
    cm=img[y:y+h,x:x+w] #cv2中利用切片和np内置函数来做，快很多
    hsvmin=np.array((np.min(cm[:,:,0]),np.min(cm[:,:,1]),np.min(cm[:,:,2])))
    hsvmax=np.array((np.max(cm[:,:,0]),np.max(cm[:,:,1]),np.max(cm[:,:,2])))
    return hsvmin,hsvmax
  def getLines(self,thresh):
    thresh=cv2.Canny(thresh,50,200)
    thresh=cv2.dilate(thresh,None)
    tmp = cv2.HoughLinesP(thresh, 1, math.pi / 180,100,None,30,10)
    self._line=[(0,0),(0,0)]
    if tmp!=None:
      lines=tmp[0]
      maxdis=0
      cx=0
      for line in lines:
        cx+=line[2]
      cx=cx/len(lines)
      for line in lines:
        if line[2]<cx:continue
        dis=(line[0]-line[2])**2+(line[1]-line[3])**2
        if dis > maxdis:
          maxdis=dis
          x0=line[0]
          y0=line[1]
          x1=line[2]
          y1=line[3]
          self._line=[(x0,y0),(x1,y1)]
  def getROI(self,tmin,tmax): #普通组合滤波,hsv 格式
    thresh=cv2.inRange(self._hsv, tmin,tmax) #过滤
    thresh=cv2.medianBlur(thresh,3) #中值滤波
    thresh=cv2.GaussianBlur(thresh,(3,3),0) #高斯滤波
    return thresh
  def getRawImage(self): #得到原始图片
    ret, self._raw = self.cam.read()
    self._hsv=cv2.cvtColor(self._raw,cv2.COLOR_BGR2HSV)
    
if __name__ == '__main__':
  print "nao vision multi thread class \nwinxos at 2012-07-12"
  m=wsNaoVision()
  m.setWindowsOn()
  m.startMonitor()
  while True:
    #print m.getGroundBallDistance(mo.getHeadPitchAngle())
    time.sleep(0.2)
  
    
  
  



