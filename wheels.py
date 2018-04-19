from hardware import Wheel_Controller
import easygopigo3

GPG = easygopigo3.EasyGoPiGo3()

wh = Wheel_Controller(GPG)

wh.move_cm(1000)

