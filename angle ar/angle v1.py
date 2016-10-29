# coding:utf-8
'''
angle game augmented reality v0.1 with python
winxos 2016-03-12
'''
import cv2
import numpy as np
import time
from datetime import datetime
import math
WIN_NAME="ANGLE AR v1"

class board:
    mask = None
    board_field = None
    showflag = True
    solved = False
    img_ans = None
    sum = 0 #for fps
    pt = 0 #for fps
    img=None
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 800)
        self.cam.set(4, 600)
        w = self.cam.get(3)
        h = self.cam.get(4)
        print w, h

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print (x, y)
            if x < 100 and y < 100:  #
                if self.img != None:  #
                    cv2.imwrite(datetime.now().strftime("%m%d%H%M%S") + ".png", self.img_ans)  #
                    print "save png file to:\n", datetime.now().strftime("%m%d%H%M%S") + ".png"
    def exact_img(self, win, img, cnt):#warp exact
        pass
    def add_warp_img(self,src,sub,cnt):
        r,c,_ = src.shape
        pts = cnt.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        M = cv2.getPerspectiveTransform(np.array([[0,0],[599,0],[599,599],[0,599]],np.float32), rect)
        return cv2.warpPerspective(sub, M,(c,r))
    def get_state(self,img):
        t, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
        w = img.shape[1]
        h = img.shape[0]

        return ans

    def find_roi(self, img):#find main board
        img = cv2.GaussianBlur(img, (3, 3), 0)  #
        #t, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
        img = cv2.Canny(img, 10, 100)
        kernel = np.ones((3,3), np.uint8)
        #img = cv2.erode(img, kernel)
        #img = cv2.dilate(img, kernel)
        #img = cv2.erode(img, kernel)
        lines = cv2.HoughLinesP(img, 1, math.pi / 180,100,None,30,10)
        circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,200)
        if circles is not None:
	        # convert the (x, y) coordinates and radius of the circles to integers
	        circles = np.round(circles[0, :]).astype("int")
	        # loop over the (x, y) coordinates and radius of the circles
	        for (x, y, r) in circles:
		        # draw the circle in the output image, then draw a rectangle
		        # corresponding to the center of the circle
		        cv2.circle(self.img, (x, y), r, (0, 255, 0), 4)
		        cv2.rectangle(self.img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
        if len(lines)>0:
            for x1,y1,x2,y2 in lines[0]:  
                cv2.line(self.img,(x1,y1),(x2,y2),(0,255,0),2)  
        #cnts, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[1:]
        cv2.imshow("img",img)
        #cv2.drawContours(self.img, cnts,-1, (0,0,255),1)
    def get_fps(self, t):
        self.sum += t
        self.pt += 1
        if self.pt > 100:
            self.pt = 1
            self.sum = t
        return int(self.pt / self.sum)

    def run(self):  #
        while True:
            st = time.clock()
            ret, self.img = self.cam.read()  #
            try:
                self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
                self.find_roi(self.gray)
                cv2.putText(self.img, "fps:" + str(self.get_fps((time.clock() - st))),
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 250, 0), 1)
                key = cv2.waitKey(20)
                if(key == 27):
                    break  #
                if self.img_ans != None:
                    #ret, mask = cv2.threshold(cv2.cvtColor(self.img_ans,cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY)
                    #mask_inv = cv2.bitwise_not(mask) #
                    #img1_bg = cv2.bitwise_and(self.img,self.img,mask = mask_inv)#
                    #img2_fg = cv2.bitwise_and(self.img_ans,self.img_ans,mask = mask) #
                    #self.img = cv2.add(img1_bg,img2_fg)
                    self.img = cv2.add(self.img,self.img_ans)
                    self.solved = True
                cv2.imshow(WIN_NAME, self.img)
                cv2.setMouseCallback(WIN_NAME, self.on_mouse)  #
            except Exception,e:
                print(e)
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    b = board()
    b.run()
