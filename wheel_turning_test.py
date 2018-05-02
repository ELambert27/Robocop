from hardware import Distance_Sensor
from hardware import Wheel_Controller
import easygopigo3
import time

gpg = easygopigo3.EasyGoPiGo3()
ds = Distance_Sensor(gpg)
wc = Wheel_Controller(gpg)

wc.rotate_left(90)
time.sleep(.5)
wc.rotate_right(90)
time.sleep(.5)
wc.rotate_left(180)

