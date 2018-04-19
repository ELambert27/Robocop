import easygopigo3
import time

class Distance_Sensor(object):
    def __init__(self, gpg3):

        # Set the GoPiGo3 instance
        self.GPG = gpg3

        # The servo instance that controls the servo that moves the distance sensor
        self.servo = self.GPG.init_servo()

        # The distance sensor itself
        self.distance_sensor = self.GPG.init_distance_sensor()

        # The servo can go from 0 - 180 degrees, but has an offset of 15 degrees in relation to the robot's frame of reference
        self.degrees_offset = 15

        # Set the servo to 90 degrees
        self.set_angle(90)

    
    #SERVO IS UPSIDE DOWN, GO FROM LEFT TO RIGHT
    def sweep(self, left, right):
            for i in range(right, left, -1):
                self.set_angle(i)
                time.sleep(0.01)

    def set_angle(self, angle):
        # Take into account the degree offset
        if (angle > (180 - self.degrees_offset)):
            angle = 180 - self.degrees_offset
        else:
            angle = angle - self.degrees_offset

        self.servo.rotate_servo(angle)

    def get_distance(self):
        return self.distance_sensor.read()

    def get_distance_stream():
        while(True):
            yield self.distance_sensor.read()
