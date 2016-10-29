# coding:utf-8
'''
摄像头模板匹配内容识别 v5
OPENCV 2.4.11
ORB算法检测，仿射矫正
winxos 2015-12-18
'''
import numpy as np
import argparse
import cv2
import time
import os
import random
# note that ORB became nonfree in cv 3.0
orb = cv2.ORB()

'''
draw the matches because in cv 2.4.11 there
is no drawMatches function.
'''
def drawMatches(img1, kp1, img2, kp2, matches):
    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1, rows2]), cols1 + cols2, 3), dtype='uint8')

    # Place the first image to the left
    out[:rows1, :cols1, :] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2, cols1:cols1 + cols2, :] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:
        mat = mat

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1, y1) = kp1[img1_idx].pt
        (x2, y2) = kp2[img2_idx].pt
        cv2.circle(out, (int(x1), int(y1)), 4, (255, 0, 0), 1)
        cv2.circle(out, (int(x2) + cols1, int(y2)), 4, (255, 0, 0), 1)

        f = lambda : random.randint(1, 255)
        line_color = (f(), f(), f())
        cv2.line(out, (int(x1), int(y1)), (int(x2) + cols1, int(y2)), line_color, 1)
    return out

def find_show(img1, img2):
    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher()
    # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.knnMatch(des1, des2, k=2)

    print len(matches), "feature points found"

    good = []
    for m, n in matches:
        # print m.distance, n.distance, m.distance / n.distance
        # filter those pts similar to the next good ones
        if m.distance < 0.7 * n.distance:
            good.append(m)
    print len(good), "good feature points"

    # require count >= 4 in function cvFindHomography
    if len(good) >= 5:
        sch_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        img_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # M是转化矩阵
        M, mask = cv2.findHomography(sch_pts, img_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        print M
        print img2
        # 计算四个角矩阵变换后的坐标，也就是在大图中的坐标
        h, w = img2.shape
        pts = np.float32(
            [[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        cv2.polylines(img1,[np.int32(dst)],True,255,3)
    cv2.imshow("2",drawMatches(img1, kp1, img2, kp2, good))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target", required=True,
                    help="path to the target image")
    args = vars(ap.parse_args())
    target = cv2.imread(args["target"],0)
    cam = cv2.VideoCapture(0)
    #cv2.namedWindow("cam")
    # cv2.namedWindow("target")
    while True:
        try:
            ret, src = cam.read()
            find_show(cv2.cvtColor(src,cv2.COLOR_BGR2GRAY),target)
            if cv2.waitKey(10) == 27:
                break
        except Exception, e:
            print(e)

    cv2.destroyAllWindows()
    # os._exit(0)
