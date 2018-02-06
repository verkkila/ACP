import ArduinoSensors
import time
import sys
import curses

update_rate = 0.5
sensors = ArduinoSensors.ArduinoSensors()

def init():
    global update_rate, sensors
    if not sensors.open():
        sys.exit()
    try:
        update_rate = float(sys.argv[1]) * 0.001
    except (IndexError, TypeError):
        print("Using default refresh rate of {} ms".format(update_rate * 1000))
    else:
        print("Using refresh rate of {} ms".format(update_rate * 1000))

def curses_main(stdscr):
    while True:
        try:
            stdscr.clear()
            stdscr.addstr(0, 5, "{:.4f}".format(sensors.get_front()))
            stdscr.addstr(1, 0, "{:.4f}".format(sensors.get_left()))
            stdscr.addstr(1, 10, "{:.4f}".format(sensors.get_right()))
            stdscr.addstr(2, 5, "{:.4f}".format(sensors.get_back()))
            stdscr.refresh()
            time.sleep(update_rate)
        except KeyboardInterrupt:
            break
    sensors.close()

init()
curses.wrapper(curses_main)
