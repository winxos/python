# coding:utf-8
'''
money recognition
winxos 2016-01-05
'''
import cv2
import numpy as np
import time
from datetime import datetime


class board:
    mask = None
    board_field = None
    showflag = True

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 1280)
        self.cam.set(4, 720)
        cv2.namedWindow("cam")
        cv2.setMouseCallback("cam", self.on_mouse)

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

    def getROI(self, hsv, tmin, tmax):  # 普通组合滤波,hsv 格式
        thresh = cv2.inRange(hsv, tmin, tmax)  # 过滤
        thresh = cv2.bitwise_not(thresh)    #
        # thresh=cv2.GaussianBlur(thresh,(3,3),0) #高斯滤波
        #element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        # thresh=cv2.erode(thresh,element)
        return thresh

    def find_board(self, img):  # 找主面板
        img = cv2.GaussianBlur(img, (3, 3), 0)
        for gray in cv2.split(img):
            contours, hierarchy = cv2.findContours(
                img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                    # if cv2.contourArea(cnt)>500000 or
                    # cv2.contourArea(cnt)<100000:continue #面积判断
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.025 * cnt_len, True)  # 最小包裹矩形
                if len(cnt) == 4 and cv2.isContourConvex(cnt):
                    if cv2.contourArea(cnt) > 300:  # 根据实际情况调整，白板大概面积
                        self.mask = np.zeros(img.shape, np.uint8)
                        if self.board_field != None:
                            if abs(np.sum(np.array([cnt[0][0], cnt[1][0], cnt[2][0], cnt[3][0]]) -
                                          self.board_field)) > 10:  # 避免频繁调整造成抖动
                                self.board_field = np.array(
                                    [cnt[0][0], cnt[1][0], cnt[2][0], cnt[3][0]])
                        else:
                            self.board_field = np.array(
                                [cnt[0][0], cnt[1][0], cnt[2][0], cnt[3][0]])
                        cv2.drawContours(self.mask, [cnt], 0, 255, -1)
                        return

    def find_squares(self, img):
        # img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # img=cv2.bitwise_not(img)   #图像取反
        img = cv2.GaussianBlur(img, (5, 5), 0)  # Gauss滤波
        # t,img=cv2.threshold(img, 0, 255, cv2.THRESH_OTSU )  #二值化
        img = cv2.Canny(img, 2, 50)  # 边缘canny检测
        # img=cv2.erode(img,cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))) #膨胀算法
        # img=cv2.medianBlur(img,3) #中值滤波
        # self.hsv=img.copy()         #保存以便显示
        squares = []
        contours, hierarchy = cv2.findContours(
            img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 500000 or cv2.contourArea(cnt) < 1000:
                continue  # 面积判断
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)  # 最小包裹
            if len(cnt) == 4 and cv2.isContourConvex(cnt):  # 4边凸包
                squares.append(cnt)
        cv2.drawContours(self.img, squares, -1, (255, 128, 0), 3)

    def undistort(self, img):
        #K = np.array([[814.473, 0, 334.013], [0, 814.628, 231.335], [0, 0, 1]])
        #dist = np.array([-0.222065, -0.186763, 0.001787, 0.002108])
        # cv2.undistort(img, K, dist) #offical way to undistort
        h, w = img.shape[:2]  # img.shape[:2] -> (height,width)
        #src = np.array([[71,147],[1162,32],[185,616],[1209,606]],np.float32)
        src = np.array(self.board_field, np.float32)
        dst = np.array([[w - 300, 50], [50, 50], [50, h - 100],
                        [w - 300, h - 100]], np.float32)
        warp = cv2.getPerspectiveTransform(src, dst)  # 得到投影变换矩阵
        img = cv2.warpPerspective(img, warp, (w, h))  # 投影变换
        return img[55:h - 100, 55:w - 305]  # 图像裁边

    def run(self):  # 主函数
        while True:
            ret, self.img = self.cam.read()  # 读取摄像头图片
            # self.hsv=cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
            # self.hsv=self.getROI(self.hsv,target[0],target[1])
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            # t,self.hsv=cv2.threshold(self.hsv, 128, 255, cv2.THRESH_OTSU)   #大津法自动分割
            # self.find_board(self.hsv)
            # if self.mask != None:
            #    self.hsv=np.bitwise_and(self.hsv,self.mask) #遮罩层提取图像***
            #if self.board_field!=None:#
            # self.img=self.undistort(self.img)       #摄像头矫正

            self.find_squares(self.gray.copy())
            if self.showflag:  # 切换显示窗体
                cv2.imshow("cam", self.img)
                cv2.setMouseCallback("cam", self.on_mouse)  # 重新注册鼠标事件
                cv2.imshow("gray", self.gray)
            key = cv2.waitKey(20)
            if(key == 27):
                break  # esc退出程序
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    b = board()
    b.run()
