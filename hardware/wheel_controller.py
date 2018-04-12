import easygopigo3
from time import sleep

class Wheel_Controller(object):    
    def __init__(self):
        self.GPG = easygopigo3.EasyGoPiGo3
        self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, 100)
        self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, 100)

    #for next three functions, /5 is because the encoding of the wheels is in increments of 5 degrees, 
    #so if we want to convert from degrees (given) to wheelIncrements (what we need to give), we divide by 5
    def turnLeftWheel(self, distance):
        self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, 100)
        self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, 0)
        self.GPG.drive_cm(distance)

    def turnRightWheel(self, distance):
        self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, 0)
        self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, 100)
        self.GPG.drive_cm(distance)

    def turnBothWheels(self, degreesForward):
        self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, 100)
        self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, 100)
        self.GPG.turn_degrees(degreesForward)

    def move_cm(self, distance):
        self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, 100)
        self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, 100)
        self.GPG.drive_cm(distance)

