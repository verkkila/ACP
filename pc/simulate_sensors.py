import struct
import sys
import noise
import math
import time

#seconds
data_rate = 0.5

BASE = 9.8

def get_value(pos):
    #x, y, value at distance=0, distance scale
    sources = [[20, 0, 4, 3], [10, 5, 2, 2]]
    value = BASE
    for source in sources:
        distance = math.sqrt((source[0] - pos[0]) ** 2 + (source[1] - pos[1]) ** 2)
        exp_value = math.exp(math.log(source[2]) - distance / source[3])
        value -= exp_value
    return value

def get_noise2(pos):
    return 3 * abs(noise.snoise2(pos[0], pos[1], octaves=24, persistence=2.0, lacunarity=2.3))

class Board:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sensor_offset = 0.0000001

    def get_pos(self):
        return (self.x, self.y)

    def get_sensor1_pos(self):
        return (self.x, self.y - self.sensor_offset)

    def get_sensor2_pos(self):
        return (self.x - self.sensor_offset, self.y)

    def get_sensor3_pos(self):
        return (self.x, self.y + self.sensor_offset)

    def get_sensor4_pos(self):
        return (self.x + self.sensor_offset, self.y)

    def get_sensor1(self, add_noise = True):
        sensor_value = get_value(board.get_sensor1_pos())
        if add_noise:
            sensor_value -= get_noise2(board.get_sensor1_pos())
        return sensor_value

    def get_sensor2(self, add_noise = True):
        sensor_value = get_value(board.get_sensor2_pos())
        if add_noise:
            sensor_value -= get_noise2(board.get_sensor2_pos())
        return sensor_value

    def get_sensor3(self, add_noise = True):
        sensor_value = get_value(board.get_sensor3_pos())
        if add_noise:
            sensor_value -= get_noise2(board.get_sensor3_pos())
        return sensor_value

    def get_sensor4(self, add_noise = True):
        sensor_value = get_value(board.get_sensor4_pos())
        if add_noise:
            sensor_value -= get_noise2(board.get_sensor4_pos())
        return sensor_value

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


board = Board(0, 0)
while True:
    if (board.get_pos()[0] <= 0):
        dirx = 1
    if (board.get_pos()[0] >= 40):
        dirx = -1

    board.move(dirx, 0)

    sensor_1_value = board.get_sensor1()
    sensor_2_value = board.get_sensor2()
    sensor_3_value = board.get_sensor3()
    sensor_4_value = board.get_sensor4()

    #sys.stderr.write("Pos: {}\n".format(board.get_pos()))
    #sys.stderr.write("{} {} {} {}\n".format(sensor_1_value, sensor_2_value, sensor_3_value, sensor_4_value))
    packed = struct.pack("ffffc", sensor_1_value, sensor_2_value, sensor_3_value, sensor_4_value, b'\n')
    sys.stdout.write(str(packed))
    sys.stdout.flush()
    time.sleep(data_rate)
