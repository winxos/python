# coding:utf-8
'''
money recognition
winxos 2016-01-05
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

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        #self.cam.set(3, 3000)
        #self.cam.set(4, 3000)
        w = self.cam.get(3)
        h = self.cam.get(4)
        print w, h
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

    def find_squares(self, img):
        self.gray = img.copy()
        # img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # img=cv2.bitwise_not(img)   #图像取反
        # img = cv2.GaussianBlur(img, (5, 5), 0)  # Gauss滤波
        img = cv2.bilateralFilter(img, 11, 17, 17)  # 双边滤波
        # t,img=cv2.threshold(img, 0, 255, cv2.THRESH_OTSU )  #二值化
        img = cv2.Canny(img, 30, 200)  # 边缘canny检测
        # img=cv2.dilate(img,cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))) #膨胀算法
        # img=cv2.medianBlur(img,3) #中值滤波
        # self.hsv=img.copy()         #保存以便显示

        cnts, _ = cv2.findContours(
            img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:20]
        squares = []
        for cnt in cnts:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)  # 最小包裹
            if len(cnt) == 4 and cv2.isContourConvex(cnt):  # 4边凸包
                squares.append(cnt)
                break
        if len(squares) > 0:
            screenCnt = squares[0]
            pts = screenCnt.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")

            # the top-left point has the smallest sum whereas the
            # bottom-right has the largest sum
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            # compute the difference between the points -- the top-right
            # will have the minumum difference and the bottom-left will
            # have the maximum difference
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

            # ...and now for the height of our new image
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

            # take the maximum of the width and height values to reach
            # our final dimensions
            maxWidth = max(int(widthA), int(widthB))
            maxHeight = max(int(heightA), int(heightB))
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            self.exact = cv2.warpPerspective(
                self.img, M, (maxWidth, maxHeight))
            if maxWidth < maxHeight:
                self.exact = self.rotate_about_center(self.exact, 90)
            self.exact = cv2.GaussianBlur(self.exact, (7, 7), 0)
            self.exact = cv2.Canny(self.exact, 5, 100)

        cv2.drawContours(self.img, squares, -1, (255, 128, 0), 3)

    def undistort(self, img):
        # K = np.array([[814.473, 0, 334.013], [0, 814.628, 231.335], [0, 0, 1]])
        # dist = np.array([-0.222065, -0.186763, 0.001787, 0.002108])
        # cv2.undistort(img, K, dist) #offical way to undistort
        h, w = img.shape[:2]  # img.shape[:2] -> (height,width)
        # src = np.array([[71,147],[1162,32],[185,616],[1209,606]],np.float32)
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
                if self.exact != None:
                    cv2.imshow("exact", self.exact)
            key = cv2.waitKey(20)
            if(key == 27):
                break  # esc退出程序
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    b = board()
    b.run()
