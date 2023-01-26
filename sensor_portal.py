#!/usr/bin/env python

import argparse
import asyncio
import json
import websockets

async def getSensorList(websocket):
    requestSensorList = { "request": "sensor-list" }
    await websocket.send(json.dumps(requestSensorList))
    pkt = await websocket.recv()
    j = json.loads(pkt)
    assert(j['event'] == 'sensor-list')
    return j['data']['sensors']


async def getSensorData(websocket, sensor):
    requestSensorData = { "request": "sensor-details", "args":f"{sensor}" }
    await websocket.send(json.dumps(requestSensorData))
    pkt = await websocket.recv()
    j = json.loads(pkt)
    assert(j['event'] == 'sensor-details')
    return j['data']


async def main(uri):
    print(f"Opening connection to Veriflite portal: {uri}")
    async with websockets.connect(uri) as websocket:
        # Print the "Connection opened" message
        pkt = await websocket.recv()
        print(pkt)

        sensorList = await getSensorList(websocket)

        for sensor in sensorList:
            sensorDetails = await getSensorData(websocket, sensor)
            print(f"{sensor}")
            print(f"\tName: {sensorDetails['friendlyName']}")
            print(f"\tFirmware version: {sensorDetails['firmwareVersion']}")
            print(f"\tBattery voltage: {sensorDetails['batteryLevel']}")
            print(f"\tBootup number: {sensorDetails['bootNumber']}")
            print(f"\tPaired: {sensorDetails['isPaired']}")
            print(f"\tSync ID: {sensorDetails['syncID']}")
            print(f"\tLifetime jumps: {sensorDetails['lifetimeJumps']}")
            print(f"\tLifetime age: {sensorDetails['lifetimeAge']}")
            print(f"\tUID: {sensorDetails['uniqueID']}")
            print(f"\tAdvertising rate: {sensorDetails['advertisingRate']}")
            print(f"\tHigh power mode: {sensorDetails['isHighPowerMode']}")
            print()


        while True:
            pkt = await websocket.recv()

            try:
                j = json.loads(pkt)
            except json.decoder.JSONDecodeError:
                print(f"::: {pkt}")
                continue
            print(f"{j}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, required=True, help="The IP address of the Veriflite portal")
    args = parser.parse_args()

    asyncio.run(main(f"ws://{args.ip}:4651/sensor"))

