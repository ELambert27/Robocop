import gopigo3
import time

class Distance_Sensor:
    GPG = gopigo3.GoPiGo3()

    def move_degrees(self, left, right):
        for i in range(left, right):
            GPG.set_servo(GPG.SERVO_1, i)
            time.sleep(0.001)
