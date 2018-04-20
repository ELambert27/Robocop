from hardware import Distance_Sensor
from hardware import Wheel_Controller
import easygopigo3
import random
import time

gpg = easygopigo3.EasyGoPiGo3()
ds = Distance_Sensor(gpg)
wc = Wheel_Controller(gpg)

def move():
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
    time.sleep(3)
    if(len(valid_choices) == 0):
        print("Turning around")
        wc.rotateLeft(180)
    else:
        choice = valid_choices[random.randint(0, len(valid_choices) - 1)]
        print("Chose ", choice)
        wc.move_cm(14)

        if(choice == 'left'):
            wc.rotateLeft(90)
        elif(choice == 'right'):
            wc.rotateRight(90)

    wc.move_cm(14)

def correct():
    ar = ds.sweep(0, 180, 15)

    print(ar)

correct()
