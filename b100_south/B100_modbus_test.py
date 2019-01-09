from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import time

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR) # Set to logging.DEBUG for verbose Modbus logging

  
def decode_and_scale_registers(registers, scaling_value):
    decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.Big, wordorder=Endian.Little)
    number = decoder.decode_32bit_int()
    number = number / scaling_value
    return number

if __name__ == "__main__":
    B100_ADDRESS = '192.168.1.200'
    MODBUS_PORT = 502

    client = ModbusClient(B100_ADDRESS, port=MODBUS_PORT, framer=ModbusFramer)
    test = client.connect()
    print(test)

    # rr1 = client.read_input_registers(0,38,unit=1)
    # print(rr1)
    # rr2 = client.read_input_registers(44,38, unit=1)
    # print(rr2)
    # rr3 = client.read_input_registers(88,38,unit=1)
    # print(rr3)
    # rr4 = client.read_input_registers(132,30,unit=1)
    # print(rr4)
    # rr5 = client.read_input_registers(168,32,unit=1)
    # print(rr5)

    # rr6 = client.read_discrete_inputs(0,4,unit=1)
    # print(rr6)
    # rr7 = client.read_discrete_inputs(5,4,unit=1)
    # print(rr7)

    LTC_TANK_TEMP_REG = 216
    TOP_OIL_TEMP_REG = 268
    UNIT = 1
    NUM_REGISTERS_TO_READ = 2
    SCALING_VALUE = 1000

    while(True):
        try:
            ltc_tank_temp_read = client.read_input_registers(LTC_TANK_TEMP_REG,NUM_REGISTERS_TO_READ,unit=UNIT)
            ltc_tank_temp = decode_and_scale_registers(ltc_tank_temp_read.registers, SCALING_VALUE)

            top_oil_temp_read = client.read_input_registers(TOP_OIL_TEMP_REG,NUM_REGISTERS_TO_READ,unit=UNIT)
            top_oil_temp = decode_and_scale_registers(top_oil_temp_read.registers, SCALING_VALUE)

            print(f'LTC Tank Temp: {ltc_tank_temp}\tTop Oil Temp: {top_oil_temp}')
            time.sleep(1)
        except Exception as ex:
            print(f'ERROR: {ex}')

    client.close()