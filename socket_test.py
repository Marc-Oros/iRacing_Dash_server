#!python3
import irsdk
import time
import socket

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
        # we shut down ir library (clear all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


def loop(sock):
    global maxrpm
    speed = "{:03d}".format(int(ir['Speed']*3.6))
    rpm = "{:05d}".format(int(ir['RPM']))
    gear = ir['Gear'] + 1
    maxrpm = max(maxrpm, ir['RPM'])
    rpm_thr = maxrpm*0.75
    curr_thr = int(rpm) - rpm_thr
    if int(rpm) < rpm_thr:
        led = 0
    else:
        led = int(min((curr_thr+50)/(maxrpm-rpm_thr), 1)*8)
    buf = str(led) + ' ' + str(speed) + ' ' + str(rpm) + ' ' + str(gear)
    final = buf.encode('ascii')
    sock.send(final)
    

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.56"
port = 8086
serversocket.bind((host, port))

serversocket.listen(5)
print('server started and listening')
(clientsocket, address) = serversocket.accept()
print("connected to client")

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
            loop(clientsocket)
        # sleep for 1 second
        # maximum you can use is 1/60
        # cause iracing update data with 60 fps
        time.sleep(1/60)
except KeyboardInterrupt:
    # press ctrl+c to exit
    pass
