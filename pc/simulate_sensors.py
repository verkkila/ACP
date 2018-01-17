import struct
import sys
import noise
import math
import time

board_x = 0
board_y = 0
sensor_offset = 0.0000001

x_offset = 0
y_offset = 0

BASE = 9.8

octs=16
ps=2.0
lac=2.2
scale=3

i = 0
while True:
    i += 1
    if (i >= 50):
        i = 0
    x_offset = 0.5 * i
    y_offset = 0.5 * math.sin((i/49.0) * 2 * math.pi)
    sensor_1_value = BASE - scale*abs(noise.snoise2(board_x + x_offset, board_y - sensor_offset + y_offset, octaves=octs, persistence=ps, lacunarity=lac))
    sensor_2_value = BASE - scale*abs(noise.snoise2(board_x - sensor_offset + x_offset, board_y + y_offset, octaves=octs, persistence=ps, lacunarity=lac))
    sensor_3_value = BASE - scale*abs(noise.snoise2(board_x + x_offset, board_y + sensor_offset + y_offset, octaves=octs, persistence=ps, lacunarity=lac))
    sensor_4_value = BASE - scale*abs(noise.snoise2(board_x + sensor_offset + x_offset, board_y + y_offset, octaves=octs, persistence=ps, lacunarity=lac))
    #print("{} {} {} {}".format(sensor_1_value, sensor_2_value, sensor_3_value, sensor_4_value))
    packed = struct.pack("ffffc", sensor_1_value, sensor_2_value, sensor_3_value, sensor_4_value, b'\n')
    sys.stdout.write(str(packed))
    sys.stdout.flush()
    time.sleep(1)
