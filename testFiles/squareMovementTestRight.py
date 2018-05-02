from hardware import Distance_Sensor
from hardware import Wheel_Controller
import easygopigo3

gpg = easygopigo3.EasyGoPiGo3()
ds = Distance_Sensor(gpg)
wc = Wheel_Controller(gpg)

wc.move_cm(20)
wc.rotateRight(90)
wc.move_cm(20)
wc.rotateRight(90)
wc.move_cm(20)
wc.rotateRight(90)
wc.move_cm(20)
wc.rotateRight(90)




