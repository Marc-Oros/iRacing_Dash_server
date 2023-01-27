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
        # we shut down ir library (clear all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


def loop():
    speed = "{:03d}".format(int(ir['Speed']*3.6))
    rpm = "{:05d}".format(int(ir['RPM']))
    gear = ir['Gear'] + 1
    led = int(8*ir['ShiftIndicatorPct'])
    buf = str(led) + ' ' + str(speed) + ' ' + str(rpm) + ' ' + str(gear)
    final = buf.encode('ascii')
    cnt=ser.write(final)


ir = irsdk.IRSDK()
state = State()

maxrpm = 1
led = 0

while True:
    try:
        ser = serial.Serial('COM3', 9600)
        print("Serial connection established")
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
        break
    except serial.serialutil.SerialException:
        time.sleep(1)

