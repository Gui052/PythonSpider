import numpy as np
import cv2
import os
import sys
from imutils import paths
from matplotlib import pyplot as plt #导入画图包
import matplotlib.cbook as cbook


dis=sys.path[0]+'/code'
# image_file = cbook.get_sample_data(dis)
# image = plt.imread(image_file)
# plt.imshow(image)
# plt.axis('off') # clear x- and y-axes
# plt.show()
for imagePath in paths.list_images(dis):

    image = cv2.imread(imagePath)
    imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for i in range(0,len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        cv2.rectangle(image, (x,y), (x+w,y+h), (153,153,0), 5)

        newimage = image[y + 2:y + h - 2, x + 2:x + w - 2]  # 先用y确定高，再用x确定宽
        nrootdir = ("cut_image/")
        if not os.path.isdir(nrootdir):
            os.makedirs(nrootdir)
        cv2.imwrite(nrootdir + str(i) + ".jpg", newimage)
        print(i)