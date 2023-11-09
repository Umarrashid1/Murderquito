import cv2 as cv
import numpy as np
import os
# working dir aendres tili mappen som det her koerer i
os.chdir(os.path.dirname(os.path.abspath(__file__)))

imgdot_cv = cv.imread("blackdot.png", 0)
imgdot_cv1 = cv.imread("blackdot.png",)
imggeek = cv.imread("geeks14.png", 0)
gray = cv.imread('black-dot1.jpg', 0) 

#cv.imshow("imgdot_cv", imgdot_cv)
#cv.imshow('imggeek', imggeek)
#cv.waitKey(0)  

th, threshed = cv.threshold(imgdot_cv, 100, 255, cv.THRESH_BINARY_INV)
# threshold 
#th, threshed = cv.threshold(gray, 100, 255, cv.THRESH_OTSU) 
# findcontours 
cnts, hierarchy = cv.findContours(threshed, 1,2) 
blablacnt = cnts[0]
M = cv.moments(blablacnt)
print(M)

#find midten af contour
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

#lav cirkel
(x_axis,y_axis),radius = cv.minEnclosingCircle(blablacnt) 

center = (cx, cy)
radius = 10 

cv.circle(imgdot_cv1, center,radius,(0,255,0),2) 
cv.imshow("imgdot_cv1", imgdot_cv1)
cv.waitKey(0) 
cv.destroyAllWindows()




#Take contour,
#1. find the centroid of the contour
#2. find distance from the centroid to each contour pixels.
#3. if this distance is almost same then it will be a circle.



# findcontours 
#cnts = cv.findContours(threshed, cv.RETR_LIST, 
#					cv.CHAIN_APPROX_SIMPLE)[-2]

# filter by area 
#s1 = 3
#s2 = 20
    #xcnts = [] 
    #for cnt in cnts: 
    #	if s1<cv.contourArea(cnt) <s2: 
    #		xcnts.append(cnt) 

s1 = 3
s2 = 400
xcnts = [] 
for cnt in cnts: 
	if s1<cv.contourArea(cnt) <s2: 
		xcnts.append(cnt) 



print("\nDots number: {}".format(len(xcnts))) 
print("\ndot coords: {}", cnts) 
print("\n\n\n\n\n", cx,)
print("\n\n\n\n\n", cy,)
 # do object detection
   # rectangles = cascade_limestone.detectMultiScale(screenshot)

    # draw the detection results onto the original image
        #detection_image = vision_limestone.draw_rectangles(screenshot, rectangles)

    # display the images
        #cv.imshow('Matches', detection_image)

