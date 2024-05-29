from pymodbus.client import AsyncModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import asyncio
import constants as variables
from fiware_api import *

async def main():

    createEntities()
    createQuantumLeapSubscription()
    valuesDict = {}
    client = AsyncModbusTcpClient(variables.DEVICE_IP, port=variables.DEVICE_PORT)
    await client.connect()
    while True:
        
        
        #MONITOR DATA
        for slave in variables.DEVICE_MON_SLAVES:
        
            for register in variables.DEVICE_MON_REGISTERS:
                regBytes = variables.DEVICE_MON_REGISTERS_BYTES[register]
                result = await client.read_holding_registers(register, count=regBytes, slave=slave, unit=2)
                if regBytes > 1:
                    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.BIG).decode_32bit_int()
                    value = (decoder / variables.DEVICE_MON_REGISTERS_SCALE[register]) + variables.DEVICE_MON_REGISTERS_OFFSET[register]
                    print(f'slave: {slave}, register:{register}, register.result: {result.registers}, decode: {decoder}, value: {value}')
                if regBytes == 1:
                    value = (result.registers[0] / variables.DEVICE_MON_REGISTERS_SCALE[register]) + variables.DEVICE_MON_REGISTERS_OFFSET[register]
                    print('slave: {0}, register:{1}, register.result: {2}, value: {3}'.format(slave, register, result.registers, value))
                
                
                valuesDict[register] = value
            updateData(valuesDict, slave)

        #INVERTERS DATA
        for slave in variables.DEVICE_INV_SLAVES:
        
            for register in variables.DEVICE_INV_REGISTERS:
                regBytes = variables.DEVICE_INV_REGISTERS_BYTES[register]
                result = await client.read_holding_registers(register, count=regBytes, slave=slave, unit=2)
                if regBytes > 1:
                    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.BIG).decode_32bit_int()
                    value = (decoder / variables.DEVICE_INV_REGISTERS_SCALE[register]) + variables.DEVICE_INV_REGISTERS_OFFSET[register]
                    print(f'slave: {slave}, register:{register}, register.result: {result.registers}, decode: {decoder}, value: {value}')
                if regBytes == 1:
                    value = (result.registers[0] / variables.DEVICE_INV_REGISTERS_SCALE[register]) + variables.DEVICE_INV_REGISTERS_OFFSET[register]
                    print('slave: {0}, register:{1}, register.result: {2}, value: {3}'.format(slave, register, result.registers, value))
                
                
                valuesDict[register] = value
            updateData(valuesDict, slave)
        await asyncio.sleep(30)

if __name__ == "__main__":

    asyncio.run(main())
