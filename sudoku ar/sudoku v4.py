# coding:utf-8
'''
sudoku augmented reality v0.4 with python
solver from web
no sample needed
winxos 2016-03-31
'''
import cv2
import numpy as np
import time
from datetime import datetime
import math
import logging
import random
from sudokuSlove import Sudoku
TITLE="SUDOKU AR v0.4"
DATAPATH="v4data"
digits=[]
def find2(img):
    #t, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
    ans=0
    m=[0]
    for i in xrange(len(digits)):
        res=cv2.matchTemplate(digits[i],img,cv2.TM_CCOEFF_NORMED)
        if res > m:
            m = res
            ans = i
    #print m,ans
    if m[0] < 0.8:
        digits.append(img)
        print "img size %d"%len(digits)
        ans=len(digits)-1
    return "%d"%ans
def find(img):
    ans=0
    m=900
    for i in xrange(len(digits)):
        res=cv2.absdiff(digits[i],img)
        if m>cv2.countNonZero(res):
            m = cv2.countNonZero(res)
            ans = i
    print ans,m
    if m>150:
        if len(digits)<10:
            digits.append(img)
            print ans,m
            print "img size %d"%len(digits)
            ans=len(digits)-1
        else:
            ans=-1
            print "miss"
    return "%d"%(ans+1)
def load_args(data):
    a = [None] * 9
    for i, d in enumerate(data.split()):
        a[i] = [int(c) for c in d]
    return a
class board:
    mask = None
    board_field = None
    showflag = True
    solved=False
    img_ans=None
    sum=0 #for fps
    pt=0 #for fps
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 1280)
        self.cam.set(4, 720)
        w = self.cam.get(3)
        h = self.cam.get(4)
        print w, h

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print (x, y)
            if x < 100 and y < 100:  #
                im = None
                if self.showflag:
                    im = self.img
                else:
                    im = self.hsv
                if im != None:  #
                    cv2.imwrite(datetime.now().strftime(
                        "%m%d%H%M%S") + ".png", im)  #
                    print "save png file to:\n", datetime.now().strftime("%m%d%H%M%S") + ".png"

    def exact_img(self, win, img, cnt):#warp exact
        if len(cnt) < 4:
            return
        pts = cnt.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))
        ratio = max(maxHeight, maxWidth) / 600.0
        #w, h = int(maxWidth / ratio), int(maxHeight / ratio)
        w, h = int(maxWidth / ratio), int(maxWidth / ratio)
        dst = np.array([
            [0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        raw=cv2.warpPerspective(img, M, (w, h))
        ma=2
        return cv2.resize(raw[ma:w-ma,ma:h-ma],(w,h))
    def add_warp_img(self,src,sub,cnt):
        r,c,_=src.shape
        pts = cnt.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        M = cv2.getPerspectiveTransform(np.array([[0,0],[599,0],[599,599],[0,599]],np.float32), rect)
        raw=cv2.warpPerspective(sub, M,(c,r))
        return raw
    def get_state(self,img):
        img = cv2.GaussianBlur(img, (3, 3), 1) 
        t, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
        cv2.imshow("otsu",img)
        w = img.shape[1]
        h = img.shape[0]
        grids=9
        gaph=h//grids
        gapw=w//grids
        margin=8
        ans=""
        for i in xrange(9):
            for j in xrange(9):
                s=img[i*gapw+margin+5:i*gapw+gapw-margin+5,j*gapw+margin+3:j*gapw+gapw-margin+3]
                mask = cv2.bitwise_not(s)
                kernel = np.ones((5,5), np.uint8)
                mask = cv2.dilate(mask, kernel)
                mask = cv2.erode(mask, kernel)
                cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnt = sorted(cnts, key=cv2.contourArea, reverse=True)
                if len(cnt)>0 and cv2.contourArea(cnt[0])>50:
                    x, y, w, h = cv2.boundingRect(cnt[0])
                    sub = cv2.resize(s[y:y + h,x:x + w],(30,30))
                    t,sub=cv2.threshold(sub,0,255,cv2.THRESH_OTSU)
                    cv2.imshow("%d"%(i*9+j),sub)
                    cv2.moveWindow("%d"%(i*9+j),j*200,i*100)
                    ans+=find(sub)
                else:
                    ans+="0"
            ans+=" "
        print ans
        #cv2.imshow("after", img)
        return ans
    def add_numbers(self,img,n,ans):#draw number
        w = img.shape[1]
        h = img.shape[0]
        grids=9
        gap=h//grids
        margin=10
        for i in xrange(9):
            for j in xrange(9):
                if ans[i*10+j]=="0":
                    print "e:%d,%d"%(((int)(n[i*9+j])-1),len(digits))
                    t=cv2.cvtColor(digits[(int)(n[i*9+j])-1], cv2.COLOR_GRAY2RGB)
                    t=cv2.bitwise_not(t)
                    t[:,:,0]=np.where(t[:,:,0]>0,random.randint(100,255),0)
                    img[i*gap+margin+10:i*gap+margin+30+10, j*gap+margin+10:j*gap+margin+30+10]=t
                    #cv2.putText(img, n[j*9+i],(i*gap+margin+gap/5, j*gap+margin+gap/2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255, 255), 3)     

    def is_valid_roi(self,img):
        return True                      
    def find_contours(self, img):#find main board
        img = cv2.GaussianBlur(img, (3, 3), 1)  #
        t, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
        kernel = np.ones((1,1), np.uint8)
        img = cv2.erode(img, kernel)
        cnts, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            if cv2.contourArea(cnt) < 50000:continue
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.01 * cnt_len, True)  #
            if len(cnt)==4 and cv2.isContourConvex(cnt):   # 4 cv2.contourArea(cnt)
                x0, y0, w0, h0 = cv2.boundingRect(cnt)
                if x0>10 and y0>10:
                    tm=self.exact_img("sudoku",self.gray,cnt)
                    if self.is_valid_roi(tm):
                        global digits
                        digits=[]
                        cv2.imshow("exact",tm)
                        return tm,cnt
        return None,None
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
                tm,cnt=self.find_contours(self.gray)
                if tm!=None:
                    if not self.solved:
                        ans=self.get_state(tm)
                        
                        s=Sudoku(load_args(ans))
                        if not s.solve():
                            print "can't solved"
                        else:
                            s=s.dump()
                            print ans," > ",s
                            sub=np.zeros((600,600,3), np.uint8)
                            self.add_numbers(sub,s,ans)
                            self.img_ans=self.add_warp_img(self.img,sub,cnt)
                            self.solved=True
                else:
                    self.solved=False
                    self.img_ans=None
                cv2.putText(self.img, "fps:" + str(self.get_fps((time.clock() - st))),
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 250, 0), 1)
                if self.showflag:  #
                    if self.img_ans!=None:
                        ret, mask = cv2.threshold(cv2.cvtColor(self.img_ans,cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY)
                        mask_inv=cv2.bitwise_not(mask) #
                        img1_bg = cv2.bitwise_and(self.img,self.img,mask = mask_inv)#
                        img2_fg = cv2.bitwise_and(self.img_ans,self.img_ans,mask = mask) #
                        self.img=cv2.add(img1_bg,img2_fg)
                    cv2.imshow(TITLE, self.img)
                    cv2.setMouseCallback(TITLE, self.on_mouse)  #
            except Exception,e:
                logging.exception("err")
            key = cv2.waitKey(20)
            if(key == 27):
                break  #
            if len(digits)>19:
                for i in range(len(digits)):
                    cv2.imwrite("./%s/%d.png"%(DATAPATH,i),digits[i])
                break
        self.cam.release()
        cv2.destroyAllWindows()
def unit_test():
    dd = [0 for i in range(10)]
    for i in range(10):
        dd[i] = cv2.imread("./%s/%d.png" % (DATAPATH,i),0)
        t,dd[i]=cv2.threshold(dd[i],0,255,cv2.THRESH_OTSU)
        cv2.imshow("%d"%i,dd[i])
        find(dd[i])
    find(dd[6])
    cv2.waitKey()
    
if __name__ == '__main__':
    board().run()
    #unit_test()