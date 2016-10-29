# coding:utf-8
'''
摄像头模板匹配内容识别 v2
OPENCV 2.4.11
ORB算法检测，
winxos 2015-12-18
'''
import numpy as np
import argparse
import cv2
import time
import os
#note that ORB became nonfree in cv 3.0
orb = cv2.ORB()

'''
self draw the matches because in cv 2.4.11 there
is no drawMatches function.
'''
def drawMatches(img1, kp1, img2, kp2): 
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]
    out = np.zeros((max([rows1, rows2]), cols1 + cols2, 3), dtype='uint8')
    out[:rows1, :cols1] = img1
    out[:rows2, cols1:] = img2
    for i in range(len(kp1)):
        (x1, y1) = kp1[i].pt
        (x2, y2) = kp2[i].pt
        cv2.circle(out, (int(x1), int(y1)), 10, (255, 0, 0), 1)
        cv2.circle(out, (int(x2) + cols1, int(y2)), 10, (255, 255, 0), 1)
        cv2.line(out, (int(x1), int(y1)),
                 (int(x2) + cols1, int(y2)), (255, 0, 255), 2)
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target", required=True,
                    help="path to the target image")
    args = vars(ap.parse_args())
    target = cv2.imread(args["target"])
    (tarHeight, tarWidth) = target.shape[:2]
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("cam")
    #cv2.namedWindow("target")
    kp1, des1 = orb.detectAndCompute(target, None)
    print(len(kp1))
    while True:
        try:
            ret, src = cam.read()
            kp2, des2 = orb.detectAndCompute(src, None)
            bf = cv2.BFMatcher()
            # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.knnMatch(des1, des2, k=2)

            # Apply ratio test
            p1, p2 = [], []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    p1.append(kp1[m.queryIdx])
                    p2.append(kp2[m.trainIdx])
            cv2.imshow("cam", drawMatches(src, p2, target, p1))
            # cv2.imshow("cam", src)
            # cv2.imshow("target",target)
            p1 = np.float32([kp.pt for kp in p1])
            p2 = np.float32([kp.pt for kp in p2])
            if len(p1) >= 4:
                H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
                print H
                print('%d / %d  inliers/matched' %
                      (np.sum(status), len(status)))
            if cv2.waitKey(10) == 27:
                break
        except Exception, e:
            print(e)

    cv2.destroyAllWindows()
    # os._exit(0)
