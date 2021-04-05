import sys, os, math

import serial
import rak811

ser = serial.Serial('/dev/serial-', 115200, timeout=5)

print(ser.name)
x = ser.write(b'at+version\r\n')
s = ser.read(255)
print(s)
ser.close()