from pymodbus.client import AsyncModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import asyncio

async def main():

    #createEntities()
    #createQuantumLeapSubscription()
    valuesDict = {}
    while True:
        
        client = AsyncModbusTcpClient("127.0.0.1", port=502)
        await client.connect()
        slave = 15

        

        result = await client.read_holding_registers(70 - 1, slave=slave)

        print('slave: {0}, register:{1}, result: {2}'.format(slave, 70, result.registers))
            
        valuesDict[70] = 0
        #updateData(valuesDict, slave)
        await asyncio.sleep(10)

if __name__ == "__main__":

    asyncio.run(main())