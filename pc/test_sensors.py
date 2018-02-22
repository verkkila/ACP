import ArduinoSensors
import time
import sys
import curses
import logging

update_rate = 0.5
sensors = ArduinoSensors.ArduinoSensors()
logger = logging.getLogger("arduino")

def init():
    global update_rate, sensors
    if not sensors.open():
        sys.exit()
    try:
        update_rate = float(sys.argv[1]) * 0.001
    except (IndexError, TypeError):
        logger.debug("Using default refresh rate of {:.0f}ms".format(update_rate * 1000))
        print("Using default refresh rate of {} ms".format(update_rate * 1000))
    else:
        logger.debug("Using refresh rate of {:.0f}ms".format(update_rate * 1000))
        print("Using refresh rate of {} ms".format(update_rate * 1000))

def curses_main(stdscr):
    prev_val_front = prev_val_left = prev_val_right = prev_val_back = 0
    logger.info("FRONT LEFT RIGHT BACK DELTA_FRONT DELTA_LEFT DELTA_RIGHT DELTA_BACK")
    while True:
        try:
            cycle_start = time.clock()
            val_front = sensors.get_front()
            val_left = sensors.get_left()
            val_right = sensors.get_right()
            val_back = sensors.get_back()
            stdscr.addstr(0, 5, "{:.4f}".format(val_front))
            stdscr.addstr(1, 0, "{:.4f}".format(val_left))
            stdscr.addstr(1, 10, "{:.4f}".format(val_right))
            stdscr.addstr(2, 5, "{:.4f}".format(val_back))

            stdscr.addstr(0, 30, "{:.4f}".format(val_front - prev_val_front))
            stdscr.addstr(1, 25, "{:.4f}".format(val_left - prev_val_left))
            stdscr.addstr(1, 35, "{:.4f}".format(val_right - prev_val_right))
            stdscr.addstr(2, 30, "{:.4f}".format(val_back - prev_val_back))
            cycle_time = time.clock() - cycle_start
            stdscr.addstr(5, 0, "Cycle time: {:.5f}s (update rate {}s)".format(cycle_time, update_rate))
            logger.info("{}: {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}".format(time.strftime("%H:%M:%S", time.localtime()), val_front, val_left, val_right, val_back, val_front - prev_val_front, val_left - prev_val_left, val_right - prev_val_right, val_back - prev_val_back))
            prev_val_front = val_front
            prev_val_left = val_left
            prev_val_right = val_right
            prev_val_back = val_back
            stdscr.refresh()
            time.sleep(max(update_rate - cycle_time, 0.01))
        except KeyboardInterrupt:
            break
    sensors.close()

logging.basicConfig(filename="logs/log_{}.txt".format(time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())), level=logging.DEBUG)
init()
curses.wrapper(curses_main)
