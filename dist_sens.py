from hardware import Distance_Sensor
from hardware import Wheel_Controller
import easygopigo3
gpg = easygopigo3.EasyGoPiGo3()
ds = Distance_Sensor(gpg)
wc = Wheel_Controller(gpg)

while(ds.get_distance() > 4):
    wc.move_cm(2)

wc.rotateLeft(90)
