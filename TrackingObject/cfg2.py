#Throttle Control
k_Throttle=5; #Proportional Value for Throttle
Throttle_Controller=[.025,.025] #Tustins Approximatinon for D=1/s at 20 Hz
PWMHigh_Throttle=348.0 #Max PWM Allowable
PWMLow_Throttle=350.0 #Low PWM
PWMOff_Throttle=360 #Assures off for Throttle
PWMDonuts_Throttle=351.0
MaxDistance=15.0 #Distance to Apply high PWM
MinDistance=1.0 #Distance to Apply Low PWM
Distance_Ref=0.0 #Desired Distance
Throttle_Channel=2


Steering_Control_Option=False 
k_Steering=10.0 
Steering_Controller=[.025,.025] 
PWMHigh_Steering=370.0; 
PWMLow_Steering=230.0; 
InnerWheelTheta=35.0; 
OuterWheelTheta=25.0;
ThetaRef=0.0;
Steering_Channel=1


MaxThetaTurn=(InnerWheelTheta+OuterWheelTheta)/2; 
PWMMid_Steering=(PWMHigh_Steering+PWMLow_Steering)/2
m_Throttle=(PWMLow_Throttle-PWMHigh_Throttle)/(MaxDistance-MinDistance);
b_Throttle=PWMHigh_Throttle+m_Throttle*MaxDistance;
m_Steering=(PWMHigh_Steering-PWMLow_Steering)/(MaxThetaTurn-(-MaxThetaTurn)); 
b_Steering=PWMHigh_Steering-m_Steering*MaxThetaTurn; 


Cam_Resolution=[720,480]
Cam_FrameRate=20

#Depth Distance Calculation
m_const=-51
b_const=65.5
inverse_const=30
linear_inverse_boundary=42


red_lower = (170,50,70)
red_upper = (179,255,255)
green_lower = (25,100,100)
green_upper = (95, 255, 255)
blue_lower = (100,150,0)
blue_upper = (140,255,255)
Ball_radius=1.375

#Ball Search Conditions
y_Limit=450 #Closeness of ball to stop Taking Action
y_Limit_Current=450
min_Pixel_Radius=20
max_Pixel_Radius=30 
y_Limit2=350


#JOYSTICK
USE_JOYSTICK_AS_DEFAULT = True
JOYSTICK_MAX_THROTTLE = 0.3
JOYSTICK_STEERING_SCALE = 1.0
AUTO_RECORD_ON_THROTTLE = True
CONTROLLER_TYPE='ps3' #(ps3|ps4)
USE_NETWORKED_JS = False
NETWORK_JS_SERVER_IP = "192.168.0.1"


#Switch
