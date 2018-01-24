import array
import serial
import sys
import time
import struct
from serial.tools import list_ports
from threading import Thread
from threading import Event
from threading import Lock

class ArduinoSensors(Thread):
    def __init__(self):
        self._serial_port = None
        self._sensor_values = [0.0, 0.0, 0.0, 0.0]
        self._sensors = {"front": 2,
                         "back": 0,
                         "left": 1,
                         "right": 3}
        self._stop_event = Event()
        self._sensor_lock = Lock()
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
        self._stop_event.wait()
        self._serial_port.close()

    def run(self):
        while not self._serial_port:
            pass

        while self._running:
            line = self._serial_port.readline()
            self._sensor_lock.acquire(True)
            try:
                self._sensor_values = list(struct.unpack("ffffc", line)[:-1])
            except struct.error:
                print("Failed to convert line: {} (length {})".format(line, len(line)))
            self._sensor_lock.release()
        self._stop_event.set()

    def get_front(self, block_until_ready=True):
        if self._sensor_lock.acquire(block_until_ready):
            sensor_value = self._sensor_2_value
            self._sensor_lock.release()
            return sensor_value
        else:
            return 0.0

    def get_back(self, block_until_ready=True):
        if self._sensor_lock.acquire(block_until_ready):
            sensor_value = self._sensor_0_value
            self._sensor_lock.release()
            return sensor_value
        else:
            return 0.0

    def get_left(self, block_until_ready=True):
        if self._sensor_lock.acquire(block_until_ready):
            sensor_value = self._sensor_1_value
            self._sensor_lock.release()
            return sensor_value
        else:
            return 0.0

    def get_right(self, block_until_ready=True):
        if self._sensor_lock.acquire(block_until_ready):
            sensor_value = self._sensor_3_value
            self._sensor_lock.release()
            return sensor_value
        else:
            return 0.0

if __name__ == "__main__":
    sensors = ArduinoSensors()
    if not sensors.open():
        sys.exit()
    try:
        while True:
            time.sleep(1)
            print("Front: {}".format(sensors.get_front()), end=" ")
            print("Back:  {}".format(sensors.get_back()), end=" ")
            print("Left:  {}".format(sensors.get_left()), end=" ")
            print("Right: {}".format(sensors.get_right()))
    except KeyboardInterrupt:
        sensors.close()
