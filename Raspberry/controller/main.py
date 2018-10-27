#!/usr/bin/python3.5
# coding: utf-8



import signal
from sensorDHT11 import SensorDHT11
import sys

if __name__ == '__main__':

    try:
        sensor = SensorDHT11()
        signal.pause()
    except KeyboardInterrupt :
        sensor.connectionDB.close()
        print('Se desconecto satisfactorio')
        sys.exit()


