print("Helloworld")


from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from time import sleep

#CONSTANTS
Gyro = GyroSensor()
wheel_diameter=55.5
color = ColorSensor()
wheels = MoveTank( OUTPUT_D, OUTPUT_A)
timeout = 1000

#var
current_ang= 0
timecount = 0



def Straight ( speed ):
    wheels.on(speed, speed)
    print("moving straight at", speed, "speed !")
    return

def Turn(direction):
    current_ang = Gyro.angle
    
    if (direction == "cw"):
        while (current_ang <= Gyro.angle + 90 or current_ang >= Gyro.angle -90):
             wheels.on(10, -10)
        Stop()
        return
    elif (direction == "ccw"):
         while (current_ang <= Gyro.angle + 90 or current_ang >= Gyro.angle -90):
             wheels.on(-10, 10)
         Stop()
         return
    else:
      print("specify cw or ccw")
    return


def Stop (  ):
    wheels.on(0, 0)
    print("Stopping")
    return






# MAINSCRIPT
sleep(1)
print("Init: DO NOT MOVE")
gyro.calibrate
color.calibrate_white()

sleep(1)


Straight(50)
while (timecount < timeout):
  timecount +=1
  if (color.color == 1):
    Stop()
    sleep(1)
    Turn("cw")
    print("found edge")
    sleep(10)
    Stop()
    break
  if (timecount == timeout -2):
      print ("timed out")

Stop()

