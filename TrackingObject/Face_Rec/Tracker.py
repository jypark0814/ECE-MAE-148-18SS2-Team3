import io
import os
import picamera
import numpy as np
import cv2

face_detect = cv2.CascadeClassifier('faces.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0)
cam.set(3, 720) # set video width
cam.set(4, 480) # set video height

count = 0

while(True):
   ret, img = cam.read()
   if ret is True :
    	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   else :
    	continue
   faces = face_detect.detectMultiScale(gray,1.3,5)

   for (x,y,h,w) in faces:
      cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
      cv2.putText(img,"face", (x,y+h),font, 1,(255,255,255),2)

cv2.imwrite("tracker/face."+str(count)+".jpg.", img)

count += 0

cam.release()
cv2.destroyAllWindows()
