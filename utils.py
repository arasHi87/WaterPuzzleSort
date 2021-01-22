import cv2
import random
import numpy as np
from pprint import pprint

def label_color(src):
    img = cv2.imread(src)
    kernel = np.ones((5,5), np.uint8)
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    open_img = cv2.morphologyEx(gray_img, cv2.MORPH_OPEN, kernel, iterations=3)
    erosion_img = cv2.erode(open_img, np.ones((20, 20), np.uint8), iterations=1)
    
    ret, binary = cv2.threshold(erosion_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE) 
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    temp = list()
    
    max_width = max(bounding_boxes, key=lambda r: r[0] + r[2])[0]
    max_height = max(bounding_boxes, key=lambda r: r[3])[3]
    nearest = max_height * 1.4
    bounding_boxes.sort(key=lambda r: (int(nearest * round(float(r[1])/nearest)) * max_width + r[0]))

    for bbox in bounding_boxes:
        [x, y, w, h] = bbox
        stk = list()
        
        mid_x = int(x+w/2)
        qut_h = int(h/4)
        y += int(qut_h/2)

        for i in range(3, -1, -1):
            b, g, r = img[y+qut_h*i, mid_x]
            stk.append([(r, g, b), 1])
       
        temp.append(stk)

    return temp

def merge_color(tubes):
    for stk in tubes:
        if stk:
            for idx in range(1, 4):
                if idx >= len(stk):
                    break

                if stk[idx] == stk[idx-1]:
                    stk[idx-1][1]+=1
                    del stk[idx]

    return tubes

def format_color(tubes):
    idx = 1
    cnvt = dict()
    cont = list()

    for stk in tubes:
        for ele in stk:
            if ele[0] not in cnvt:
                cnvt[ele[0]] = idx
                idx+=1
            ele[0]=cnvt[ele[0]]

    for key, val in cnvt.items():
        print("{}, {}".format(key, val))

    return tubes

if __name__ == "__main__":
    tubes = label_color('imgs/U3f38b6f273c8b7dbad03a7b0aa45c837.jpg')
    tubes = merge_color(tubes)
    tubes = format_color(tubes)

    pprint(tubes)

    for tube in tubes:
        for block in tube:
            print("{} {}".format(block[0], block[1]))
