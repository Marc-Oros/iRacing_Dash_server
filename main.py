#!python3
import irsdk
import time
import serial


class State:
    ir_connected = False
    last_car_setup_tick = -1


def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset all your in State variables
        state.last_car_setup_tick = -1
        global maxrpm
        maxrpm = 1
        # we are shut down ir library (clear all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


def loop():
    global maxrpm
    speed = "{:03d}".format(int(ir['Speed']/3.6))
    rpm = "{:05d}".format(int(ir['RPM']))
    gear = ir['Gear'] + 1
    maxrpm = max(maxrpm, ir['RPM'])
    ratio = ir['RPM'] / maxrpm
    if ratio < 3/4:
        led = 0
    elif ratio < 7/8:
        led = 1
    elif ratio <= 1:
        led = 2
    buf = str(led) + ' ' + str(speed) + ' ' + str(rpm) + ' ' + str(gear)
    final = buf.encode('ascii')
    cnt=ser.write(final)


ser = serial.Serial('COM3', 9600)
ir = irsdk.IRSDK()
state = State()

maxrpm = 1
led = 0

try:
    # infinite loop
    while True:
        # check if we are connected to iracing
        check_iracing()
        # if we are, then process data
        if state.ir_connected:
            loop()
        # sleep for 1 second
        # maximum you can use is 1/60
        # cause iracing update data with 60 fps
        time.sleep(1/60)
except KeyboardInterrupt:
    # press ctrl+c to exit
    pass
