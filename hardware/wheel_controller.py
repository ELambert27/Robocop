import easygopigo3
from time import sleep

defaultSpeed = 50 
#speed is measured in degrees per second
defaultMotorPower = 50

class Wheel_Controller(object):    
    def __init__(self, gpg3):
        self.GPG = gpg3
        #self.GPG.set_speed(defaultSpeed)
        #self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, defaultMotorPower)
        #self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, defaultMotorPower)

    def rotateRight(self, degrees):
        self.GPG.turn_degrees(degrees, False)
        
    def rotateLeft(self, degrees):
        self.GPG.turn_degrees(-degrees, False)

    def turnBothWheels(self, degreesForward):
        self.GPG.drive_degrees(degreesForward)

    def move_cm(self, distance):
        #self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, defaultMotorPower)
        #self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, defaultMotorPower)
        self.GPG.drive_cm(distance)

