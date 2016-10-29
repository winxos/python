# coding:utf-8
'''
摄像头模板匹配内容识别测试 v0.1
opencv 2.4.11
不具备尺度与旋转不变性
winxos 2015-12-15
'''
import numpy as np
import argparse
import cv2
import time
import os


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target", required=True,
                    help="path to the target image")
    args = vars(ap.parse_args())
    target = cv2.imread(args["target"])
    (tarHeight, tarWidth) = target.shape[:2]
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("cam")
    cv2.namedWindow("target")

    while True:
        try:
            ret, src = cam.read()
            #TM_CCORR_NORMED ,TM_SQDIFF_NORMED ,TM_CCOEFF_NORMED 
            result = cv2.matchTemplate(src, target, cv2.TM_CCORR_NORMED)
            _, _, _, maxLoc = cv2.minMaxLoc(result)
            if src[maxLoc[1], maxLoc[0]][0] > 100:
                print src[maxLoc[1], maxLoc[0]]
                roi = src[maxLoc[1]:maxLoc[1] + tarHeight,
                          maxLoc[0]:maxLoc[0] + tarWidth]

                mask = np.zeros(src.shape, dtype="uint8")
                mask[maxLoc[1]:maxLoc[1] + tarHeight,
                     maxLoc[0]:maxLoc[0] + tarWidth] = roi
                src = cv2.addWeighted(src, 0.5, mask, 0.5, 0)
            #cv2.imshow("target", result)
            cv2.imshow("target", target)
            cv2.imshow("cam", src)
            # time.sleep(0.03)
            if cv2.waitKey(20) == 27:
                break
        except Exception, e:
            print(e)

    cv2.destroyAllWindows()
    # os._exit(0)
