import easygopigo3
from time import sleep
from hardware import Distance_Sensor

defaultSpeed = 50 
#speed is measured in degrees per second
defaultMotorPowerLeft = 50
defaultMotorPowerRight = 50.0000001

class Wheel_Controller(object):    
    def __init__(self, gpg3):
        self.GPG = gpg3
        self.DS = Distance_Sensor(self.GPG)
        #self.GPG.set_speed(defaultSpeed)
        #self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, defaultMotorPowerLeft)
        #self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, defaultMotorPowerRight)

    def rotateRight(self, degrees):
        self.TO_TURN = degrees
        if self.TO_TURN >= 90:
            self.TO_TURN = self.TO_TURN + 10
        #if self.TO_TURN >= 180:
        #    self.TO_TURN = self.TO_TURN + 5
        if self.TO_TURN >= 360:
            self.TO_TURN = self.TO_TURN + 10
        print(self.TO_TURN)
        self.GPG.turn_degrees(self.TO_TURN, True)
        
    def rotateLeft(self, degrees):
        self.TO_TURN = degrees
        if self.TO_TURN >= 90:
            self.TO_TURN = self.TO_TURN + 10
        #if self.TO_TURN >= 180:
        #    self.TO_TURN = self.TO_TURN + 5
        if self.TO_TURN >= 360:
            self.TO_TURN = self.TO_TURN + 10
        self.GPG.turn_degrees(-self.TO_TURN, True)

    def turnBothWheels(self, degreesForward):
        self.GPG.drive_degrees(degreesForward)

    def move_cm(self, distance):
        #self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, defaultMotorPowerLeft)
        #self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, defaultMotorPowerRight)
        self.GPG.drive_cm(distance)
        #self.GPG.set_motor_power(self.GPG.MOTOR_LEFT, 0)
        #self.GPG.set_motor_power(self.GPG.MOTOR_RIGHT, 0)

