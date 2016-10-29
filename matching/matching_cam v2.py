# coding:utf-8
'''
摄像头模板匹配内容识别 v2
具备尺度与旋转不变性
winxos 2015-12-15
'''
import numpy as np
import argparse
import cv2
import time
import os
orb = cv2.ORB()


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
    kp1, des1 = orb.detectAndCompute(target,None)
    print(len(kp1))
    while True:
        try:
            ret, src = cam.read()
            kp2, des2 = orb.detectAndCompute(src,None)
            # FLANN parameters
            '''
            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks=50)   # or pass empty dictionary

            flann = cv2.FlannBasedMatcher(index_params,search_params)

            matches = flann.knnMatch(des1,des2,k=2)

            # Need to draw only good matches, so create a mask
            matchesMask = [[0,0] for i in xrange(len(matches))]

            # ratio test as per Lowe's paper
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]

            draw_params = dict(matchColor = (0,255,0),
                               singlePointColor = (255,0,0),
                               matchesMask = matchesMask,
                               flags = 0)
            print(matches)
            '''
            src=cv2.drawKeypoints(src,kp2,color=(0,255,0),flags=0)
            ntar=cv2.drawKeypoints(target,kp1,color=(0,255,255),flags=0)
            #asrc = drawMatches(target,kp1,src,kp2,draw_params)
            #cv2.imshow("target", asrc)
            cv2.imshow("cam", src)
            cv2.imshow("target",ntar)
            # time.sleep(0.03)
            if cv2.waitKey(20) == 27:
                break
        except Exception, e:
            print(e)

    cv2.destroyAllWindows()
    # os._exit(0)
