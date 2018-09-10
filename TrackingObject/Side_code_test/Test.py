import numpy as np
import time
import cv2
import io
import Cam

#ShapeDetector Import
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#PiCamera Import
from picamera.array import PiRGBArray
from picamera import PiCamera
import cfg2
from donkeycar.vehicle import Vehicle 
#import detect_shapes



#Create a memory stream so photos doesn't need to be saved in a file
#stream = io.BytesIO()
#Initialize Camera
camera = PiCamera()
rawCapture=PiRGBArray(camera, size=cfg2.Cam_Resolution)

#Set the resolution and framerate
camera.resolution = cfg2.Cam_Resolution
camera.framerate = cfg2.Cam_FrameRate

#Capture a frame
#Create a reference to the raw camera capture
rawCapture = PiRGBArray(camera, size = [720,480])
#Use the camera to take a raw image

#camera.capture(stream,format='jpeg')
#buff = np.fromstring(stream.getvalue(), dtype=np.uint8)
#img = cv2.imdecode(buff,1)
camera.capture(rawCapture, format='bgr',use_video_port=False)
img = rawCapture.array
cv2.imwrite('raw.jpg',img)
#Set color parameters
sensitivity = 35;
sens = 50;
red_lower = (170,50,70)
red_upper = (179,255,255)
red_lower2 = (0,70,50)
red_upper2 = (10,255,255)
green_lower = (60 - sensitivity,100,100)
green_upper = (60 + sensitivity, 255, 255)
blue_lower = (-3,100,100)
blue_upper = (17,255,255)
#Convert brg to hsv image
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#Draw hsv img
cv2.imwrite('hsv.jpg',img_hsv)

mask1 = cv2.inRange(img_hsv, red_lower, red_upper)
mask2 = cv2.inRange(img_hsv, red_lower2, red_upper2)
#img_inRange = cv2.bitwise_or(mask1,mask2)
img_inRange = cv2.inRange(img_hsv, red_lower, red_upper)
cv2.imwrite('inrange.jpg',img_inRange)

eroded_img = cv2.erode(img_inRange, None, iterations=4)

cv2.imwrite('eroded.jpg',eroded_img)
dilated_img_red = cv2.dilate(eroded_img, None, iterations=2)
cv2.imwrite('dilated_red.jpg',dilated_img_red)
contours_red = cv2.findContours(dilated_img_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

print ('Try finding red')
if len(contours_red)>0:
    image = dilated_img_red
    c = max(contours_red, key=cv2.contourArea)
    ((x,y),Current_radius) = cv2.minEnclosingCircle(c)
    print('Found Red')
    print('x coord is ', x)
    print('y coord is ', y)
    print('Radius is ', Current_radius)

else:
    print('Red not found. Try finding Green')

img_inRange = cv2.inRange(img_hsv, green_lower, green_upper)
#cv2.imwrite('inrange.jpg',img_inRange)

eroded_img = cv2.erode(img_inRange, None, iterations=4)

cv2.imwrite('eroded.jpg',eroded_img)
dilated_img_green = cv2.dilate(eroded_img, None, iterations=2)
cv2.imwrite('dilated_green.jpg',dilated_img_green)
contours_green = cv2.findContours(dilated_img_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

if len(contours_green)>0:
    image = dilated_img_green
    c = max(contours_green, key=cv2.contourArea)
    ((x,y),Current_radius) = cv2.minEnclosingCircle(c)
    print('Found Green')
    print('x coord is ', x)
    print('y coord is ', y)
    print('Radius is ', Current_radius)

else:
    print ('Green not found. Try finding Blue')
    #image = cv2.imread('shapes_and_colors.png',0)
    #resized = imutils.resize(image, width=300)
    #ratio = image.shape[0] / float(resized.shape[0])

    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
   # gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
   # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
   # thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
   # image = thresh.copy()
#img_inRange = cv2.inRange(img_hsv, blue_lower, blue_upper)
#cv2.imwrite('inrange.jpg',img_inRange)

#eroded_img = cv2.erode(img_inRange, None, iterations=4)

#cv2.imwrite('eroded.jpg',eroded_img)
#dilated_img = cv2.dilate(eroded_img, None, iterations=2)
#cv2.imwrite('dilated.jpg',dilated_img)
#contours_blue = cv2.findContours(dilated_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
#contours_blue=0
#if len(contours_blue)>0:
#    c = max(contours_blue, key=cv2.contourArea)
#    ((x,y),Current_radius) = cv2.minEnclosingCircle(c)
#    print('Found Blue')
#    print('x coord is ', x)
#    print('y coord is ', y)
#    print('Radius is ', Current_radius)
#else:
#    print('Blue not found')

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better

resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
blurred = cv2.GaussianBlur(resized, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# convert the resized image to grayscale, blur it slightly,
# and threshold it
#gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(resized, (5, 5), 0)
#thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

# loop over the contours
c = max(cnts,key=cv2.contourArea)
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
M = cv2.moments(c)
cX = int((M["m10"] / M["m00"]) * ratio)
cY = int((M["m01"] / M["m00"]) * ratio)
shape = sd.detect(c)

	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
c = c.astype("float")
c *= ratio
c = c.astype("int")
cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 5)


	# show the output image
plt.imshow(image, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.savefig('shapedetect.jpg')
print(shape)
