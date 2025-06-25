from motionsensor import MotionSensor

motion_sensor = MotionSensor()

while True:
    motion_sensor.check_motion()
    motion_sensor.check_reset()