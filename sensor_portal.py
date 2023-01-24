#!/usr/bin/env python

import argparse
import asyncio
import json
import websockets

async def main(uri):
    print(f"Opening connection to Veriflite portal: {uri}")
    async with websockets.connect(uri) as websocket:
        pkt = await websocket.recv()
        print(pkt)

        requestSensorList = { "requestType": "SensorList" }
        await websocket.send(json.dumps(requestSensorList))

        pkt = await websocket.recv()
        sensorList = json.loads(pkt)

        for i in sensorList['Sensors']:
            print(f"\nSensor {i}")
            requestSensorDetails = { "requestType": "SensorDetails", "args":f"{i}" }
            await websocket.send(json.dumps(requestSensorDetails))

            pkt = await websocket.recv()
            sensorDetails = json.loads(pkt)
            print(f"\tFirmware version: {sensorDetails['FirmwareVersion']}")
            print(f"\tBattery voltage: {sensorDetails['BatteryLevel']}")
            print(f"\tBootup number: {sensorDetails['BootNumber']}")
            print(f"\tLifetime jumps: {sensorDetails['LifetimeJumps']}")
            print(f"\tLifetime age: {sensorDetails['LifetimeAge']}")
            print(f"\tUID: {sensorDetails['UID']}")
            print(f"\tAdvertising rate: {sensorDetails['AdvertisingRate']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, required=True, help="The IP address of the Veriflite portal")
    args = parser.parse_args()

    asyncio.run(main(f"ws://{args.ip}:4651/sensor"))

