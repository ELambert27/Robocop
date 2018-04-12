from hardware import Distance_Sensor

ds = Distance_Sensor()
print(ds.get_distance())
ds.set_angle(0)
#ds.move_degrees(90, 90)

ds.move_degrees(0, 180)
