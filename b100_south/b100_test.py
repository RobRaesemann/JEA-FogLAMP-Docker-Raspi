import b100modbus
import time

ADDRESS = '192.168.1.200'
PORT = "502"

while(True):
    readings = b100modbus.get_b100_readings(ADDRESS, PORT)
    print(readings)
    time.sleep(1)
