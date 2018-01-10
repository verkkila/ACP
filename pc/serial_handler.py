import array
import array
import serial
from serial.tools import list_ports
from threading import Thread

import time

class ArduinoSensors(Thread):
    def __init__(self):
        self._serial_port = None
        self._sensor_0_value = 0.0
        self._sensor_1_value = 0.0
        self._sensor_2_value = 0.0
        self._sensor_3_value = 0.0
        Thread.__init__(self)

    def open(self):
        try:
            port = next(list_ports.grep("Arduino"))
        except StopIteration:
            print("Arduino not found!")
        else:
            self._serial_port = serial.Serial(port.device, 9600, timeout = 3)
            self._running = True
            self.start()
            print("Serial port opened and poll thread running")

    def close(self):
        self._running = False
        #wait for run() to stop before closing serial port
        self._serial_port.close()

    def run(self):
        while not self._serial_port:
            pass

        while self._running:
            line = self._serial_port.readline()
            line = line.rstrip(b"\n")
            data_floats = array.array("f", line)
            try:
                self._sensor_0_value = data_floats[0]
                self._sensor_1_value = data_floats[1]
                self._sensor_2_value = data_floats[2]
                self._sensor_3_value = data_floats[3]
            except IndexError:
                pass

    def get_front(self):
        return self._sensor_2_value

    def get_back(self):
        return self._sensor_0_value

    def get_left(self):
        return self._sensor_1_value

    def get_right(self):
        return self._sensor_3_value

sensors = ArduinoSensors()
sensors.open()
for i in range(0, 4):
    time.sleep(2)
    print("Front: {}".format(sensors.get_front()))
    print("Back:  {}".format(sensors.get_back()))
    print("Left:  {}".format(sensors.get_left()))
    print("Right: {}".format(sensors.get_right()))
sensors.close()
