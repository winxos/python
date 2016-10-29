# coding:utf-8
'''
sudoku augmented reality v0.2 with python
solver from web
for sudoku+ game
winxos 2016-03-02
'''
import cv2
import numpy as np
import time
from datetime import datetime
import math
from sudokuSlove import Sudoku
digits = [0 for i in range(10)]
for i in range(9):
    digits[i] = cv2.imread("./v2data/%d.png" % (i + 1),0)
def find(img):
    #t, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
    m = 0
    ans = 0
    for i in xrange(9):
        res = cv2.matchTemplate(digits[i],img,cv2.TM_CCOEFF_NORMED)
        if res > m:
            m = res
            ans = i + 1
    #print m,ans
    if m[0] < 0.5:
        print "recognition miss ",m[0],ans
        ans = 0
    return "%d" % ans
def load_args(data):
    a = [None] * 9
    for i, d in enumerate(data.split()):
        a[i] = [int(c) for c in d]
    return a
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
    def save_sample(self):
        pass
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
        dst = np.array([[0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        return cv2.warpPerspective(img, M, (w, h))
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
        grids = 9
        gaph = h // grids
        gapw = w // grids
        for i in range(grids-1):
            cv2.line(img,(0,(i+1)*gaph),(w,(i+1)*gaph),(0,0,255),2)
            cv2.line(img,(0+(i+1)*gapw,0),((i+1)*gapw,h),(0,0,255),2)
        margin = 1
        ans = ""
        for i in xrange(9):
            for j in xrange(9):
                #print cv2.countNonZero(img[i * gapw + margin:i * gapw + gapw - margin,j * gapw + margin:j * gapw + gapw - margin])
                if cv2.countNonZero(img[i * gapw + margin:i * gapw + gapw - margin,j * gapw + margin:j * gapw + gapw - margin]) < 3900:
                    s = img[i * gapw + margin:i * gapw + gapw - margin,j * gapw + margin:j * gapw + gapw - margin]
                    mask = cv2.bitwise_not(s)
                    kernel = np.ones((5,5), np.uint8)
                    mask = cv2.dilate(mask, kernel)
                    mask = cv2.erode(mask, kernel)
                    kernel = np.ones((3,3), np.uint8)
                    mask = cv2.dilate(mask, kernel)
                    #mask = cv2.erode(mask, kernel)
                    #cv2.imshow("m%d"%(i*9+j+1),mask)
                    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
                    #print cnt
                    x, y, w, h = cv2.boundingRect(cnt)
                    sub = cv2.resize(s[y:y + h,x:x + w],(40,40))
                    #cv2.imshow("%d"%(i*9+j+1),sub)
                    #print "%d"%(i*9+j+1),w,h
                    #cv2.imwrite("./v2data/%d.png"%(i*9+j+1),sub)
                    ans+=find(sub)
                    cv2.resizeWindow("m%d"%(i*9+j+1),200,100)
                else:
                    ans+="0"
            ans+=" "
        #cv2.imshow("after", img)
        return ans
    def add_numbers(self,img,n,ans):#draw number
        w = img.shape[1]
        h = img.shape[0]
        grids = 9
        gap = h // grids
        margin = 15
        for i in xrange(9):
            for j in xrange(9):
                if ans[j * 10 + i] == "0":
                    cv2.putText(img, n[j * 9 + i],(i * gap + margin + gap / 5, j * gap + margin + gap / 2), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0,255, 0), 3)        
    def find_contours(self, img):#find main board
        img = cv2.GaussianBlur(img, (3, 3), 1)  #
        t, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
        #t, img = cv2.threshold(img,97,255,cv2.THRESH_BINARY)#
        kernel = np.ones((3,3), np.uint8)
        img = cv2.erode(img, kernel)
        img = cv2.dilate(img, kernel)
        img = cv2.erode(img, kernel)
        cnts, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0:5]
        #cv2.imshow("img",img)
        for cnt in cnts:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.01 * cnt_len, True)  #
            if len(cnt) == 4 and cv2.isContourConvex(cnt) and cv2.contourArea(cnt) > 50000:   # 4 cv2.contourArea(cnt)
                x0, y0, w0, h0 = cv2.boundingRect(cnt)
                dista=math.hypot(cnt[1][0][0]-cnt[0][0][0],cnt[1][0][1]-cnt[0][0][1])
                distb=math.hypot(cnt[3][0][0]-cnt[0][0][0],cnt[3][0][1]-cnt[0][0][1])
                #print dista,distb
                if dista>distb:
                    cnt[0][0][0]+=(cnt[1][0][0] - cnt[0][0][0]) * 0.07
                    cnt[0][0][1]+=(cnt[1][0][1] - cnt[0][0][1]) * 0.07
                    cnt[3][0][0]+=(cnt[2][0][0] - cnt[3][0][0]) * 0.07
                    cnt[3][0][1]+=(cnt[2][0][1] - cnt[3][0][1]) * 0.07
                else:
                    cnt[0][0][0]+=(cnt[3][0][0] - cnt[0][0][0]) * 0.07
                    cnt[0][0][1]+=(cnt[3][0][1] - cnt[0][0][1]) * 0.07
                    cnt[1][0][0]+=(cnt[2][0][0] - cnt[1][0][0]) * 0.07
                    cnt[1][0][1]+=(cnt[2][0][1] - cnt[1][0][1]) * 0.07
                cv2.drawContours(self.img, [cnt],-1, (0,0,255),1)
                #return
                print self.solved,x0,y0,w0,h0
                if not self.solved and  x0 > 10 and y0 > 10:#
                    ans=""
                    m=self.exact_img("sudoku",img,cnt)
                    #cv2.imshow("m",m)
                    ans=self.get_state(m)
                    if ans!="":
                        if not self.solved:
                            s=Sudoku(load_args(ans))
                            if not s.solve():
                                print "can't solved"
                                self.solved=False
                            else:
                                s=s.dump()
                                print ans," > ",s
                                sub=np.zeros((600,600,3), np.uint8)
                                self.add_numbers(sub,s,ans)
                                self.img_ans=self.add_warp_img(self.img,sub,cnt)
                    else:
                        self.solved=False
                    break
            else:
                self.solved = False
                self.img_ans = None
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
                self.find_contours(self.gray)
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
                cv2.imshow("sudoku ar v0.2", self.img)
                cv2.setMouseCallback("sudoku ar v0.1", self.on_mouse)  #
            except Exception,e:
                print(e)
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    b = board()
    b.run()
