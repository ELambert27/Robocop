import easygopigo3
import time

class Distance_Sensor(object):
    def __init__(self):
        self.GPG = easygopigo3.EasyGoPiGo3()
        self.servo = self.GPG.init_servo()
        self.distance_sensor = self.GPG.init_distance_sensor()

    #SERVO IS UPSIDE DOWN, GO FROM LEFT TO RIGHT
    def move_degrees(self, left, right):
            self.servo.rotate_servo(right)
            for i in range(right, left, -1):
                self.servo.rotate_servo(i)
                time.sleep(0.01)

    def set_angle(self, angle):
        self.servo.rotate_servo(angle)
        time.sleep(1)

    def get_distance(self):
        return self.distance_sensor.read()

    def get_distance_stream():
        while(True):
            yield self.distance_sensor.read()
