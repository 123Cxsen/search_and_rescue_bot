#!/usr/bin/env python3
# ---  ---  ---  ---  ---  ---
# file name:    main.py
# author:       Alexandre EANG
# date:         2023 12 11
# ---  ---  ---
# ---  ---  ---  ---  ---
# file name:         SquarePattern.py
# description :      Movement plus rectracting square pattern
#
#
#
# author:            Alexandre EANG
# created on:        2023 12 11
# last updated:      2023 12 11
# updated by:        Alexandre EANG
# comment :          * Applied template to this document
# ---  ---   ---  ---  ---  ---



# ---  IMPORTS  ---  ---  ---  ---
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from time import sleep
# ---  ---   ---  ---  ---  --



# ---  DECLARATIONS  ---
    # --- CONSTANTS
wheel_diameter=55.5
color = ColorSensor()
wheels = MoveTank( OUTPUT_D, OUTPUT_A)
tank.gyro = GyroSensor()
timeout = 3000
    # --- VARIABLES
current_ang= 0
timecount = 0




# ---  FUNCTION DEFINITION  ---
# write function definitions here
# ---  ---  ---  ---  ---  ---  ---
def Straight ( speed ):
    wheels.on(speed, speed)
    print("moving straight at", speed, "speed !")
    return

def Pivot(direction, angle):
    current_ang = gyro.angle
    print(current_ang)
    timecounter = 0
    if (direction == "cw"):
        while (current_ang +angle >= gyro.angle ):
            timecounter +=1
            print(gyro.angle)
            wheels.on(10, -10)
            if(timecounter == timeout):
                break
        Stop()
        return
    elif (direction == "ccw"):
         while (current_ang - angle <= gyro.angle):
             timecounter +=1
             print(gyro.angle)
             wheels.on(-10, 10)
             if(timecounter == timeout):
                break
         Stop()
         return
    else:
      print("specify cw or ccw")
    return

def Turn(direction):
    current_ang = gyro.angle
    print(current_ang)
    timecounter = 0
    if (direction == "cw"):
        while (current_ang +180 >= gyro.angle ):
            timecounter +=1
            print(gyro.angle)
            wheels.on(10, 0)
            if(timecounter == timeout):
                break
        Stop()
        return
    elif (direction == "ccw"):
         while (current_ang - 180 <= gyro.angle):
             timecounter +=1
             print(gyro.angle)
             wheels.on(0, 10)
             if(timecounter == timeout):
                break
         Stop()
         return
    else:
      print("specify cw or ccw")
    return


def Stop (  ):
    wheels.on(0, 0)
    print("Stopping")
    return





# ---  CODE START  ---
print("Hello, World!")
print("Init: DO NOT MOVE")
tank.gyro.calibrate()
color.calibrate_white()
print("Init: done, starting soon ...")

try:
wheels.follow_gyro_angle(
                    kp=11.3, ki=0.05, kd=3.2,
                    speed=20,
                    target_angle=45,
                    follow_for=3000,
                    ms=4500
                )
except FollowGyroAngleErrorTooFast:
    Stop()
    raise



# Straight(50)
# while (timecount < timeout):
#   timecount +=1
#   if (color.color == 1):
#         print("found edge")
#         Stop()
#         print("turning now")
#         Turn("cw")
#         timecount = 0
#         Straight(20)
# Stop()