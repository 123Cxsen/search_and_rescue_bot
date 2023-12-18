#!/usr/bin/env python3
# ---  ---  ---  ---  ---  ---
# file name:    main.py
# author:       Alexandre MENSAH
# date:         2023 12 11
# ---  ---  ---
# ---  ---  ---  ---  ---
# file name:         SquarePattern.py
# description :      Movement plus rectracting square pattern + return to the origin after grabbing the object
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
ultrasonic_sensor = UltrasonicSensor()
claw_motor_right = MediumMotor(OUTPUT_B)
wheel_diameter=55.5
color = ColorSensor()
wheels = MoveDifferential( OUTPUT_D, OUTPUT_A, EV3Tire, 16 * STUD_MM)
gyro = GyroSensor()
wheels.gyro = GyroSensor()
timeout = 3000
drive_distance = 1500
    # --- VARIABLES
current_ang= 0
timecount = 0




# ---  FUNCTION DEFINITION  ---
# write function definitions here
# ---  ---  ---  ---  ---  ---  ---

def open_claw():
    claw_motor_right.on_for_seconds(speed=50, seconds=1)

def close_claw():
    claw_motor_right.on_for_seconds(speed=-50, seconds=1)

def find_and_grab_object():
    try:
        while True:
            distance = ultrasonic_sensor.distance_centimeters
            print("Distance to object:", distance, "cm")

            if distance <= 10: # Adjust this distance according to your needs
                print("Object detected - grabbing...")
                open_claw()
                sleep(2) # Adjust time to hold the object
                close_claw()
                sleep(1)
                close_claw()
                break # Exit the loop after grabbing the object

    except KeyboardInterrupt:
        # Stop motors and exit cleanly on Ctrl+C
        #claw_motor_left.off()
        claw_motor_right.off()


def Straight_distance ( speed, drive_distance):
    wheels.on_for_distance(speed, drive_distance)
    return

def Pivot(direction ="cw", angle= 90):
    current_ang = gyro.angle
    timecounter = 0

    if (direction == "cw"):
        while (current_ang +angle >= gyro.angle ):
            timecounter +=1
            if(timecounter == timeout):
                break

            wheels.on(10, -10)
        Stop()
        return 0
    elif (direction == "ccw"):
         while (current_ang - angle <= gyro.angle):
            if(timecounter == timeout):
                break
            timecounter +=1

            wheels.on(-10, 10)
         Stop()
         return 0

    else:
      print("specify cw or ccw")
    return 1

def PivotPID(angle= 90, speed=10, kp=0, ki=0, kd=0):
    current_ang = gyro.angle
    timecounter = 0
    pid_speed = speed
    old_pid_speed = speed

    if (angle == 0):
        return 1


    elif (angle > 0):
        while (current_ang + angle > gyro.angle +1):
            timecounter +=1
            if(timecounter >= timeout):
                print("Timed out")
                return 1
            ang_delta = current_ang +angle - gyro.angle

            #pid_speed -= ki * (pid_speed - old_pid_speed)

            pid_speed = speed + (kp * ang_delta)
            #old_pid_speed = pid_speed

            print("ang_delta\tpid_speed")
            print(ang_delta, "\t", pid_speed, "\t",timecounter, "\n\n\n\n")

            if (pid_speed >= 100):
                pid_speed =100
            elif (pid_speed <= 0):
                pid_speed =0

            wheels.on(pid_speed, -pid_speed)
        Stop()
        return 0


    elif (angle < 0):
        ang_delta = current_ang +angle + gyro.angle
        while (current_ang + angle < gyro.angle -1):
            timecounter +=1
            if(timecounter >= timeout):
                print("Timed out")
                return 1
            ang_delta = gyro.angle- (current_ang +angle)

            #pid_speed -= ki * (pid_speed - old_pid_speed)

            pid_speed = speed + kp * ang_delta 
            #old_pid_speed = pid_speed

            print("ang_delta\tpid_speed")
            print(ang_delta, "\t", pid_speed, "\t",timecounter, "\n\n\n\n")

            if (pid_speed >= 100):
                pid_speed =100
            elif (pid_speed <= 0):
                pid_speed = 0

            wheels.on(-pid_speed, pid_speed)
        Stop()
        return 0



    else:
      print("specify cw or ccw")
    return 1


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
    return

def run_grab_return(speed,turnspeed, kp):
    Straight(speed)
    try:
        while True:
            distance = ultrasonic_sensor.distance_centimeters
            print("Distance to object:", distance, "cm")

            if distance <= 10: # Adjust this distance according to your needs
                Stop()
                print("Object detected - grabbing...")
                open_claw()
                sleep(2) # Adjust time to hold the object
                close_claw()
                sleep(1)
                close_claw()
                wheels.on_to_coordinates(SpeedRPM(20),0,0)
                Stop()
                break # Exit the loop after grabbing the object

    except KeyboardInterrupt:
        # Stop motors and exit cleanly on Ctrl+C
        #claw_motor_left.off()
        claw_motor_right.off()



# ---  CODE START  ---
print("Hello, World!")
print("Init: DO NOT MOVE")
wheels.gyro.calibrate()
wheels.odometry_start()
color.calibrate_white()
print("Init: done, starting soon ...")

# try:
#     wheels.follow_gyro_angle(
#                     kp=11.3, ki=0.05, kd=3.2,
#                     speed=20,
#                     target_angle=45
#                 )
# except FollowGyroAngleErrorTooFast:
#     Stop()
#     raise

#---  CODE TEST DEF START  ---
def QuarterTurns( speed = 30, direction = "cw", kp = 0.3):
    timecount = 0

    Straight_distance(speed)
    while (True):
      timecount +=1
      if ( timecount == timeout):
        Stop()
        return

      if (color.color == 1):
            print("found edge")
            Stop()
            print("turning now")
            if (direction == "cw"):
                angle = -180
            else:
                angle = 180
            PivotPID(angle, speed, kp)
            QuarterTurns(speed, direction, kp)

    Stop()
    return


def RuntoLine (speed = 4):
    timecount = 0
    while (color.color != 1):
        timecount +=1
        if ( timecount == timeout):
            Stop()
            return

        Straight_distance(speed)
    while (color.color ==1):
        timecount +=1
        if ( timecount == timeout):
            Stop()
            return
, distance
        Straight_distance(2.5,distance)
        if (color.color !=1):
            Stop()
            break
    return
def RetractingSquare() :
    while (1) :
        wheels.on_for_distance(40)
