from time import time
import cv2
import numpy as np


class Camera(object):

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.detector = cv2.ORB(400)

    def deal_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp, desc = self.detector.detectAndCompute(img, None)
        img = cv2.drawKeypoints(img, kp)
        return img

    def get_frame(self):
        s, frame = self.cam.read()
        frame = self.deal_img(frame)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]  # quality
        f, buf = cv2.imencode('.jpg', frame, encode_param)
        buf_data = np.array(buf).tostring()
        return buf_data
