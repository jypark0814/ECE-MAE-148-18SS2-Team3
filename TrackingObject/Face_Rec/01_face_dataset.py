import os
import io
import picamera
import cv2
import numpy

#stream = io.BytesIO()

#with picamera.PiCamera() as camera:
#    camera.resolution = (720, 480)
#    camera.capture(stream, format='jpeg')

#buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

#cam = cv2.imdecode(buff, 1)


cam = cv2.VideoCapture(0)
cam.set(3, 720) # set video width
cam.set(4, 480) # set video height



face_detector = cv2.CascadeClassifier('faces.xml')

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look at the camera and wait ...")
# Initialize individual sampling face count
count = 0

while(True):

    ret, img = cam.read()
    if ret is True :
    	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
    	continue
    #img = cv2.imread('01test.jpg')
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        #cv2.imshow('image', img)
 
#    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
#    if k == 27:
#        break
#    elif count >= 30: # Take 30 face sample and stop video
#         break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
