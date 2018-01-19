import array
import serial
import sys
import time
from serial.tools import list_ports
from threading import Thread


class ArduinoSensors(Thread):
    def __init__(self):
        self._serial_port = None
        self._sensor_0_value = 0.0
        self._sensor_1_value = 0.0
        self._sensor_2_value = 0.0
        self._sensor_3_value = 0.0
        Thread.__init__(self)

    def open(self):
        if "-s" in sys.argv:
            try:
                self._serial_port = serial.Serial("/tmp/socatout", 9600, timeout = 3)
            except serial.serialutil.SerialException:
                print("Failed to open /tmp/socatout, is the virtual device running?")
                return False
        else:
            try:
                port = next(list_ports.grep("Arduino"))
            except StopIteration:
                print("Arduino not found!")
                return False
            else:
                self._serial_port = serial.Serial(port.device, 9600, timeout = 3)
        self._running = True
        self.start()
        print("Serial port opened and poll thread running")
        return True

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
            try:
                data_floats = array.array("f", line)
                self._sensor_lock.acquire(True)
                self._sensor_0_value = data_floats[0]
                self._sensor_1_value = data_floats[1]
                self._sensor_2_value = data_floats[2]
                self._sensor_3_value = data_floats[3]
                self._sensor_lock.release()
            except ValueError:
                print("Failed to convert line: {}(len: {})".format(line, len(line)))
                pass
            except IndexError:
                pass
        self._stop_event.set()

    def get_front(self, block_until_ready=True):
        if self._sensor_lock.acquire(block_until_ready):
            retval = self._sensor_2_value
            self._sensor_lock.release()
            return retval
        else:
            return 0.0

    def get_back(self, block_until_ready=True):
        if self._sensor_lock.acquire(block_until_ready):
            retval = self._sensor_0_value
            self._sensor_lock.release()
            return retval
        else:
            return 0.0

    def get_left(self, block_until_ready=True):
        if self._sensor_lock.acquire(block_until_ready):
            retval = self._sensor_1_value
            self._sensor_lock.release()
            return retval
        else:
            return 0.0

    def get_right(self, block_until_ready=True):
        if self._sensor_lock.acquire(block_until_ready):
            retval = self._sensor_3_value
            self._sensor_lock.release()
            return retval
        else:
            return 0.0

sensors = ArduinoSensors()
if not sensors.open():
    sys.exit()
time.sleep(1)
for i in range(0, 10):
    time.sleep(1)
    print("Front: {}".format(sensors.get_front()), end=" ")
    print("Back:  {}".format(sensors.get_back()), end=" ")
    print("Left:  {}".format(sensors.get_left()), end=" ")
    print("Right: {}".format(sensors.get_right()))
sensors.close()
