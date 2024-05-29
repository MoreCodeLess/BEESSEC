import json
import os
import requests
import constants as variables

def createEntities():
    print(os.listdir())
    with open('mon_entity.json', 'r') as file:
        data = json.load(file)
        r = requests.post(url="http://127.0.0.1:1026/v2/entities", json=data)
        print(r.text)
    for pos in range(1,4):
        with open('inv_entity.json', 'r') as file:

            data = json.load(file)
            id_key = "id"
            type_key = "type"
            if id_key in data:
                data[id_key] = f"B00{pos}"
            if type_key in data:
                data[type_key] = f"B{pos}"
            r = requests.post(url="http://127.0.0.1:1026/v2/entities", json=data)
            print(r.text)

def createQuantumLeapSubscription():
    with open('mon_subscription.json', 'r') as file:
        data = json.load(file)
        r = requests.post(url="http://127.0.0.1:1026/v2/subscriptions", json=data)
        print(r.text)
    for pos in range(1, 4):
        with open('inv_subscription.json', 'r') as file:
            type_key = "type"
            data = json.load(file)
            if type_key in data["subject"]["entities"][0]:
                data["subject"]["entities"][0][type_key] = f"B{pos}"
            r = requests.post(url="http://127.0.0.1:1026/v2/subscriptions", json=data)
            print(r.text)

def updateData(collectedData, currentSlave):
    if currentSlave == 1:
        with open('mon_attrs.json', 'r') as file:
            data = json.load(file)

            for object in data:
                if object == "id":
                    continue
                if object == "type":
                    continue
                reg = variables.DEVICE_MON_REG_NAME[object]
                #print(reg)

                #print(object)
                for step in data[object]:
                    if "value" in data[object]:
                        newValue =  collectedData[reg]
                        data[object]["value"] = newValue
            # print(data[object])
            r = requests.patch(url=f"http://127.0.0.1:1026/v2/entities/M001/attrs", json=data)
            print(r.status_code)
    else:
        idFromSlave = 1 if currentSlave == 12 else 2 if currentSlave == 10 else 3
        with open('inv_attrs.json', 'r') as file:
            data = json.load(file)

            for object in data:
                if object == "id":
                    continue
                if object == "type":
                    continue
                reg = variables.DEVICE_INV_REG_NAME[object]
                #print(reg)

                #print(object)
                for step in data[object]:
                    if "value" in data[object]:
                        newValue =  collectedData[reg]
                        data[object]["value"] = newValue
            # print(data[object])
            r = requests.patch(url=f"http://127.0.0.1:1026/v2/entities/B00{idFromSlave}/attrs", json=data)
            print(r.status_code)
