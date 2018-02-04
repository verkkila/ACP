import array
import serial
import sys
import time
import struct
from serial.tools import list_ports
from threading import Thread
from threading import Event
from threading import Lock

print_errors = False

class ArduinoSensors(Thread):
    def __init__(self, poll_rate = 300):
        self._serial_port = None
        self._sensor_values = [0.0, 0.0, 0.0, 0.0]
        self._sensors = {"front": 2,
                         "back": 0,
                         "left": 1,
                         "right": 3}
        self._poll_rate = poll_rate
        self._first_line_read = False
        self._stop_event = Event()
        self._init_event = Event()
        self._sensor_lock = Lock()
        Thread.__init__(self, daemon = True)

    def open(self):
        try:
            port = next(list_ports.grep("Arduino"))
        except StopIteration:
            print("Arduino not found!")
            return False
        else:
            self._serial_port = serial.Serial(port.device, 9600, timeout = 2)
        self._running = True
        self.start()
        print("Serial port opened and polling thread started.")
        self._serial_port.reset_input_buffer()
        self._serial_port.reset_output_buffer()
        self._init_event.set()
        self._serial_port.write(b"A")
        return True

    def close(self):
        self._running = False
        self._stop_event.wait()
        self._serial_port.close()

    def set_update_rate(self, new_ms):
        self._poll_rate = new_ms

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
        if not self._first_line_read:
            self._first_line_read = True
        return b"".join(line)

    def run(self):
        self._init_event.wait()

        while self._running:
            self._serial_port.write(b"A")
            line = self.__readline()
            self._sensor_lock.acquire(True)
            try:
                self._sensor_values = list(struct.unpack("ffffc", line)[:-1])
            except struct.error:
                if print_errors:
                    print("Failed to convert line: {} (length {})".format(line, len(line)))
            self._sensor_lock.release()
            time.sleep(0.001 * self._poll_rate)
        self._stop_event.set()

    def __get_sensor(self, sensor_name, block_until_ready = True):
        while not self._first_line_read:
            pass
        if self._sensor_lock.acquire(block_until_ready):
            try:
                sensor_value = self._sensor_values[self._sensors[sensor_name]]
            except KeyError:
                print("Sensor {} doesn't exist.".format(sensor_name))
            self._sensor_lock.release()
            return sensor_value
        else:
            return 0.0

    def get_front(self):
        return self.__get_sensor("front")

    def get_back(self):
        return self.__get_sensor("back")

    def get_left(self):
        return self.__get_sensor("left")

    def get_right(self):
        return self.__get_sensor("right")
