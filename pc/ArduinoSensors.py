import array
import serial
import sys
import time
import struct
import logging
from serial.tools import list_ports
from threading import Thread
from threading import Event
from threading import Lock

print_errors = False
logger = logging.getLogger("arduino")

class ArduinoSensors():
    def __init__(self, print_errors = False):
        self._serial_port = None
        self._sensor_values = [0.0, 0.0, 0.0, 0.0]
        self._sensors = {"front": 2,
                         "back": 0,
                         "left": 1,
                         "right": 3}
        self._fresh_value = {"front": False,
                             "back": False,
                             "left": False,
                             "right": False}
        self._initialized = False
        self._last_read_at = time.clock()
        self._print_errors = print_errors

    def open(self):
        try:
            port = next(list_ports.grep("Arduino"))
        except StopIteration:
            self.__error("Arduino not found!")
            return False
        else:
            self._serial_port = serial.Serial(port.device, 9600, timeout = 2)
        self._serial_port.reset_input_buffer()
        self._serial_port.reset_output_buffer()
        self._initialized = True
        return True

    def close(self):
        self._serial_port.close()

    def __error(self, msg):
        if self._print_errors:
            print(msg)
        logger.error(msg)

    def __readline(self):
        line = []
        while self._serial_port.out_waiting > 0:
            pass
        while True:
            in_byte = self._serial_port.read()
            if not in_byte:
                break
            line.append(in_byte)
        if len(line) == 0:
            return b""
        return b"".join(line)

    def __read_sensors(self):
        if not self._initialized:
            self.__error("Run open() before trying to read sensors!")
            return False

        self._serial_port.write(b"A")
        line = self.__readline()
        try:
            self._sensor_values = list(struct.unpack("ffffc", line)[:-1])
        except struct.error:
            self.__error("Failed to convert line: {} (length {})".format(line, len(line)))
            return False
        self._fresh_value["front"] = True
        self._fresh_value["back"] = True
        self._fresh_value["left"] = True
        self._fresh_value["right"] = True
        self._last_read_at = time.clock()
        return True

    def __expired(self):
        now = time.clock()
        return now - self._last_read_at > 1.0

    def __get_sensor(self, sensor_name, block_until_ready = True):
        if self._fresh_value[sensor_name] and not self.__expired():
            value = self._sensor_values[self._sensors[sensor_name]]
            self._fresh_value[sensor_name] = False
            return value
        else:
            self.__read_sensors()
            return self._sensor_values[self._sensors[sensor_name]]

    def get_front(self):
        return self.__get_sensor("front")

    def get_back(self):
        return self.__get_sensor("back")

    def get_left(self):
        return self.__get_sensor("left")

    def get_right(self):
        return self.__get_sensor("right")
