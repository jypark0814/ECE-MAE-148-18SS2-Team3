import Cam
import cfg2
import numpy as np
import time

#need given parameter
class Controller(object):
    
    def __init__(self):
        self.running=True
        self.PWM_Steering=0.0
        self.PWMLast_Steering=cfg2.PWMMid_Steering    
        self.PWM_Throttle=0.0
        self.PWMLast_Throttle=0.0
        self.ErrorLast_PWM_Steering=0.0
        self.PWM_Last_Throttle=0.0
        self.ErrorLast_distance=0.0
        self.PWMref_Steering=0.0
        self.depth_distance=0.0
        self.time_start=0.0
        self.time_passed=0.0
        self.donutReset=True
        self.dummySteeringReturn=0.0
        self.dummyThrottleReturn=0.0        
        
        
    def run(self, x,y,Current_radius,shape):
        #print('y dist:',y)
         if x is not 0: #If we found at least 1 contour
            print('x value is',x)
            print('Radius is', Current_radius)
            print('found something')
            print(shape)
            if Current_radius < 50:
               print('lets go')
               self.distance_calc(x,y,Current_radius)
               #print('theta center',self.theta_center)
                   
               if cfg2.Steering_Control_Option: #If implementing Control to Steering
                  print('Control Steering')
                  self.PWMref_Steering=cfg2.m_Steering*self.theta_center;
                  self.SteeringController()
                  self.PWM_Steering=self.PWM_Steering+cfg2.b_Steering;

               else:
                  self.PWM_Steering=cfg2.m_Steering*self.theta_center+cfg2.b_Steering; #What PWM value do we need to turn $

               self.ThrottleController() #Control Throttle
               self.PWM_Throttle=self.PWM_Throttle+cfg2.b_Throttle;
               Value=self.PWM_Steering
                      #print('value before',self.PWM_Steering)
               self.PWM_Steering=self.WithinBounds(Value,cfg2.PWMHigh_Steering,cfg2.PWMLow_Steering)
                      #print('value after',self.PWM_Steering)
               Value=self.PWM_Throttle
               self.PWM_Throttle=self.WithinBounds(Value,cfg2.PWMLow_Throttle,cfg2.PWMHigh_Throttle)
               x = 0

            else:
                   print('Arrive')
                   self.PWM_Throttle = 370
#            if Current_radius > cfg2.max_Pixel_Radius:
 #                self.PWM_Throttle = 370
         else:
            print('Not Found')
            self.PWM_Throttle=370
         return self.PWM_Steering, self.PWM_Throttle

    #distance_calc finds the distance the ball is from the RC car. This calculation
    #is split into an inverse function determined by pixel_radius=inverseConstant*distance^-1
    #and a linear function determined by pixel_radius=m_constant*distance+b_constant.
    #The linear function is applied for distances close to the RC car while inverse
    #function is used for far distances
    #Constants can be determined by manually calibrating by looking at the pixel radius
    #of your ball various distances. For a standard tenis ball using the SainSmart Wide
    #Angle Fish-eye Camera using 720x480 resolution, the following values were obtained:
    #       distance (ft):[0.167  .5   1   1.5  2   2.5   3   4   5   6   7   8]
    # pix Radius (pixels):[57     40  28  20   15   12    9   8   6   5   4   3]
    #Distance Value is returned in Inches and theta in degrees         
    def distance_calc(self,x,y,radius):
        if radius >cfg2.linear_inverse_boundary: #in the linear regime
            self.depth_distance=(radius-cfg2.b_const)*12/cfg2.m_const
            
        elif radius <=cfg2.linear_inverse_boundary:
            self.depth_distance=(cfg2.inverse_const*12/radius)

        x_pixel_distance=x-cfg2.Cam_Resolution[0]/2
        center_distance=x_pixel_distance*cfg2.Ball_radius/radius
        
        if center_distance!=0:
                self.theta_center = np.arctan2(center_distance,self.depth_distance)*180/np.pi
        else:
                self.theta_center =-999
    
    #If no ball is found for a certain time, doDonuts tells the car to do donuts
    #until it finds something           

    def doDonuts(self):
        
        self.time_passed=time.time()-self.time_start
        if self.time_passed>cfg2.donutTime:
            print('time passed, doing donuts')
            self.PWM_Throttle=cfg2.PWMDonuts_Throttle
            self.PWM_Steering=cfg2.PWMLow_Steering

        else:
            print('time not passed, not doing donuts')           
            self.PWM_Throttle=cfg2.PWMOff_Throttle
            self.PWM_Steering=self.PWM_Steering
    
    #ThrottleController/SteeringContoller applies PI control to the throttle, in which the reference
    #input is a desired distance and the plant is found by the linear interpolation
    #determined in cfg2.py. In this code, Tutstin's approximation at 20Hz is used to determine
    #the coefficients found in cfg2.Throttle_Controller  
    def SteeringController(self):
        self.Error_PWM_Steering=self.PWMRef_Steering-self.PWMLast_Steering;
        self.PWM_Steering=cfg2.k_Steering*(cfg2.Steering_Controller[0]*self.Error_PWM_Steering \
            +cfg2.Steering_Controller[1]*self.ErrorLast_PWM_Steering)+self.PWMLast_Steering;
        self.ErrorLast_PWM_Steering=self.Error_PWM_Steering;
        self.PWMLast_Steering=self.PWM_Steering;
    
    def ThrottleController(self):
        self.Error_distance=self.depth_distance/12-cfg2.Distance_Ref;
        self.PWM_Throttle=cfg2.k_Throttle*(cfg2.Throttle_Controller[0]*self.Error_distance+ \
            cfg2.Throttle_Controller[1]*self.ErrorLast_distance)+self.PWMLast_Throttle;
        self.ErrorLast_distance=self.Error_distance;
        self.PWMLast_Throttle=self.PWM_Throttle;

    
    #WithinBounds determines if the PWM values are within a certain bounds. If it is
    #above or below, returns the upper or lower boundary value
    def WithinBounds(self, Value,UpperBound,LowerBound):
        if Value>UpperBound:
            #print('Returning upper Value', UpperBound)
            return UpperBound
        elif Value<LowerBound:
            #print('Returning lower Value', LowerBound)
            return LowerBound
        else:
            return Value
            #print('Returning Same Value', Value)
    
    #Resets the controller values to zero to eliminate the integrator wind-up upon 
    #finding the ball and then searching again
    def ResetControlValues(self):
        print('reseting Control Values')
        self.PWM_Steering=0.0
        self.PWMLast_Steering=cfg2.PWMMid_Steering    
        self.PWM_Throttle=0.0
        self.PWMLast_Throttle=0.0
        self.ErrorLast_PWM_Steering=0.0
        self.PWM_Last_Throttle=0.0
        self.ErrorLast_distance=0.0
    
    def shutdown(self):
        print('reseting colors and y_limit')
        self.running=False
        cfg2.y_Limit_Current=cfg2.y_Limit


#SteeringPWMSender takes the PWM value for the steering and sends it to the car
class SteeringPWMSender(object):
    
    def __init__(self, steeringController):
        self.running=True
        self.steering_controller=steeringController
        
    def run(self,PWM_Steering):
        if PWM_Steering is not None:
            print('sending steering:',PWM_Steering)
            self.steering_controller.set_pulse(int(PWM_Steering))
        else:
            print('steering is none')

        
    def shutdown(self):
        self.running=False
        self.steering_controller.set_pulse(int(cfg2.PWMMid_Steering))


#ThrottlePWMSender takes the PWM value for the Throttle and sends it to the car
class ThrottlePWMSender(object):
    
    def __init__(self, ThrottleController):
        self.running=True
        self.throttle_controller=ThrottleController
        
    def run(self,PWM_Throttle):
        if PWM_Throttle is not None:
            print('sending throttle:',PWM_Throttle)
            self.throttle_controller.set_pulse(int(PWM_Throttle))
        else:
            self.throttle_controller.set_pulse(int(cfg2.PWMOff_Throttle))
        
    def shutdown(self):
        self.running=False
        self.throttle_controller.set_pulse(int(cfg2.PWMOff_Throttle))
