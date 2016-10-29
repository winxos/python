# coding:utf-8
'''
banknote recognition v2
winxos 2016-01-12
'''
import cv2
import numpy as np
import time
from datetime import datetime
import math


class board:
    mask = None
    board_field = None
    showflag = True
    exact = None
    moneys = []
    money_files = {
        "1b.png": "1 yuan back", "1f.png": "1 yuan front",
        "10b.png": "10 yuan back", "10f.png": "10 yuan front",
                   "20b.png": "20 yuan back", "20f.png": "20 yuan front",
                   "50b.png": "50 yuan back", "50f.png": "50 yuan front",
                   "100b.png": "100 yuan back", "100f.png": "100 yuan front",
                   "5b.png": "5 yuan back", "5f.png": "5 yuan front",
    }
    detector = cv2.ORB(400)
    norm = cv2.NORM_HAMMING
    matcher = cv2.BFMatcher(norm)

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 1280)
        self.cam.set(4, 720)
        w = self.cam.get(3)
        h = self.cam.get(4)
        print w, h
        cv2.namedWindow("cam")
        cv2.setMouseCallback("cam", self.on_mouse)

        # img1 = cv2.bilateralFilter(img1, 11, 17, 17) #
        # img1 = cv2.Canny(img1, 30, 200) # ±ßÔµcanny¼ì²â
        for d in self.money_files:
            print d
            img = cv2.imread(d)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            kp, desc = self.detector.detectAndCompute(img, None)
            img = cv2.drawKeypoints(img, kp)
            # cv2.imshow(self.money_files[d],img.copy())
            self.moneys.append((desc, self.money_files[d]))
        self.sum = 0
        self.pt = 0

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

    def rotate_about_center(self, src, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        rangle = np.deg2rad(angle)  # angle in radians
        # now calculate new image width and height
        nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
        nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array(
            [(nw - w) * 0.5, (nh - h) * 0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        return cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)

    def adjust(self, win, img, cnt):
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
        w, h = int(maxWidth / ratio), int(maxHeight / ratio)
        dst = np.array([
            [0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        exact = cv2.warpPerspective(img, M, (w, h))
        ans = self.recognition(exact)
        if ans != "":
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.putText(self.img, ans, (cx - maxWidth / 4, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 250), 3)
        # cv2.imshow(win,exact)

    def find_contours(self, img):
        img = cv2.GaussianBlur(img, (3, 3), 1)  #
        #t, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
        img = cv2.Canny(img, 100, 250)  #
        kernel = np.ones((3, 3), np.uint8)
        #img = cv2.erode(img, kernel)
        img = cv2.dilate(img, kernel)
        #img = cv2.erode(img, kernel)
        #img=cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        cv2.imshow("test", img)
        cnts, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        squares = []
        for cnt in cnts:
            cnt_len = cv2.arcLength(cnt, True)
            # cnt = cv2.approxPolyDP(cnt, 0.05 * cnt_len, True)  #
            # if len(cnt)==4 and cv2.isContourConvex(cnt) and
            # cv2.contourArea(cnt)>4000:   # 4 cv2.contourArea(cnt)
            if cv2.contourArea(cnt) > 100:   # 4 cv2.contourArea(cnt)
                x, y, w, h = cv2.boundingRect(cnt)
                #x,y,w,h = cv2.minAreaRect(cnt)
                rect = [(x, y), (x + w, y + h)]
                squares.append(rect)
        for i in range(len(squares)):
            # self.adjust(str(cv2.contourArea(squares[i])//5000),self.img,squares[i])
            #cv2.drawContours(self.img, squares, i, (0,i*100%255,255-i*100%255),2)
            cv2.rectangle(self.img, squares[i][0], squares[i][
                          1], (0, i * 100 % 255, 255 - i * 100 % 255), 2)

    def recognition(self, img):
        kp1, desc1 = self.detector.detectAndCompute(img, None)
        #img = cv2.drawKeypoints(img,kp1)
        for md, mn in self.moneys:
            matches = self.matcher.knnMatch(desc1, md, k=2)
            good = []
            for m, n in matches:
                # print m.distance, n.distance, m.distance / n.distance
                # filter those pts similar to the next good ones
                if m.distance < 0.7 * n.distance:
                    good.append(m)
            if len(good) > 10:
                # print mn,len(good)
                return mn
        return ""

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
                if self.showflag:  #
                    cv2.imshow("cam", self.img)
                    cv2.setMouseCallback("cam", self.on_mouse)  #
            except Exception,e:
                print(e)
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    b = board()
    b.run()
