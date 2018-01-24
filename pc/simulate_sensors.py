import struct
import sys
import time
import random

#seconds
data_rate = 0.5

while True:
    sensor_1_value = 9.81 + random.uniform(0.000, 0.009)
    sensor_2_value = 9.82 + random.uniform(0.000, 0.009)
    sensor_3_value = 9.83 + random.uniform(0.000, 0.009)
    sensor_4_value = 9.84 + random.uniform(0.000, 0.009)

    packed = struct.pack("ffffc", sensor_1_value, sensor_2_value, sensor_3_value, sensor_4_value, b'\n')
    sys.stdout.buffer.write(packed)
    sys.stdout.flush()
    time.sleep(data_rate)
