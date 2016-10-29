# coding:utf-8
'''
money recognition v5
winxos 2016-01-09
'''
import math
from datetime import datetime

import cv2
import numpy as np


class board:
    mask = None
    board_field = None
    showflag = True
    exact = None
    moneys = []
    detector = cv2.ORB(400)
    norm = cv2.NORM_HAMMING
    matcher = cv2.BFMatcher(norm)

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        w = self.cam.get(3)
        h = self.cam.get(4)
        print w, h
        cv2.namedWindow("cam")
        cv2.setMouseCallback("cam", self.on_mouse)

        # img1 = cv2.bilateralFilter(img1, 11, 17, 17)  # 双边滤波
        # img1 = cv2.Canny(img1, 30, 200)  # 边缘canny检测

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print (x, y)
            if x < 100 and y < 100:  # 点击窗体左上角完成保存文件
                im = None
                if self.showflag:
                    im = self.img
                else:
                    im = self.hsv
                if im != None:  # 保存图片至png文件
                    cv2.imwrite(datetime.now().strftime(
                            "%m%d%H%M%S") + ".png", im)  # 时间
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

    def find_contours(self, img):
        self.gray = img.copy()
        # img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # img=cv2.bitwise_not(img)   #图像取反
        # img = cv2.GaussianBlur(img, (5, 5), 0)  # Gauss滤波
        # img = cv2.bilateralFilter(img, 11, 17, 17)  # 双边滤波
        t, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)  # 二值化
        # img = cv2.Canny(img, 30, 200)  # 边缘canny检测
        # img=cv2.dilate(img,cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))) #膨胀算法
        # img=cv2.medianBlur(img,3) #中值滤波
        # self.hsv=img.copy()         #保存以便显示

        cnts, _ = cv2.findContours(
                img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:20]
        squares = []
        for cnt in cnts:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.1 * cnt_len, True)  # 最小包裹
            if len(cnt) == 4 and cv2.contourArea(cnt) > 1000:  # 4边凸包 cv2.contourArea(cnt)
                squares.append(cnt)
                print cv2.contourArea(cnt)
        cv2.drawContours(self.img, squares, -1, (255, 128, 0), 3)

    def recognition(self, img):
        kp1, desc1 = self.detector.detectAndCompute(img, None)
        self.img = cv2.drawKeypoints(self.img, kp1)

    def distdiff(self, im1, im2, div):
        diff = cv2.bitwise_xor(im1, im2)
        return div*div-cv2.countNonZero(diff)

    def find_diff(self, im1, im2):
        div = 10
        lm = []
        for i in range(0, 320, div):
            for j in range(div * 2, 480, div):
                sim1 = im1[j:j + div, i:i + div]
                sim2 = im2[j:j + div, i:i + div]
                lm.append((self.distdiff(sim1, sim2, div), i, j))
        # print lm
        lm = sorted(lm)
        for i in range(len(lm)):
            if lm[i][0]>div*div*0.8:continue
            cv2.rectangle(self.img, (lm[i][1], lm[i][2]), (lm[i][1] + div, lm[i][2] + div), (0, i * 5, 255 - i * 5),
                          1)
            cv2.rectangle(self.img, (lm[i][1] + 320, lm[i][2]), (lm[i][1] + div + 320, lm[i][2] + div),
                          (0, i * 5, 255 - i * 5), 1)

    def run(self):  # 主函数
        while True:
            ret, self.img = self.cam.read()  # 读取摄像头图片
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            # self.find_contours(self.gray)
            # self.recognition(self.gray.copy())
            #self.hsv=cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV)
            #self.hsv[:,:,2]=128;
            #self.gray = cv2.GaussianBlur(self.gray, (5, 5), 0)  # Gauss滤波
            #self.gray = cv2.Canny(self.gray, 30, 200)  # 边缘canny检测
            t, self.gray = cv2.threshold(self.gray, 0, 255, cv2.THRESH_OTSU)  # 二值化
            im1 = self.gray[0:480, 0:320]
            im2 = self.gray[0:480, 320:640]
            # im2=cv2.Canny(im2, 30, 200)  # 边缘canny检测
            #im1 = cv2.GaussianBlur(im1, (5, 5), 0)  # Gauss滤波
            #t, im1 = cv2.threshold(im1, 0, 255, cv2.THRESH_OTSU)  # 二值化
            #im2 = cv2.GaussianBlur(im2, (5, 5), 0)  # Gauss滤波
            #t, im2 = cv2.threshold(im2, 0, 255, cv2.THRESH_OTSU)  # 二值化
            self.find_diff(im1, im2)

            # cv2.rectangle(self.img,(i,j),(i+div,j+div),(0,255,0),2)
            if self.showflag:  # 切换显示窗体
                cv2.line(self.img, (320, 0), (320, 480), (0, 0, 255), 3)
                cv2.imshow("cam", self.img)
                #cv2.imshow("hsv", self.hsv)
                cv2.imshow("v1", im1)
                cv2.imshow("v2", im2)
                cv2.setMouseCallback("cam", self.on_mouse)  # 重新注册鼠标事件
            key = cv2.waitKey(20)
            if (key == 27):
                break  # esc退出程序
        self.cam.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    b = board()
    b.run()
