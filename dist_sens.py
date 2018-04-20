from hardware import Distance_Sensor
from hardware import Wheel_Controller
import easygopigo3
import random
import time
import math

gpg = easygopigo3.EasyGoPiGo3()
ds = Distance_Sensor(gpg)
wc = Wheel_Controller(gpg)

def move_and_correct(distance):
    
    print("--running move_and_correct--")
    ds.set_angle(180)
    time.sleep(1)
    firstReading = ds.get_distance()
    print("first reading:", firstReading)
    ds.set_angle(90)
    time.sleep(1)
    forwardDistance = ds.get_distance()
    
    if forwardDistance < distance:
        forwardDistance = forwardDistance - 2
    else:
        forwardDistance = distance
    
    print("forward distance:", forwardDistance)
    wc.move_cm(forwardDistance)
    ds.set_angle(180)
    time.sleep(1)
    secondReading = ds.get_distance()
    print("second reading:", secondReading)
    if abs(secondReading - firstReading) > .25 and abs(secondReading - firstReading) < 7  and forwardDistance != 0 and (firstReading < 14 or secondReading < 14):
        print("forwardDistance:", forwardDistance)
        angleInRadians = math.atan(float(secondReading) / (float(forwardDistance) + (float(-forwardDistance) * float(firstReading))/(float(firstReading) - float(secondReading))))
        print("radians:", angleInRadians)
        angleInDegrees = angleInRadians * 180 / math.pi
        print("angle is:", angleInDegrees)
        wc.move_cm(-forwardDistance)
        if secondReading > firstReading:
            wc.rotateLeft(angleInDegrees)
        else:
            wc.rotateLeft(angleInDegrees)
        wc.move_cm(forwardDistance)
   
    ds.set_angle(180)
    time.sleep(1)
    afterMoveReadingLeft = ds.get_distance()
    print("afterMoveReadingLeft", afterMoveReadingLeft)
    print("----")
    if afterMoveReadingLeft < 11.5:
        offset = 14 - 2.5 - afterMoveReadingLeft
        print("off center left:", offset)
        wc.rotateLeft(30)
        time.sleep(1)
        wc.move_cm(-(offset / math.sin(math.pi/6)))
        time.sleep(1)
        wc.rotateRight(30)	
        time.sleep(1)
        wc.move_cm(offset / math.tan(math.pi/6))

    if afterMoveReadingLeft > 13 and afterMoveReadingLeft < 28:
        offset = afterMoveReadingLeft - (14 - 2.5)
        print("off center left:", offset)
        wc.rotateRight(30)
        time.sleep(1)
        wc.move_cm(-(offset / math.sin(math.pi/6)))
        time.sleep(1)
        wc.rotateLeft(30)
        time.sleep(1)
        wc.move_cm(offset / math.tan(math.pi/6))


    

def move():
    move_and_correct(14)

    ar = ds.sweep(0, 180, 90)
    print("Distances: " + str(ar))
    valid_choices = []
    if(ar[0] > 17):
        print("Left is valid")
        valid_choices.append('left')
    if(ar[1] > 17):
        print("Straight is valid")
        valid_choices.append('straight')
    if(ar[2] > 17):
        print("Right is valid")
        valid_choices.append('right')
    time.sleep(1)
    if(len(valid_choices) == 0):
        print("Turning around")
        move_and_correct(14)
        time.sleep(.25)
        #ds.set_angle(90)
        #time.sleep(1)
        #if(ds.get_distance() < 14):
        #    wc.move_cm(ds.get_distance() - 2)
        #else:            
        #    wc.move_cm(14)
        wc.rotateLeft(180)
    else:
        choice = valid_choices[random.randint(0, len(valid_choices) - 1)]
        print("Chose ", choice)
        #ds.set_angle(90)
        #time.sleep(1)
        #if(ds.get_distance() < 14):
        #    wc.move_cm(ds.get_distance() - 2)
        #else:
        #    wc.move_cm(14)
        move_and_correct(14)
        time.sleep(.25)
        if(choice == 'left'):
            wc.rotateLeft(90)
        elif(choice == 'right'):
            wc.rotateRight(90)


def correct():
    ar = ds.sweep(0, 180, 15)

    print(ar)

while True:
    move()
