from hardware import Distance_Sensor
from hardware import Wheel_Controller
import easygopigo3
gpg = easygopigo3.EasyGoPiGo3()
ds = Distance_Sensor(gpg)
wc = Wheel_Controller(gpg)
ar = ds.sweep(0, 180, 90)

if(ar[1] >= 28):
    wc.move_cm(28)

