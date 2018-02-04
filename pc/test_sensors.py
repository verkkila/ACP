import ArduinoSensors
import time
import sys

sensors = ArduinoSensors.ArduinoSensors(poll_rate = 100)
sensors.open()
update_rate = 0.5
try:
    update_rate = float(sys.argv[1]) * 0.001
except (IndexError, TypeError):
    print("Using default refresh rate of {} ms".format(update_rate * 1000))

while True:
    try:
        print("Front: {:.4f}".format(sensors.get_front()))
        print("Back:  {:.4f}".format(sensors.get_back()))
        print("Left:  {:.4f}".format(sensors.get_left()))
        print("Right: {:.4f}".format(sensors.get_right()))
        time.sleep(update_rate)
    except KeyboardInterrupt:
        sensors.close()
        break
