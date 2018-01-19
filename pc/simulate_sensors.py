import struct
import sys
import noise
import math
import time

#seconds
data_rate = 0.5

board_x = 0
board_y = 0
sensor_offset = 0.0000001

x_offset = 0
y_offset = 0

BASE = 9.8

octs=24
ps=2.0
lac=2.3
scale=3

def get_value(x, y):
    #x, y, value at distance=0, distance scale
    sources = [[20, 0, 4, 3], [10, 5, 2, 2]]
    value = BASE
    for source in sources:
        distance = math.sqrt((source[0] - x) ** 2 + (source[1] - y) ** 2)
        exp_value = math.exp(math.log(source[2]) - distance / source[3])
        value -= exp_value
    return value

i = 0
while True:
    i += 1
    if (i >= 50):
        i = 0
    x_offset = 0.5 * i
    y_offset = 0.5 * math.sin((i/49.0) * 2 * math.pi)
    real_x = board_x + x_offset
    real_y = board_y + y_offset

    sensor_1_value = get_value(real_x, real_y - sensor_offset) - scale*abs(noise.snoise2(real_x, real_y -sensor_offset, octaves=octs, persistence=ps, lacunarity=lac))
    sensor_2_value = get_value(real_x - sensor_offset, real_y) - scale*abs(noise.snoise2(real_x - sensor_offset, real_y, octaves=octs, persistence=ps, lacunarity=lac))
    sensor_3_value = get_value(real_x, real_y + sensor_offset) - scale*abs(noise.snoise2(real_x, real_y + sensor_offset, octaves=octs, persistence=ps, lacunarity=lac))
    sensor_4_value = get_value(real_x + sensor_offset, real_y) - scale*abs(noise.snoise2(real_x + sensor_offset, real_y, octaves=octs, persistence=ps, lacunarity=lac))
    sys.stderr.write("{} {} {} {}\n".format(sensor_1_value, sensor_2_value, sensor_3_value, sensor_4_value))
    packed = struct.pack("ffffc", sensor_1_value, sensor_2_value, sensor_3_value, sensor_4_value, b'\n')
    sys.stdout.write(str(packed))
    sys.stdout.flush()
    time.sleep(data_rate)
