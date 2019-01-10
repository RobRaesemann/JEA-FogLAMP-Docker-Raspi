from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

modbus_client = None

def decode_and_scale_registers(registers, scaling_value):
    """ Converts unsigned int from Modbus device to a signed integer divided by the scaling_value """
    decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.Big, wordorder=Endian.Little)
    number = decoder.decode_32bit_int()
    number = number / scaling_value
    return number
    
def get_b100_readings(address, port):
    global modbus_client

    if modbus_client is None:
        try:                
            modbus_client = ModbusClient(address, port=port, framer=ModbusFramer)
        except:
            raise ValueError

    ltc_tank_temp = None
    top_oil_temp = None

    LTC_TANK_TEMP_REG = 216
    TOP_OIL_TEMP_REG = 268
    UNIT = 1
    NUM_REGISTERS_TO_READ = 2
    SCALING_VALUE = 1000

    # read LTC Tank Temperature
    try:
        ltc_tank_temp_read = modbus_client.read_input_registers(LTC_TANK_TEMP_REG,NUM_REGISTERS_TO_READ,unit=UNIT)
        ltc_tank_temp = decode_and_scale_registers(ltc_tank_temp_read.registers, SCALING_VALUE)
    except Exception as ex:
        print(ex) 
        ltc_tank_temp = 'error'
			
    try:
        top_oil_temp_read = modbus_client.read_input_registers(TOP_OIL_TEMP_REG,NUM_REGISTERS_TO_READ,unit=UNIT)
        top_oil_temp = decode_and_scale_registers(top_oil_temp_read.registers, SCALING_VALUE)
    except: 
        top_oil_temp = 'error'
			
    readings = {
        'ltc_tank_temp': ltc_tank_temp,
        'top_oil_temp': top_oil_temp
        }

    return readings

def close_connection():
    global modbus_client
    try:
        if modbus_client is not None:
            modbus_client.close()
            return('B100 client connection closed.')
    except:
        raise
    else:
        modbus_client = None
        return('B100 plugin shut down.')