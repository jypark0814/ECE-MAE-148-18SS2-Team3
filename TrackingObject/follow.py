from donkeycar.vehicle import Vehicle
from donkeycar.parts.controller import JoystickController, PS3JoystickController
from donkeycar.parts.throttle_filter import ThrottleFilter
from donkeycar.parts.transform import Lambda
from picamera.array import PiRGBArray
from picamera import PiCamera
from donkeycar.parts.actuator import PCA9685
import time
import Cam
import mod as FF
import cfg2

#Setup Vehicle, PWM senders, and Camera
V=Vehicle()
steering_controller = PCA9685(cfg2.Steering_Channel)
throttle_controller = PCA9685(cfg2.Throttle_Channel)

camera=PiCamera()
camera.resolution=cfg2.Cam_Resolution
camera.framerate = cfg2.Cam_FrameRate
rawCapture=PiRGBArray(camera, size=cfg2.Cam_Resolution)

#Setup Controller

cont_class = PS3JoystickController
ctr = cont_class(throttle_scale=cfg2.JOYSTICK_MAX_THROTTLE,
                                 steering_scale=cfg2.JOYSTICK_STEERING_SCALE,
                                 auto_record_on_throttle=cfg2.AUTO_RECORD_ON_THROTTLE)
print('Warming Cam...')
time.sleep(.5)
print('Camera Warmed')

#Add parts to the Donkeycar Vehicle
cam=Cam.CvCam(camera, rawCapture)
V.add(cam, outputs=["camera/image"],threaded=False)
print('Added Camera Part')

V.add(ctr,inputs=["camera/image"],outputs=['user/angle', 'user/throttle', 'user/mode','recording'],threaded = True)
print('Added PS3 Part')

th_filter = ThrottleFilter()
V.add(th_filter, inputs=['user/throttle'],outputs=['user/throttle'])


def drive_mode(mode,
               switch,user_throttle,pilot_throttle):
    if mode == 'user':
        return switch, pilot_throttle
    elif mode == 'local_angle':
        return switch, user_throttle
    else:
        return switch, pilot_throttle

drive_mode_part = Lambda(drive_mode)
V.add(drive_mode_part,
          inputs=['user/mode', 'recording', 'user/throttle','PWM_Throttle'],
          outputs=['switch', 'throttle'])
print('Added switch command part')


filterImage=Cam.ImageConvandFilter()
V.add(filterImage, inputs=["camera/image"], outputs=["x","y","Current_radius","shape"],threaded=False)
print('Added Filtering Part')

Controller=FF.Controller()
V.add(Controller,inputs=["x","y","Current_radius","shape"],outputs=["PWM_Steering","PWM_Throttle"], threaded=False)
print('Added Controller Part')

SteeringPWMSender=FF.SteeringPWMSender(steering_controller)
ThrottlePWMSender=FF.ThrottlePWMSender(throttle_controller)
#V.add(SteeringPWMSender,inputs=["PWM_Steering"],threaded=False)
#V.add(ThrottlePWMSender,inputs=["PWM_Throttle"],threaded=False)
print('Added PWMSending Parts')

V.add(SteeringPWMSender,inputs=["PWM_Steering"],threaded=False)
V.add(ThrottlePWMSender, inputs=['throttle'],threaded=False)


#Start the Vehicle
V.start()
