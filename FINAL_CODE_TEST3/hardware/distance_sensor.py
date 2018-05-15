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

        # Time to allow servo to move
        self.sleep_time = 0.5

    def get_valid_directions(self):
        directions = self.get_corridor_measurements()
        to_return = []         
        if directions[0] > 20:
            to_return.append('left')
        if directions[1] > 20:
            to_return.append('straight')
        if directions[2] > 20:
            to_return.append('right')
        return to_return

    def get_corridor_measurements(self):
        self.set_angle(180)
        time.sleep(.25)
        left  = self.get_distance()

        self.set_angle(90)
        time.sleep(.25)
        straight = self.get_distance()

        self.set_angle(0)
        time.sleep(.25)
        right = self.get_distance()

        return (left, straight, right)
 
    #SERVO IS UPSIDE DOWN, GO FROM LEFT TO RIGHT
    def sweep(self, left, right):
        for i in range(right, left, -1):
            self.set_angle(i)
            time.sleep(0.01)

    #SERVO IS UPSIDE DOWN, GO FROM LEFT TO RIGHT
    def sweep(self, left, right, inc):
        right += 1
        ret = []
        print(range(right, left, -inc))
        for i in range(right, left, -inc):
            self.set_angle(i)
            time.sleep(0.1)
            ret.append(self.get_distance())

        return ret

    def set_angle(self, angle):
        # Take into account the degree offset
        if (angle > (180 - self.degrees_offset)):
            angle = 180 - self.degrees_offset
        else:
            angle = angle - self.degrees_offset

        # Set the servo angle, and wait 
        self.servo.rotate_servo(angle)
        time.sleep(0.25)

    def get_distance(self):
        return self.distance_sensor.read()

    def get_distance_stream():
        while(True):
            yield self.distance_sensor.read()
