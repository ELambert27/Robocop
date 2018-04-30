import easygopigo3
from time import sleep
from hardware import Distance_Sensor
import random
import math

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

    def move_and_correct(self, distance):
        self.DS.set_angle(180)
        time.sleep(1)
        firstReading = self.DS.get_distance()
        self.DS.set_angle(90)
        time.sleep(1)
        forwardDistance = ds.get_distance()
        if forwardDistance < distance:
            forwardDistance = forwardDistance - 2
        else:
            forwardDistance = distance
        self.move_cm(forwardDistance)
        self.DS.set_angle(180)
        time.sleep(1)
        secondReading = self.DS.get_distance()
        if abs(secondReading - firstReading) > .25 and abs(secondReading - firstReading) < 7 and forwardDistance != 0 and (firstReading < 14 or secondReading < 14):
            angleInRadians = math.atan(float(secondReading)/ (float(forwardDistance) + float(-forwardDistance) * float(firstReading))/(float(firstReading) - float(secondReading))))
            angleInDegrees = angleInRadians * 180 / math.pi
            self.move_cm(-forwardDistance)
            self.rotateLeft(angleInDegrees)
            self.move_cm(forwardDistance)
        self.DS.set_angle(180)
        time.sleep(1)
        afterMoveReadingLeft = self.DS.get_distance()
        if afterMoveReadingLeft < 11.5:
            offset = distance - 2.5 - afterMoveReadingLeft
            self.rotateLeft(30)
            self.sleep(1)
            self.move_cm(-(offset / math.sin(math.pi/6)))
            time.sleep(1)
            self.rotateRight(30)
            time.sleep(1)
            self.move_cm(offset / math.tan(math.pi/6))


    def move_and_navigate(self):
        self.move_and_correct(14)
        ar = self.DS.sweep(0, 180, 90)
        valid_choices = []
        if ar[0] > 17:
            valid_choices.append('left')
        if ar[1] > 17:
            valid_choices.append('straight')
        if ar[2] > 17:
            valid_choices.append('right')
        if len(valid_choices) == 0:
            #turning around
            self.move_and_correct(14)
            time.sleep(.25)
            self.rotateLeft(180)
        else:
            choice = valid_choices[random.randint(0, len(valid_choices) - 1)]
            self.move_and_correct(14)
            time.sleep(.25)
            if choice == 'left':
                self.rotateLeft(90)
            if choice == 'right':
                self.rotateRight(90)


    def go(self):
        while True:
            self.move_and_navigate()











